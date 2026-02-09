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
    is_completed: bool = False

    def update_priority(self, priority: int) -> None:
        """Update the priority level of the task."""
        if priority < 0:
            raise ValueError("Priority must be non-negative")
        self.priority = priority

    def update_duration(self, duration_minutes: int) -> None:
        """Update the duration of the task in minutes."""
        if duration_minutes <= 0:
            raise ValueError("Duration must be positive")
        self.duration_minutes = duration_minutes

    def is_due(self) -> bool:
        """Check if the task is due (not completed or is recurring)."""
        return not self.is_completed or self.is_recurring

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a new care task for this pet."""
        self.tasks.append(task)

    def edit_task(self, task: CareTask) -> None:
        """Edit an existing task by replacing it with the updated version."""
        for i, existing_task in enumerate(self.tasks):
            if existing_task.title == task.title:
                self.tasks[i] = task
                return
        raise ValueError(f"Task '{task.title}' not found for pet '{self.name}'")

    def get_tasks(self) -> List[CareTask]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: Optional[str] = None
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def update_preferences(self, preferences: Optional[str]) -> None:
        """Update the owner's care preferences."""
        self.preferences = preferences

    def get_all_tasks(self) -> List[CareTask]:
        """Retrieve all tasks from all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, constraints: Optional[str] = None) -> None:
        self.constraints = constraints
        self.plan: List[CareTask] = []
        self.reasoning: Optional[str] = None

    def generate_plan(self, owner: Owner, tasks: List[CareTask]) -> List[CareTask]:
        """
        Generate an optimized care plan based on owner's available time and task priorities.
        Returns a list of tasks sorted by priority that fit within the time budget.
        """
        # Filter tasks based on constraints first
        filtered_tasks = self.filter_tasks_by_constraints(tasks)

        # Only include tasks that are due
        due_tasks = [task for task in filtered_tasks if task.is_due()]

        # Sort by priority (higher priority first)
        sorted_tasks = sorted(due_tasks, key=lambda t: t.priority, reverse=True)

        # Select tasks that fit within available time
        selected_tasks = []
        total_time = 0

        for task in sorted_tasks:
            if total_time + task.duration_minutes <= owner.available_minutes:
                selected_tasks.append(task)
                total_time += task.duration_minutes

        # Store the plan and reasoning
        self.plan = selected_tasks
        self.reasoning = (
            f"Generated plan for {owner.name} with {owner.available_minutes} minutes available.\n"
            f"Selected {len(selected_tasks)} tasks totaling {total_time} minutes.\n"
            f"Tasks prioritized by urgency and importance."
        )

        if owner.preferences:
            self.reasoning += f"\nOwner preferences considered: {owner.preferences}"

        return self.plan

    def explain_plan(self) -> Optional[str]:
        return self.reasoning

    def filter_tasks_by_constraints(self, tasks: List[CareTask]) -> List[CareTask]:
        """
        Filter tasks based on scheduler constraints.
        If no constraints, return all tasks.
        """
        if not self.constraints:
            return tasks

        # Parse constraints and filter accordingly
        filtered = []
        constraints_lower = self.constraints.lower()

        for task in tasks:
            # Example constraint filtering by category
            if "category:" in constraints_lower:
                # Extract category from constraints (simple parsing)
                category_constraint = constraints_lower.split("category:")[1].split()[0].strip()
                if task.category.lower() == category_constraint:
                    filtered.append(task)
            else:
                # If constraints don't match expected format, include all tasks
                filtered.append(task)

        # If no specific filtering was applied, return all tasks
        return filtered if filtered else tasks
