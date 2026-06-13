from __future__ import annotations

import json
import logging
from datetime import date, datetime
from typing import Any

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data layer (swap this dict for a real DB call in production)
# ---------------------------------------------------------------------------
_BOOKS: dict[str, dict[str, Any]] = {
    "The Midnight Library": {"in_stock": False, "restock_date": "2026-07-05"},
    "Atomic Habits":        {"in_stock": True,  "restock_date": None},
    "Project Hail Mary":    {"in_stock": False, "restock_date": "2026-06-28"},
    "The Thursday Murder Club": {"in_stock": False, "restock_date": "2026-07-15"},
    "Lessons in Chemistry": {"in_stock": True,  "restock_date": None},
}

_ORDERS: dict[str, dict[str, Any]] = {
    "PT-9923": {
        "status": "shipped",
        "carrier": "FedEx",
        "eta": "Tomorrow by 8 pm",
        "order_date": "2026-05-20",
    },
    "PT-0042": {
        "status": "processing",
        "carrier": None,
        "eta": "Ships in 2 business days",
        "order_date": "2026-06-10",
    },
    "PT-7777": {
        "status": "delivered",
        "carrier": "UPS",
        "eta": "Delivered yesterday",
        "order_date": "2026-05-01",
    },
}

_RETURN_WINDOW_DAYS = 30


def _validate_order_id(order_id: str) -> None:
    if not order_id or not order_id.startswith("PT-"):
        raise ValueError(
            f"Invalid order ID '{order_id}'. Expected format: PT-XXXX."
        )


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------
def check_order_status(order_id: str) -> dict[str, Any]:
    _validate_order_id(order_id)
    order = _ORDERS.get(order_id)
    if order is None:
        return {"status": "not_found", "message": f"No order found for {order_id}."}
    return {k: v for k, v in order.items() if k != "order_date"}


def get_estimated_restock_date(book_title: str) -> dict[str, Any]:
    """Return restocking information for an out-of-stock book."""
    if not book_title or not book_title.strip():
        raise ValueError("book_title must not be empty.")

    # Case-insensitive lookup
    title_lower = book_title.strip().lower()
    match = next(
        (info for title, info in _BOOKS.items() if title.lower() == title_lower),
        None,
    )

    if match is None:
        return {
            "found": False,
            "message": (
                f"'{book_title}' is not in our catalogue. "
                "It may be available by special order — contact us at orders@pageturner.com."
            ),
        }

    if match["in_stock"]:
        return {"found": True, "in_stock": True, "restock_date": None,
                "message": f"'{book_title}' is currently in stock and ready to ship."}

    return {
        "found": True,
        "in_stock": False,
        "restock_date": match["restock_date"],
        "message": (
            f"'{book_title}' is currently out of stock. "
            + (
                f"Expected back in stock around {match['restock_date']}."
                if match["restock_date"]
                else "No restock date confirmed yet — check back soon."
            )
        ),
    }


def check_return_eligibility(order_id: str) -> dict[str, Any]:
    _validate_order_id(order_id)
    order = _ORDERS.get(order_id)
    if order is None:
        return {"eligible": False, "reason": f"No order found for {order_id}."}

    order_date = datetime.strptime(order["order_date"], "%Y-%m-%d").date()
    days_since = (date.today() - order_date).days
    eligible = days_since <= _RETURN_WINDOW_DAYS

    return {
        "eligible": eligible,
        "days_since_order": days_since,
        "days_remaining": max(0, _RETURN_WINDOW_DAYS - days_since),
        "reason": (
            f"Order placed {days_since} days ago — "
            + ("within" if eligible else "outside")
            + f" the {_RETURN_WINDOW_DAYS}-day return window."
        ),
    }


# ---------------------------------------------------------------------------
# Tool registry — maps name → callable
# ---------------------------------------------------------------------------
_REGISTRY: dict[str, Any] = {
    "check_order_status": check_order_status,
    "check_return_eligibility": check_return_eligibility,
    "get_estimated_restock_date": get_estimated_restock_date,
}

# ---------------------------------------------------------------------------
# Tool schemas exposed to Claude
# cache_control on the last entry caches the full tools list (Module 5)
# ---------------------------------------------------------------------------
TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "check_order_status",
        "description": (
            "Looks up the current shipping and delivery status of a PageTurner order. "
            "Call this when a customer asks where their order is, when it arrives, "
            "or whether it has been delivered."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "PageTurner order ID in the format PT-XXXX (e.g. PT-9923).",
                }
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "check_return_eligibility",
        "description": (
            "Checks whether a PageTurner order is within the 30-day return window. "
            "Call this when a customer asks if they can return an order or how many "
            "days they have left."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "PageTurner order ID in the format PT-XXXX.",
                }
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "get_estimated_restock_date",
        "description": (
            "Returns stock availability and expected restock date for a book by title. "
            "Call this when a customer asks about an out-of-stock book, when a title "
            "will be available, or whether they can order an unavailable title."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "book_title": {
                    "type": "string",
                    "description": "The exact title of the book (e.g. 'The Midnight Library').",
                }
            },
            "required": ["book_title"],
        },
        "cache_control": {"type": "ephemeral"},
    },
]


# ---------------------------------------------------------------------------
# Executor
# ---------------------------------------------------------------------------
def execute_tool_calls(blocks: list[Any]) -> list[dict[str, Any]]:
    """Run every tool_use block in *blocks* and return tool_result dicts."""
    results: list[dict[str, Any]] = []

    for block in blocks:
        if block.type != "tool_use":
            continue

        fn = _REGISTRY.get(block.name)
        if fn is None:
            log.error("Unknown tool requested: %s", block.name)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Tool '{block.name}' is not available.",
                "is_error": True,
            })
            continue

        try:
            output = fn(**block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(output),
                "is_error": False,
            })
        except Exception:
            log.exception("Tool '%s' raised an exception", block.name)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Tool '{block.name}' failed. Please try again.",
                "is_error": True,
            })

    return results
