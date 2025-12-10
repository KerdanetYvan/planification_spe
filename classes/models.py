# classes/models.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass(frozen=True)
class TimeSlot:
    index: int          # 0..4
    label: str          # ex: "09:00-09:25"

@dataclass
class Assignment:
    specialty: str
    timeslot: TimeSlot
    group_index: int    # 0-based (groupe 1 => 0, etc.)

@dataclass
class Student:
    name: str
    classe: str
    choices: List[str]                  # liste de spé demandées
    assignments: Dict[int, Assignment] = field(default_factory=dict)
    # key = timeslot.index

    def add_assignment(self, assignment: Assignment) -> None:
        """Ajoute une affectation pour l'élève sur un créneau donné."""
        self.assignments[assignment.timeslot.index] = assignment

@dataclass
class GroupRecord:
    """Vue 'par groupe' pour l'affichage / export."""
    specialty: str
    timeslot: TimeSlot
    group_index: int
    student_name: str
    classe: str

@dataclass
class UnplacedStudent:
    """Information sur un élève qui n'a pas pu être placé."""
    student: Student
    failed_specialty: str  # La spécialité qui n'a pas pu être placée
    reason: str           # La raison de l'échec
