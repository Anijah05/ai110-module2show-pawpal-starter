"""Tests for PawPal system functionality."""

import pytest
from pawpal_system import CareTask, Pet, Owner, Scheduler


def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    # Create a task
    task = CareTask(
        title="Feed dog",
        duration_minutes=10,
        priority=8,
        category="feeding"
    )

    # Initially, task should not be completed
    assert task.is_completed is False

    # Mark task as complete
    task.mark_complete()

    # Verify task is now completed
    assert task.is_completed is True


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Create a pet
    pet = Pet(name="Buddy", species="Dog", age=2)

    # Initially, pet should have no tasks
    assert len(pet.get_tasks()) == 0

    # Create and add first task
    task1 = CareTask(
        title="Morning walk",
        duration_minutes=30,
        priority=9,
        category="exercise"
    )
    pet.add_task(task1)

    # Verify pet now has 1 task
    assert len(pet.get_tasks()) == 1

    # Add second task
    task2 = CareTask(
        title="Feed breakfast",
        duration_minutes=10,
        priority=10,
        category="feeding"
    )
    pet.add_task(task2)

    # Verify pet now has 2 tasks
    assert len(pet.get_tasks()) == 2

    # Verify the tasks are the ones we added
    tasks = pet.get_tasks()
    assert task1 in tasks
    assert task2 in tasks
