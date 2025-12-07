from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime

@dataclass
class Grade:
    value: int
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

@dataclass
class Student:
    name: str
    age: int
    id: str
    courses: List[str] = field(default_factory=list)
    grades: Dict[str, List[Grade]] = field(default_factory=dict)

@dataclass
class Course:
    title: str
    id: str
    students: List[str] = field(default_factory=list)