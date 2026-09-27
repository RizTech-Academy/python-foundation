from datetime import date

import pytest

from expense_tracker.models import Expense
from expense_tracker.reporting import (
    by_category,
    filter_expenses,
    format_table,
    total_paise,
)


@pytest.fixture
def expenses() -> list[Expense]:
    return [
        Expense(1, 25000, "food", date(2026, 9, 1)),
        Expense(2, 1500000, "rent", date(2026, 9, 1)),
        Expense(3, 12000, "food", date(2026, 10, 3)),
    ]


def test_total_sums_every_amount(expenses):
    assert total_paise(expenses) == 1537000


def test_total_of_nothing_is_zero():
    assert total_paise([]) == 0


def test_filter_by_category(expenses):
    assert [e.id for e in filter_expenses(expenses, category="food")] == [1, 3]


def test_filter_by_month(expenses):
    assert [e.id for e in filter_expenses(expenses, month="2026-10")] == [3]


def test_filters_combine(expenses):
    result = filter_expenses(expenses, category="food", month="2026-10")
    assert result == [expenses[2]]


def test_no_filters_returns_everything(expenses):
    assert filter_expenses(expenses) == expenses


def test_filter_with_no_matches_is_empty(expenses):
    assert filter_expenses(expenses, category="transport") == []


def test_by_category_groups_amounts(expenses):
    assert by_category(expenses) == {"food": 37000, "rent": 1500000}


def test_format_table_says_so_when_empty():
    assert format_table([]) == "No expenses found."


def test_format_table_includes_every_expense(expenses):
    output = format_table(expenses)
    assert output.count("\n") == 2
