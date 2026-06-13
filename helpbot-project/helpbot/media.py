from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

import anthropic

_MIME_MAP: dict[str, str] = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
}


def _b64(path: Path) -> str:
    return base64.standard_b64encode(path.read_bytes()).decode("utf-8")


def ask_about_image(
    client: anthropic.Anthropic,
    model: str,
    image_path: str | Path,
    question: str,
) -> str:
    path = Path(image_path)
    mime = _MIME_MAP.get(path.suffix.lstrip(".").lower(), "image/jpeg")

    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime,
                        "data": _b64(path),
                    },
                },
                {"type": "text", "text": question},
            ],
        }],
    )
    return response.content[0].text


def ask_about_pdf(
    client: anthropic.Anthropic,
    model: str,
    pdf_path: str | Path,
    question: str,
) -> str:
    path = Path(pdf_path)

    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": _b64(path),
                    },
                    "title": path.stem,
                },
                {"type": "text", "text": question},
            ],
        }],
    )
    return response.content[0].text
