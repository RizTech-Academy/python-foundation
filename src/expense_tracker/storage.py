"""Reading and writing the JSON data file."""

import json
import os
from pathlib import Path

from .models import Expense


def data_file() -> Path:
    """Where expenses are stored. Overridable for tests and scripts."""
    override = os.environ.get("EXPENSES_FILE")
    return Path(override) if override else Path.home() / ".expenses.json"


def load(path: Path) -> tuple[list[Expense], int]:
    """Return the stored expenses and the next id.

    A missing file is treated as empty. A corrupt one raises, so we never
    silently discard somebody's data.
    """
    if not path.exists():
        return [], 1

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error}") from error

    expenses = [Expense.from_dict(item) for item in raw.get("expenses", [])]
    return expenses, int(raw.get("next_id", len(expenses) + 1))


def save(path: Path, expenses: list[Expense], next_id: int) -> None:
    """Write expenses to disk, replacing the file atomically.

    Writing to a temporary file and replacing means a crash part-way through
    leaves the original intact rather than half a file.
    """
    payload = {
        "next_id": next_id,
        "expenses": [expense.to_dict() for expense in expenses],
    }
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    temporary.replace(path)
