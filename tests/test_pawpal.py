"""Comprehensive test suite for PawPal+ system."""

import pytest
from pawpal_system import CareTask, Pet, Owner, Scheduler


# ===== Test 1: Task Completion and Due Status =====

def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    task = CareTask(
        title="Feed dog",
        duration_minutes=10,
        priority=8,
        category="feeding"
    )

    assert task.is_completed is False
    assert task.is_due() is True

    task.mark_complete()

    assert task.is_completed is True
    assert task.is_due() is False  # Non-recurring task should not be due after completion


def test_recurring_task_stays_due():
    """Verify that recurring tasks remain due even after completion."""
    task = CareTask(
        title="Morning walk",
        duration_minutes=30,
        priority=9,
        category="exercise",
        is_recurring=True
    )

    assert task.is_due() is True

    task.mark_complete()

    # Recurring task should still be "due" even when marked complete
    assert task.is_completed is True
    assert task.is_due() is True


# ===== Test 2: Task Addition to Pets =====

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Buddy", species="Dog", age=2)

    assert len(pet.get_tasks()) == 0

    task1 = CareTask(
        title="Morning walk",
        duration_minutes=30,
        priority=9,
        category="exercise"
    )
    pet.add_task(task1)

    assert len(pet.get_tasks()) == 1

    task2 = CareTask(
        title="Feed breakfast",
        duration_minutes=10,
        priority=10,
        category="feeding"
    )
    pet.add_task(task2)

    assert len(pet.get_tasks()) == 2

    tasks = pet.get_tasks()
    assert task1 in tasks
    assert task2 in tasks


# ===== Test 3: Priority-Based Sorting =====

def test_priority_sorting():
    """Verify that scheduler sorts tasks by priority (highest first)."""
    owner = Owner(name="Alex", available_minutes=100)
    pet = Pet(name="Max", species="Dog", age=4)

    # Add tasks with different priorities
    task_low = CareTask(title="Brush fur", duration_minutes=10, priority=3, category="grooming")
    task_high = CareTask(title="Give medicine", duration_minutes=5, priority=10, category="medical")
    task_medium = CareTask(title="Play fetch", duration_minutes=20, priority=6, category="play")

    pet.add_task(task_low)
    pet.add_task(task_high)
    pet.add_task(task_medium)

    owner.add_pet(pet)

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    # Verify tasks are sorted by priority (highest first)
    assert len(plan) == 3
    assert plan[0].title == "Give medicine"  # Priority 10
    assert plan[1].title == "Play fetch"      # Priority 6
    assert plan[2].title == "Brush fur"       # Priority 3


def test_sorting_with_equal_priorities():
    """Verify scheduler handles tasks with equal priorities."""
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Mochi", species="Cat", age=2)

    task1 = CareTask(title="Task A", duration_minutes=10, priority=5, category="feeding")
    task2 = CareTask(title="Task B", duration_minutes=10, priority=5, category="feeding")
    task3 = CareTask(title="Task C", duration_minutes=10, priority=8, category="feeding")

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    owner.add_pet(pet)

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    # Task C should be first (highest priority)
    assert plan[0].priority == 8
    # Tasks A and B should both be included (same priority)
    assert len(plan) == 3


# ===== Test 4: Time Budget Constraints =====

def test_time_budget_respected():
    """Verify scheduler respects owner's available time budget."""
    owner = Owner(name="Sam", available_minutes=60)
    pet = Pet(name="Rocky", species="Dog", age=5)

    # Add tasks totaling 100 minutes (exceeds 60 minute budget)
    task1 = CareTask(title="Long walk", duration_minutes=45, priority=10, category="exercise")
    task2 = CareTask(title="Grooming", duration_minutes=30, priority=8, category="grooming")
    task3 = CareTask(title="Play time", duration_minutes=25, priority=6, category="play")

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    owner.add_pet(pet)

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    # Calculate total time in plan
    total_time = sum(task.duration_minutes for task in plan)

    # Should not exceed available time
    assert total_time <= owner.available_minutes

    # Should include high priority tasks first
    assert plan[0].title == "Long walk"  # Priority 10, 45 min fits in 60 min budget
    # Grooming (30 min) would make total 75 min, exceeding 60 min budget
    # Only one task should fit
    assert len(plan) == 1


def test_exact_time_budget():
    """Verify scheduler handles tasks that exactly match available time."""
    owner = Owner(name="Taylor", available_minutes=60)
    pet = Pet(name="Luna", species="Cat", age=3)

    task1 = CareTask(title="Task 1", duration_minutes=30, priority=10, category="feeding")
    task2 = CareTask(title="Task 2", duration_minutes=30, priority=9, category="play")

    pet.add_task(task1)
    pet.add_task(task2)

    owner.add_pet(pet)

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    total_time = sum(task.duration_minutes for task in plan)

    assert total_time == 60
    assert len(plan) == 2


def test_all_tasks_exceed_budget():
    """Verify scheduler handles case where single tasks exceed budget."""
    owner = Owner(name="Chris", available_minutes=30)
    pet = Pet(name="Bear", species="Dog", age=6)

    # All tasks individually exceed budget
    task1 = CareTask(title="Long activity", duration_minutes=45, priority=10, category="exercise")
    task2 = CareTask(title="Another long task", duration_minutes=40, priority=9, category="grooming")

    pet.add_task(task1)
    pet.add_task(task2)

    owner.add_pet(pet)

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    # Should return empty plan if no tasks fit
    assert len(plan) == 0


# ===== Test 5: Multi-Pet Task Aggregation =====

def test_multi_pet_task_aggregation():
    """Verify owner.get_all_tasks() aggregates tasks from all pets."""
    owner = Owner(name="Jamie", available_minutes=120)

    dog = Pet(name="Rex", species="Dog", age=4)
    cat = Pet(name="Mittens", species="Cat", age=2)
    bird = Pet(name="Tweety", species="Bird", age=1)

    dog.add_task(CareTask(title="Walk dog", duration_minutes=30, priority=9, category="exercise"))
    dog.add_task(CareTask(title="Feed dog", duration_minutes=10, priority=10, category="feeding"))

    cat.add_task(CareTask(title="Feed cat", duration_minutes=5, priority=10, category="feeding"))
    cat.add_task(CareTask(title="Clean litter", duration_minutes=10, priority=8, category="hygiene"))

    bird.add_task(CareTask(title="Feed bird", duration_minutes=5, priority=9, category="feeding"))

    owner.add_pet(dog)
    owner.add_pet(cat)
    owner.add_pet(bird)

    all_tasks = owner.get_all_tasks()

    # Should have 5 tasks total
    assert len(all_tasks) == 5

    # Verify tasks from all pets are included
    task_titles = [task.title for task in all_tasks]
    assert "Walk dog" in task_titles
    assert "Feed cat" in task_titles
    assert "Feed bird" in task_titles


def test_owner_with_no_pets():
    """Verify owner with no pets returns empty task list."""
    owner = Owner(name="Alex", available_minutes=100)

    all_tasks = owner.get_all_tasks()

    assert len(all_tasks) == 0


def test_pets_with_no_tasks():
    """Verify pets without tasks don't break aggregation."""
    owner = Owner(name="Morgan", available_minutes=100)

    pet1 = Pet(name="Pet1", species="Dog", age=3)
    pet2 = Pet(name="Pet2", species="Cat", age=2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    all_tasks = owner.get_all_tasks()

    assert len(all_tasks) == 0


# ===== Test 6: Input Validation =====

def test_invalid_priority():
    """Verify that negative priority raises ValueError."""
    task = CareTask(title="Test", duration_minutes=10, priority=5, category="feeding")

    with pytest.raises(ValueError, match="Priority must be non-negative"):
        task.update_priority(-1)


def test_invalid_duration():
    """Verify that zero or negative duration raises ValueError."""
    task = CareTask(title="Test", duration_minutes=10, priority=5, category="feeding")

    with pytest.raises(ValueError, match="Duration must be positive"):
        task.update_duration(0)

    with pytest.raises(ValueError, match="Duration must be positive"):
        task.update_duration(-10)


def test_edit_nonexistent_task():
    """Verify that editing a non-existent task raises ValueError."""
    pet = Pet(name="Buddy", species="Dog", age=3)

    task = CareTask(title="Nonexistent", duration_minutes=10, priority=5, category="feeding")

    with pytest.raises(ValueError, match="Task 'Nonexistent' not found"):
        pet.edit_task(task)


# ===== Test 7: Constraint Filtering =====

def test_category_constraint_filtering():
    """Verify scheduler filters tasks by category constraint."""
    owner = Owner(name="Pat", available_minutes=100)
    pet = Pet(name="Spot", species="Dog", age=4)

    task1 = CareTask(title="Walk", duration_minutes=30, priority=9, category="exercise")
    task2 = CareTask(title="Feed", duration_minutes=10, priority=10, category="feeding")
    task3 = CareTask(title="Play", duration_minutes=20, priority=8, category="exercise")

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    owner.add_pet(pet)

    # Filter only exercise tasks
    scheduler = Scheduler(constraints="category:exercise")
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    # Should only include exercise tasks
    assert len(plan) == 2
    assert all(task.category == "exercise" for task in plan)
    assert plan[0].title == "Walk"   # Priority 9
    assert plan[1].title == "Play"   # Priority 8


def test_no_constraints():
    """Verify scheduler with no constraints includes all tasks."""
    owner = Owner(name="River", available_minutes=100)
    pet = Pet(name="Fluffy", species="Cat", age=2)

    task1 = CareTask(title="Task 1", duration_minutes=10, priority=9, category="feeding")
    task2 = CareTask(title="Task 2", duration_minutes=10, priority=8, category="play")

    pet.add_task(task1)
    pet.add_task(task2)

    owner.add_pet(pet)

    scheduler = Scheduler()  # No constraints
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    assert len(plan) == 2


def test_constraint_no_matching_tasks():
    """Verify scheduler returns empty plan when no tasks match constraint."""
    owner = Owner(name="Casey", available_minutes=100)
    pet = Pet(name="Whiskers", species="Cat", age=3)

    task1 = CareTask(title="Feed", duration_minutes=10, priority=10, category="feeding")

    pet.add_task(task1)
    owner.add_pet(pet)

    # Look for exercise tasks (none exist)
    scheduler = Scheduler(constraints="category:exercise")
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    assert len(plan) == 0


# ===== Test 8: Scheduler Reasoning =====

def test_scheduler_explains_plan():
    """Verify scheduler provides reasoning for generated plan."""
    owner = Owner(name="Drew", available_minutes=60, preferences="Morning walks preferred")
    pet = Pet(name="Buddy", species="Dog", age=3)

    task = CareTask(title="Walk", duration_minutes=30, priority=10, category="exercise")
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler()
    scheduler.generate_plan(owner, owner.get_all_tasks())

    reasoning = scheduler.explain_plan()

    assert reasoning is not None
    assert "Drew" in reasoning
    assert "60 minutes" in reasoning
    assert "Morning walks preferred" in reasoning


# ===== Test 9: Completed Tasks Excluded from Schedule =====

def test_completed_tasks_excluded():
    """Verify completed non-recurring tasks are excluded from schedule."""
    owner = Owner(name="Avery", available_minutes=100)
    pet = Pet(name="Max", species="Dog", age=4)

    task1 = CareTask(title="Task 1", duration_minutes=20, priority=10, category="feeding")
    task2 = CareTask(title="Task 2", duration_minutes=20, priority=9, category="play")

    # Mark task1 as complete
    task1.mark_complete()

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, owner.get_all_tasks())

    # Only task2 should be in the plan (task1 is completed and not recurring)
    assert len(plan) == 1
    assert plan[0].title == "Task 2"
