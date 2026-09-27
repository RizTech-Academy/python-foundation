"""The Expense type and the rules an expense must obey."""

from dataclasses import dataclass
from datetime import date

VALID_CATEGORIES = ("food", "transport", "rent", "other")
MAX_NOTE_LENGTH = 200


@dataclass(frozen=True)
class Expense:
    """A single recorded expense. Amounts are stored in paise."""

    id: int
    amount_paise: int
    category: str
    date: date
    note: str = ""

    def __post_init__(self) -> None:
        if self.amount_paise <= 0:
            raise ValueError(
                f"amount must be positive, got {self.amount_paise / 100:.2f}"
            )
        if self.category not in VALID_CATEGORIES:
            raise ValueError(
                f"unknown category {self.category!r}. "
                f"Valid: {', '.join(VALID_CATEGORIES)}"
            )
        if len(self.note) > MAX_NOTE_LENGTH:
            raise ValueError(f"note must be {MAX_NOTE_LENGTH} characters or fewer")

    @property
    def rupees(self) -> float:
        """The amount in rupees, for display only."""
        return self.amount_paise / 100

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "amount_paise": self.amount_paise,
            "category": self.category,
            "date": self.date.isoformat(),
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            id=int(data["id"]),
            amount_paise=int(data["amount_paise"]),
            category=data["category"],
            date=date.fromisoformat(data["date"]),
            note=data.get("note", ""),
        )
