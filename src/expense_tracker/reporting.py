"""Filtering, totals and formatting.

Every function here is pure: values in, values out, nothing printed and
nothing read from disk. That is what makes them straightforward to test.
"""

from collections import defaultdict

from .models import Expense


def filter_expenses(
    expenses: list[Expense],
    category: str | None = None,
    month: str | None = None,
) -> list[Expense]:
    """Filter by category and/or a YYYY-MM month string."""
    result = expenses
    if category:
        result = [e for e in result if e.category == category]
    if month:
        result = [e for e in result if e.date.isoformat().startswith(month)]
    return result


def total_paise(expenses: list[Expense]) -> int:
    return sum(e.amount_paise for e in expenses)


def by_category(expenses: list[Expense]) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for expense in expenses:
        totals[expense.category] += expense.amount_paise
    return dict(totals)


def format_table(expenses: list[Expense]) -> str:
    if not expenses:
        return "No expenses found."
    return "\n".join(
        f"  #{e.id:<4} {e.date}  {e.category:<10} "
        f"₹{e.rupees:>12,.2f}  {e.note}".rstrip()
        for e in expenses
    )
