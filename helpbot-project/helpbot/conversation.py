from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Conversation:
    """Owns the message history for a single customer session.

    The Claude API is stateless — every request must carry the full history.
    This class is the single source of truth for that history.
    """

    _messages: list[dict[str, Any]] = field(default_factory=list)

    @property
    def messages(self) -> list[dict[str, Any]]:
        return self._messages

    def add_user(self, text: str) -> None:
        self._messages.append({"role": "user", "content": text})

    def add_assistant(self, text: str) -> None:
        self._messages.append({"role": "assistant", "content": text})

    def add_assistant_raw(self, content: Any) -> None:
        """Appends a raw content block (may include tool_use blocks)."""
        self._messages.append({"role": "assistant", "content": content})

    def add_tool_results(self, results: list[dict[str, Any]]) -> None:
        self._messages.append({"role": "user", "content": results})

    def pop_last(self) -> dict[str, Any]:
        return self._messages.pop()

    def __len__(self) -> int:
        return len(self._messages)
