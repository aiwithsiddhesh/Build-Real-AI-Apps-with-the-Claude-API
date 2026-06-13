from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from helpbot import HelpBot, RAGIndex, Settings
from helpbot.media import ask_about_image
from helpbot.output import extract_return_request

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s  %(name)s  %(message)s",
)
log = logging.getLogger(__name__)

POLICY_PATH = "pageturner_returns_policy.md"

_TEMP_PRESETS: dict[str, tuple[float, str]] = {
    "precise":  (0.1, "order lookups — consistent, factual"),
    "support":  (0.3, "standard support — default"),
    "warm":     (0.7, "apology emails — more human-feeling"),
    "creative": (0.9, "book recommendations — varied & surprising"),
}

_DAMAGE_CATEGORIES = (
    "torn cover, water damage, missing pages, printing defect, incorrect item, other"
)


def _print_banner(temperature: float, prefill: str) -> None:
    print("=" * 60)
    print("  PageTurner Books — Customer Support (HelpBot)")
    print("=" * 60)
    print(f"  Temperature : {temperature}  (/temp <0.0–1.0> or preset)")
    print("  Presets     : /temp precise · support · warm · creative")
    prefill_display = f'"{prefill}"' if prefill else "off"
    print(f"  Prefill     : {prefill_display}  (/prefill <phrase> | /prefill off)")
    print("  Commands    : 'return' · /image <path> · 'quit'")
    print("-" * 60)


# ---------------------------------------------------------------------------
# /temp
# ---------------------------------------------------------------------------
def _handle_temp(bot: HelpBot, arg: str) -> None:
    arg = arg.strip().lower()
    if arg in _TEMP_PRESETS:
        value, label = _TEMP_PRESETS[arg]
        bot.temperature = value
        print(f"  [temperature → {value}  ({label})]\n")
        return
    try:
        value = float(arg)
        bot.temperature = value
        print(f"  [temperature → {value}]\n")
    except ValueError:
        print(
            f"  [invalid value '{arg}' — use a number 0.0–1.0 "
            f"or a preset: {', '.join(_TEMP_PRESETS)}]\n"
        )


# ---------------------------------------------------------------------------
# /prefill
# ---------------------------------------------------------------------------
def _handle_prefill(bot: HelpBot, arg: str) -> None:
    arg = arg.strip()
    if arg.lower() == "off" or arg == "":
        bot.prefill = ""
        print("  [prefill cleared — responses start naturally]\n")
    else:
        bot.prefill = arg
        print(f'  [prefill set → "{bot.prefill}"]\n')


# ---------------------------------------------------------------------------
# return
# ---------------------------------------------------------------------------
def _handle_return(bot: HelpBot, settings: Settings) -> None:
    print("\n[Return Request]")
    print("Describe your return — include order ID, reason, and urgency:")

    try:
        raw = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        return

    if not raw:
        return

    try:
        form = extract_return_request(
            client=bot._client,
            model=settings.model,
            customer_message=raw,
        )
    except Exception as exc:
        log.error("Could not parse return request: %s", exc)
        print("[HelpBot] Sorry, I had trouble reading that. Please try again.\n")
        return

    print("\n--- Return Request Filed ---")
    print(json.dumps(form, indent=2))
    print("----------------------------")

    reply = (
        f"I've logged your return for order {form.get('order_id', 'N/A')}. "
        "You'll receive a confirmation email within 24 hours."
    )
    print(f"\nHelpBot: {reply}\n")


# ---------------------------------------------------------------------------
# /image
# ---------------------------------------------------------------------------
def _handle_image(bot: HelpBot, settings: Settings, path_str: str) -> None:
    path = Path(path_str.strip().strip('"').strip("'"))
    if not path.exists():
        print(f"  [file not found: {path}]\n")
        return

    print(f"\n[Analysing image: {path.name}]")
    try:
        analysis = ask_about_image(
            client=bot._client,
            model=settings.model,
            image_path=path,
            question=(
                "You are a customer support agent for PageTurner Books. "
                "A customer has sent a photo of their book. "
                f"Categorise the damage into exactly one of: {_DAMAGE_CATEGORIES}. "
                "Then write a 1-sentence description of what you see. "
                "Reply in this format:\n"
                "Category: <category>\nDescription: <description>"
            ),
        )
    except Exception as exc:
        log.error("Image analysis failed: %s", exc)
        print("  [HelpBot] Could not analyse the image. Please try again.\n")
        return

    print(f"\nHelpBot (image analysis):\n{analysis}\n")

    # Feed the finding into the ongoing conversation so HelpBot can act on it
    damage_summary = f"[Customer attached a photo of their book. Analysis: {analysis}]"
    result = bot.chat(
        f"{damage_summary}\n\nPlease acknowledge the damage and ask for their order ID "
        "so I can arrange a replacement or refund."
    )
    print(
        f"  [tokens  in={result.input_tokens}"
        f"  out={result.output_tokens}"
        f"  cache_read={result.cache_read_tokens}"
        f"  cache_write={result.cache_write_tokens}"
        f"  temp={bot.temperature}]\n"
    )


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main() -> None:
    try:
        settings = Settings.from_env()
    except EnvironmentError as exc:
        sys.exit(str(exc))

    rag = RAGIndex()
    rag.build(POLICY_PATH, settings.voyage_api_key)

    bot = HelpBot(settings=settings, rag_index=rag)

    _print_banner(bot.temperature, bot.prefill)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHelpBot: Thanks for contacting PageTurner. Happy reading!")
            break

        if not user_input:
            continue

        # --- slash commands (checked before match so lowercasing is safe) ---
        lower = user_input.lower()

        if lower.startswith("/temp"):
            arg = user_input[5:].strip()
            if not arg:
                print(f"  [current temperature: {bot.temperature}]\n")
            else:
                _handle_temp(bot, arg)
            continue

        if lower.startswith("/prefill"):
            _handle_prefill(bot, user_input[8:])
            continue

        if lower.startswith("/image"):
            path_arg = user_input[6:].strip()
            if not path_arg:
                print("  [usage: /image <path/to/photo.jpg>]\n")
            else:
                _handle_image(bot, settings, path_arg)
            continue

        match lower:
            case "quit" | "exit" | "bye":
                print("HelpBot: Thanks for contacting PageTurner. Happy reading!")
                break
            case "return":
                _handle_return(bot, settings)
            case _:
                result = bot.chat(user_input)
                print(
                    f"  [tokens  in={result.input_tokens}"
                    f"  out={result.output_tokens}"
                    f"  cache_read={result.cache_read_tokens}"
                    f"  cache_write={result.cache_write_tokens}"
                    f"  temp={bot.temperature}]\n"
                )


if __name__ == "__main__":
    main()
