# Example 5-15. dataclass/club_generic.py: this ClubMember definition is more precise

from dataclasses import dataclass, field

@dataclass
class ClubMember:
    name: str
    guests: list[str] = field(default_factory=list)
