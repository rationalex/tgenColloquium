from dataclasses import dataclass
from typing import List


@dataclass
class Problem:
    name: str
    short_name: str


@dataclass
class Contest:
    name: str
    problems: List[Problem]


@dataclass()
class Participant:
    name: str
    user_id: int


@dataclass
class Standings:
    contests: List[Contest]
    Participants: List[Participant]
