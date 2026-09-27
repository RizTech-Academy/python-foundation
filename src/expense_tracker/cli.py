"""Command-line interface.

This is the only module that prints. Everything else returns values, which
is what keeps the rest of the program testable.
"""

import argparse
import sys
from datetime import date

from .models import VALID_CATEGORIES, Expense
from .reporting import by_category, filter_expenses, format_table, total_paise
from .storage import data_file, load, save


def cmd_add(args: argparse.Namespace) -> int:
    path = data_file()
    expenses, next_id = load(path)

    expense = Expense(
        id=next_id,
        amount_paise=round(args.amount * 100),
        category=args.category,
        date=date.today(),
        note=args.note or "",
    )

    expenses.append(expense)
    save(path, expenses, next_id + 1)

    suffix = f" ({expense.note})" if expense.note else ""
    print(f"Added #{expense.id}: {expense.category} ₹{expense.rupees:,.2f}{suffix}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    expenses, _ = load(data_file())
    matching = filter_expenses(expenses, category=args.category, month=args.month)
    print(format_table(matching))
    return 0


def cmd_summary(_: argparse.Namespace) -> int:
    expenses, _unused = load(data_file())

    if not expenses:
        print("No expenses recorded yet. Add one with: expenses add 250 food")
        return 0

    total = total_paise(expenses)
    print(f"Total:        ₹{total / 100:,.2f}\n")

    ordered = sorted(
        by_category(expenses).items(), key=lambda pair: pair[1], reverse=True
    )
    for category, amount in ordered:
        share = amount / total * 100
        print(f"  {category:<10} ₹{amount / 100:>12,.2f}   ({share:.1f}%)")

    months = {e.date.isoformat()[:7] for e in expenses}
    average = total / 100 / len(months)
    print(f"\nAcross {len(months)} month(s) — average ₹{average:,.2f}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    path = data_file()
    expenses, next_id = load(path)

    match = next((e for e in expenses if e.id == args.id), None)
    if match is None:
        raise ValueError(
            f"no expense with id {args.id}. Run 'expenses list' to see ids."
        )

    expenses.remove(match)
    # next_id is not decremented: ids are never reused.
    save(path, expenses, next_id)
    print(f"Deleted #{match.id}: {match.category} ₹{match.rupees:,.2f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expenses",
        description="Track personal expenses from the command line.",
        epilog="Data is stored in ~/.expenses.json (override with EXPENSES_FILE).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="record a new expense")
    add.add_argument("amount", type=float, help="amount in rupees, e.g. 250.50")
    add.add_argument("category", choices=VALID_CATEGORIES, help="expense category")
    add.add_argument("--note", default="", help="optional description")
    add.set_defaults(func=cmd_add)

    listing = sub.add_parser("list", help="list expenses")
    listing.add_argument("--category", choices=VALID_CATEGORIES)
    listing.add_argument("--month", help="filter by month, e.g. 2026-09")
    listing.set_defaults(func=cmd_list)

    summary = sub.add_parser("summary", help="totals and a category breakdown")
    summary.set_defaults(func=cmd_summary)

    delete = sub.add_parser("delete", help="delete an expense by id")
    delete.add_argument("id", type=int, help="the id shown by 'expenses list'")
    delete.set_defaults(func=cmd_delete)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
