from __future__ import annotations

import logging
from typing import Any

import anthropic

from helpbot.config import Settings, SYSTEM_PROMPT
from helpbot.conversation import Conversation
from helpbot.output import StreamResult, stream_reply
from helpbot.rag import RAGIndex
from helpbot.tools import TOOL_SCHEMAS, execute_tool_calls

log = logging.getLogger(__name__)

_CACHED_SYSTEM = [
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},
    }
]


class HelpBot:
    """Stateful HelpBot session.

    One instance per customer session. Owns the conversation history and
    coordinates RAG retrieval, tool execution, and streaming.
    """

    def __init__(self, settings: Settings, rag_index: RAGIndex) -> None:
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._settings = settings
        self._rag = rag_index
        self._conversation = Conversation()
        self._temperature = settings.temperature
        self._prefill: str = ""

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Temperature must be between 0.0 and 1.0, got {value}")
        self._temperature = value

    @property
    def prefill(self) -> str:
        return self._prefill

    @prefill.setter
    def prefill(self, value: str) -> None:
        self._prefill = value.strip()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------
    def chat(self, user_input: str) -> StreamResult:
        """Process one customer turn and return the streamed reply."""
        augmented = self._augment_with_rag(user_input)
        self._conversation.add_user(augmented)
        return self._run_turn()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------
    def _augment_with_rag(self, text: str) -> str:
        chunks = self._rag.search(text, self._settings.voyage_api_key)
        if not chunks:
            return text
        context = "\n\n---\n\n".join(chunks)
        return (
            f"<policy_context>\n{context}\n</policy_context>\n\n"
            f"Customer question: {text}"
        )

    def _call(self) -> Any:
        return self._client.messages.create(
            model=self._settings.model,
            max_tokens=self._settings.max_tokens,
            system=_CACHED_SYSTEM,
            messages=self._conversation.messages,
            tools=TOOL_SCHEMAS,
            temperature=self._temperature,
        )

    def _run_turn(self) -> StreamResult:
        # Tool loop — iterate until Claude stops requesting tools.
        while True:
            response = self._call()
            self._conversation.add_assistant_raw(response.content)

            if response.stop_reason != "tool_use":
                # Replace the non-streamed assistant entry with a streamed one.
                self._conversation.pop_last()

                # Inject prefill: add a partial assistant turn so Claude continues
                # from that exact phrase, then remove it before storing history.
                if self._prefill:
                    self._conversation.add_assistant(self._prefill)

                result = stream_reply(
                    client=self._client,
                    model=self._settings.model,
                    system=_CACHED_SYSTEM,
                    messages=self._conversation.messages,
                    tools=TOOL_SCHEMAS,
                    temperature=self._temperature,
                    prefill=self._prefill,
                )

                if self._prefill:
                    self._conversation.pop_last()  # remove the bare prefill entry

                self._conversation.add_assistant(result.text)
                return result

            tool_results = execute_tool_calls(response.content)
            self._conversation.add_tool_results(tool_results)
