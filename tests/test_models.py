from datetime import date

import pytest

from expense_tracker.models import Expense


def make_expense(**overrides) -> Expense:
    """An Expense with sensible defaults, overridable per test."""
    values = {
        "id": 1,
        "amount_paise": 25000,
        "category": "food",
        "date": date(2026, 9, 27),
        "note": "",
    }
    return Expense(**{**values, **overrides})


def test_rupees_converts_from_paise():
    assert make_expense(amount_paise=25000).rupees == 250.0


def test_rejects_zero_amount():
    with pytest.raises(ValueError, match="must be positive"):
        make_expense(amount_paise=0)


def test_rejects_negative_amount():
    with pytest.raises(ValueError, match="must be positive"):
        make_expense(amount_paise=-100)


def test_rejects_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        make_expense(category="groceries")


def test_error_lists_the_valid_categories():
    with pytest.raises(ValueError, match="food, transport, rent, other"):
        make_expense(category="groceries")


def test_rejects_an_overlong_note():
    with pytest.raises(ValueError, match="200 characters"):
        make_expense(note="x" * 201)


def test_to_dict_and_back_gives_an_equal_expense():
    original = make_expense(note="lunch")
    assert Expense.from_dict(original.to_dict()) == original


def test_from_dict_handles_a_missing_note():
    data = {
        "id": 1,
        "amount_paise": 25000,
        "category": "food",
        "date": "2026-09-27",
    }
    assert Expense.from_dict(data).note == ""


def test_expenses_with_identical_fields_are_equal():
    assert make_expense() == make_expense()


def test_expenses_with_different_ids_are_not_equal():
    assert make_expense(id=1) != make_expense(id=2)
