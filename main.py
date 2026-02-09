from pawpal_system import CareTask, Pet, Owner, Scheduler


def main():
    # Create an owner
    owner = Owner(
        name="Sarah",
        available_minutes=120,
        preferences="Prefer outdoor activities in the morning"
    )

    # Create two pets
    dog = Pet(name="Max", species="Dog", age=3)
    cat = Pet(name="Whiskers", species="Cat", age=5)

    # Add tasks for the dog
    dog.add_task(CareTask(
        title="Morning walk",
        duration_minutes=30,
        priority=10,
        category="exercise",
        is_recurring=True
    ))
    dog.add_task(CareTask(
        title="Feed breakfast",
        duration_minutes=10,
        priority=9,
        category="feeding"
    ))
    dog.add_task(CareTask(
        title="Brush teeth",
        duration_minutes=5,
        priority=5,
        category="grooming"
    ))

    # Add tasks for the cat
    cat.add_task(CareTask(
        title="Feed breakfast",
        duration_minutes=5,
        priority=9,
        category="feeding"
    ))
    cat.add_task(CareTask(
        title="Clean litter box",
        duration_minutes=10,
        priority=8,
        category="hygiene"
    ))
    cat.add_task(CareTask(
        title="Play with toys",
        duration_minutes=15,
        priority=6,
        category="exercise"
    ))

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Get all tasks
    all_tasks = owner.get_all_tasks()

    # Create scheduler and generate plan
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, all_tasks)

    # Print Today's Schedule
    print("=" * 50)
    print(f"TODAY'S SCHEDULE FOR {owner.name.upper()}")
    print("=" * 50)
    print(f"Available time: {owner.available_minutes} minutes")
    print(f"Preferences: {owner.preferences}")
    print()

    total_time = 0
    for i, task in enumerate(plan, 1):
        print(f"{i}. {task.title}")
        print(f"   Duration: {task.duration_minutes} min | Priority: {task.priority} | Category: {task.category}")
        total_time += task.duration_minutes

    print()
    print(f"Total scheduled time: {total_time} minutes")
    print(f"Remaining time: {owner.available_minutes - total_time} minutes")
    print()
    print("SCHEDULER REASONING:")
    print(scheduler.explain_plan())
    print("=" * 50)


if __name__ == "__main__":
    main()
