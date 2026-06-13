from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

import anthropic

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class StreamResult:
    text: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int


def stream_reply(
    client: anthropic.Anthropic,
    model: str,
    system: list[dict[str, Any]],
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    temperature: float,
    on_token: Any = None,
    prefill: str = "",
) -> StreamResult:
    """Stream a Claude reply token-by-token.

    Args:
        on_token: Optional callable(str) invoked for each text chunk.
                  Defaults to printing to stdout.
        prefill: If set, printed immediately before streaming begins and
                 prepended to the stored text so history is complete.
    """
    emit = on_token or (lambda chunk: print(chunk, end="", flush=True))

    if prefill:
        emit(prefill)

    streamed_text = ""

    with client.messages.stream(
        model=model,
        max_tokens=1000,
        system=system,
        messages=messages,
        tools=tools,
        temperature=temperature,
    ) as stream:
        for chunk in stream.text_stream:
            emit(chunk)
            streamed_text += chunk

        usage = stream.get_final_message().usage

    return StreamResult(
        text=prefill + streamed_text,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0) or 0,
        cache_write_tokens=getattr(usage, "cache_creation_input_tokens", 0) or 0,
    )


def extract_return_request(
    client: anthropic.Anthropic,
    model: str,
    customer_message: str,
) -> dict[str, Any]:
    """Return a structured return-request dict from free-text customer input.

    Uses prefilling + a stop sequence so the response is always raw JSON
    with no markdown wrapper or explanation text.
    """
    prompt = (
        "Extract a return request from the customer message below.\n"
        "Respond with ONLY a JSON object — no explanation, no markdown.\n"
        "Fields: order_id, reason, urgency (low|medium|high), "
        "customer_name (null if absent), "
        "preferred_resolution (refund|exchange|store_credit|unknown).\n\n"
        f"Customer message: {customer_message}"
    )

    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "```json"},  # prefill
        ],
        stop_sequences=["```"],
    )

    raw = "```json" + response.content[0].text
    return json.loads(raw.replace("```json", "").replace("```", "").strip())
