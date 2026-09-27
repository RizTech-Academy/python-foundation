from datetime import date

import pytest

from expense_tracker.models import Expense
from expense_tracker.storage import load, save


def test_load_of_a_missing_file_is_empty(tmp_path):
    expenses, next_id = load(tmp_path / "nothing.json")
    assert expenses == []
    assert next_id == 1


def test_save_then_load_round_trips(tmp_path):
    path = tmp_path / "expenses.json"
    original = [Expense(1, 25000, "food", date(2026, 9, 27), "lunch")]

    save(path, original, next_id=2)
    loaded, next_id = load(path)

    assert loaded == original
    assert next_id == 2


def test_corrupt_file_raises_rather_than_returning_empty(tmp_path):
    path = tmp_path / "expenses.json"
    path.write_text("this is not json", encoding="utf-8")

    with pytest.raises(ValueError, match="not valid JSON"):
        load(path)


def test_corrupt_file_is_not_overwritten(tmp_path):
    """The most valuable test here: corrupt data is never silently destroyed."""
    path = tmp_path / "expenses.json"
    path.write_text("this is not json", encoding="utf-8")

    with pytest.raises(ValueError):
        load(path)

    assert path.read_text(encoding="utf-8") == "this is not json"


def test_save_creates_missing_directories(tmp_path):
    path = tmp_path / "nested" / "deeper" / "expenses.json"
    save(path, [], next_id=1)
    assert path.exists()
