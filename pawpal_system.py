from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: int
    category: str
    is_recurring: bool = False

    def update_priority(self, priority: int) -> None:
        pass

    def update_duration(self, duration_minutes: int) -> None:
        pass

    def is_due(self) -> bool:
        return False


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        pass

    def edit_task(self, task: CareTask) -> None:
        pass

    def get_tasks(self) -> List[CareTask]:
        return []


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: Optional[str] = None
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def update_preferences(self, preferences: Optional[str]) -> None:
        pass

    def get_all_tasks(self) -> List[CareTask]:
        return []


class Scheduler:
    def __init__(self, constraints: Optional[str] = None) -> None:
        self.constraints = constraints
        self.plan: List[CareTask] = []
        self.reasoning: Optional[str] = None

    def generate_plan(self, owner: Owner, tasks: List[CareTask]) -> List[CareTask]:
        return []

    def explain_plan(self) -> Optional[str]:
        return self.reasoning

    def filter_tasks_by_constraints(self, tasks: List[CareTask]) -> List[CareTask]:
        return []
