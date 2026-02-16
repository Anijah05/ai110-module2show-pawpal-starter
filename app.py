import streamlit as st
from pawpal_system import CareTask, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is an intelligent pet care planning assistant powered by a priority-based scheduling algorithm.
It helps busy pet owners optimize their daily care routines across multiple pets.

🧠 **Smart Features:**
- Priority-based task scheduling
- Automatic time budget optimization
- Multi-pet task aggregation
- Category-based filtering
- Recurring task management
"""
)

with st.expander("How it works", expanded=False):
    st.markdown(
        """
### Intelligent Scheduling Algorithm

**PawPal+** uses a sophisticated priority-based scheduler that:

1. **Aggregates** tasks from all your pets
2. **Filters** tasks based on your constraints (category, preferences)
3. **Prioritizes** urgent and important tasks first (1-10 scale)
4. **Optimizes** task selection to fit your available time budget
5. **Explains** its reasoning for each scheduling decision

### System Architecture

- **CareTask**: Represents individual pet care activities with priority, duration, and completion tracking
- **Pet**: Manages multiple tasks per pet with add/edit capabilities
- **Owner**: Aggregates tasks across all pets with preference management
- **Scheduler**: The "brain" that generates optimized daily plans with explainable reasoning
"""
    )

st.divider()

# Initialize session state for Owner if it doesn't exist
if "owner" not in st.session_state:
    st.session_state.owner = None

if "current_pet" not in st.session_state:
    st.session_state.current_pet = None

# Step 1: Create Owner Profile
st.subheader("👤 Owner Profile")
if st.session_state.owner is None:
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name", value="Jordan")
        available_minutes = st.number_input(
            "Available minutes per day", min_value=30, max_value=480, value=120
        )
        preferences = st.text_area(
            "Care preferences (optional)",
            placeholder="e.g., Prefer outdoor activities in the morning"
        )

        if st.form_submit_button("Create Owner Profile"):
            st.session_state.owner = Owner(
                name=owner_name,
                available_minutes=available_minutes,
                preferences=preferences if preferences else None
            )
            st.success(f"✅ Owner profile created for {owner_name}!")
            st.rerun()
else:
    owner = st.session_state.owner
    st.info(f"**Owner:** {owner.name} | **Available time:** {owner.available_minutes} min/day")
    if owner.preferences:
        st.caption(f"Preferences: {owner.preferences}")

    if st.button("Reset Owner"):
        st.session_state.owner = None
        st.session_state.current_pet = None
        st.rerun()

st.divider()

# Step 2: Add Pets
if st.session_state.owner is not None:
    st.subheader("🐾 Add Pets")

    with st.form("pet_form"):
        pet_name = st.text_input("Pet name", value="Mochi")
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

        if st.form_submit_button("Add Pet"):
            new_pet = Pet(name=pet_name, species=species, age=age)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"✅ Added {pet_name} the {species}!")
            st.rerun()

    # Display existing pets
    if st.session_state.owner.pets:
        st.markdown("### Your Pets")
        for i, pet in enumerate(st.session_state.owner.pets):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{pet.name}** ({pet.species}, {pet.age} years old) - {len(pet.tasks)} tasks")
            with col2:
                if st.button(f"Select", key=f"select_pet_{i}"):
                    st.session_state.current_pet = pet
                    st.rerun()
    else:
        st.info("No pets added yet. Create one above!")

    st.divider()

    # Step 3: Add Tasks to Selected Pet
    if st.session_state.current_pet is not None:
        current_pet = st.session_state.current_pet
        st.subheader(f"📋 Tasks for {current_pet.name}")

        with st.form("task_form"):
            st.caption("Add a care task")
            col1, col2 = st.columns(2)
            with col1:
                task_title = st.text_input("Task title", value="Morning walk")
                duration = st.number_input("Duration (minutes)", min_value=5, max_value=240, value=20)
            with col2:
                category = st.selectbox("Category", ["feeding", "exercise", "grooming", "hygiene", "play", "medical"])
                priority = st.slider("Priority", min_value=1, max_value=10, value=5)

            is_recurring = st.checkbox("Recurring task", value=False)

            if st.form_submit_button("Add Task"):
                new_task = CareTask(
                    title=task_title,
                    duration_minutes=int(duration),
                    priority=priority,
                    category=category,
                    is_recurring=is_recurring
                )
                current_pet.add_task(new_task)
                st.success(f"✅ Added task: {task_title}")
                st.rerun()

        # Display tasks for current pet
        if current_pet.tasks:
            st.markdown("#### Current Tasks")
            for task in current_pet.tasks:
                status = "✅" if task.is_completed else "⏳"
                recurring = "🔄" if task.is_recurring else ""
                st.write(
                    f"{status} {recurring} **{task.title}** - {task.duration_minutes} min "
                    f"| Priority: {task.priority} | Category: {task.category}"
                )
        else:
            st.info(f"No tasks for {current_pet.name} yet.")

        st.divider()

    # Step 4: Generate Schedule
    st.subheader("📅 Generate Daily Schedule")

    scheduler_constraints = st.text_input(
        "Scheduler constraints (optional)",
        placeholder="e.g., category:exercise"
    )

    if st.button("🎯 Generate Optimized Schedule"):
        if not st.session_state.owner.pets:
            st.error("Please add at least one pet first!")
        else:
            # Get all tasks from all pets
            all_tasks = st.session_state.owner.get_all_tasks()

            if not all_tasks:
                st.warning("No tasks found. Please add tasks to your pets first!")
            else:
                # Create scheduler and generate plan
                scheduler = Scheduler(
                    constraints=scheduler_constraints if scheduler_constraints else None
                )
                plan = scheduler.generate_plan(st.session_state.owner, all_tasks)

                # Calculate task statistics
                total_time = sum(task.duration_minutes for task in plan)
                remaining_time = st.session_state.owner.available_minutes - total_time
                excluded_tasks = [task for task in all_tasks if task.is_due() and task not in plan]

                # Display the schedule
                st.success("✅ Schedule Generated!")

                # Show warnings if tasks were excluded
                if excluded_tasks:
                    st.warning(
                        f"⚠️ **{len(excluded_tasks)} task(s) couldn't fit in your time budget** "
                        f"and were excluded from today's schedule."
                    )
                    with st.expander("View excluded tasks"):
                        for task in excluded_tasks:
                            st.write(f"• **{task.title}** ({task.duration_minutes} min, Priority: {task.priority})")

                st.markdown("### 📋 Today's Optimized Schedule")

                if plan:
                    # Display tasks in a table format
                    for i, task in enumerate(plan, 1):
                        # Priority color coding
                        if task.priority >= 8:
                            priority_badge = "🔴 HIGH"
                        elif task.priority >= 5:
                            priority_badge = "🟡 MEDIUM"
                        else:
                            priority_badge = "🟢 LOW"

                        recurring_badge = "🔄 Recurring" if task.is_recurring else ""

                        with st.container():
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"**{i}. {task.title}** {recurring_badge}")
                                st.caption(f"Category: {task.category}")
                            with col2:
                                st.write(f"⏱️ {task.duration_minutes} min")
                            with col3:
                                st.write(f"{priority_badge}")
                            st.divider()
                else:
                    st.info("No tasks fit within your available time budget.")

                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tasks scheduled", f"{len(plan)}/{len(all_tasks)}")
                with col2:
                    st.metric("Total time", f"{total_time} min")
                with col3:
                    if remaining_time >= 0:
                        st.metric("Free time", f"{remaining_time} min", delta="Available")
                    else:
                        st.metric("Over budget", f"{abs(remaining_time)} min", delta="Exceeded", delta_color="inverse")

                # Display reasoning
                with st.expander("🧠 Scheduler Reasoning & Algorithm Details"):
                    st.write(scheduler.explain_plan())
                    st.markdown("---")
                    st.markdown("""
                    **Algorithm:** Priority-Based Greedy Scheduler
                    - Sorts tasks by priority (descending)
                    - Selects tasks that fit within time budget
                    - Excludes completed non-recurring tasks
                    - Applies user-defined constraints
                    """)
else:
    st.info("👆 Create an owner profile to get started!")
