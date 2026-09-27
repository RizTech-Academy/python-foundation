# Expense Tracker

The capstone project from the [RizTech Academy Python course](https://www.riztechacademy.com/learn/python-foundation).

Track personal expenses from the command line. Data is stored as JSON in your
home directory — no database, no account, no network, no dependencies outside
the standard library.

## This is reference code, not a starting point

The course walks you through building this in eight steps. **Build it yourself
first.** This repository is here for when you are stuck and want to compare, or
when you want to see the finished shape before starting.

Copying it will teach you very little. Typing it will teach you a lot.

## Setup

    git clone https://github.com/RizTech-Academy/python-foundation.git
    cd python-foundation
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -e ".[dev]"

## Usage

Record an expense:

    expenses add 250 food --note "lunch"

List them, optionally filtered:

    expenses list
    expenses list --category food
    expenses list --month 2026-09

See a breakdown:

    expenses summary

Delete one by id:

    expenses delete 1

Categories are `food`, `transport`, `rent` and `other`. Amounts are given in
rupees and stored internally as paise, so totals are exact.

## Where the data lives

`~/.expenses.json` by default. Override it with an environment variable, which
is also how the tests keep out of your real data:

    EXPENSES_FILE=/tmp/test.json expenses list

## Tests

    pytest

Twenty-five tests, all of which run without a database, a file fixture you have
to maintain, or any network access.

    ruff format .
    ruff check .

## What to look at

| File | Worth reading for |
|---|---|
| `models.py` | a frozen dataclass whose `__post_init__` makes an invalid expense impossible to create |
| `storage.py` | atomic writes — a crash part-way through cannot corrupt the file |
| `reporting.py` | pure functions: values in, values out, nothing printed |
| `cli.py` | the only module that prints, and one `try` that turns any `ValueError` into a message rather than a traceback |
| `tests/test_storage.py` | the most valuable test in the suite checks that corrupt data is never silently overwritten |

## Decisions the course explains

- **Money is an integer count of paise**, never a float. `₹250.00` is `25000`.
- **Dates are ISO strings** in JSON, because JSON has no date type.
- **`next_id` is stored** rather than computed, so a deleted id is never reused.
- **A corrupt data file raises** rather than returning empty, so the next save
  cannot destroy it.
- **Deleting does not decrement `next_id`.**

## Licence

MIT
