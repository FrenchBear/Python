# Example 5-13. dataclass/club_wrong.py: this class raises ValueError

from dataclasses import dataclass

@dataclass
class ClubMember:
    name: str
    guests: list = []
