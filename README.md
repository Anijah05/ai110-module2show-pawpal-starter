# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

### 🧠 Intelligent Scheduling Algorithm

- **Priority-Based Scheduling**: Tasks are automatically sorted by urgency (1-10 scale) to ensure critical care activities happen first
- **Time Budget Optimization**: Greedy algorithm selects maximum value tasks that fit within your available daily minutes
- **Constraint Filtering**: Filter schedules by category (feeding, exercise, grooming, hygiene, play, medical)
- **Multi-Pet Task Aggregation**: Seamlessly manages care tasks across multiple pets in one unified schedule

### 📋 Task Management

- **Recurring Tasks**: Mark tasks as recurring to keep them in the schedule even after completion
- **Completion Tracking**: Track which tasks are done with automatic exclusion from future schedules
- **Task Editing**: Update priority and duration dynamically as needs change
- **Category Organization**: Organize tasks by care type for better filtering and analysis

### 👥 Owner & Pet Profiles

- **Owner Preferences**: Set care preferences that influence scheduling decisions
- **Available Time Management**: Define daily time budget to get realistic schedules
- **Multi-Pet Support**: Add unlimited pets with individual task lists
- **Pet Details**: Track name, species, and age for each pet

### 🎯 Smart Warnings & Insights

- **Excluded Task Warnings**: Get notified when tasks don't fit in your time budget
- **Priority Indicators**: Visual color-coding for high/medium/low priority tasks
- **Scheduler Reasoning**: Detailed explanations of why tasks were selected and ordered
- **Time Metrics**: Real-time display of scheduled time, remaining time, and task counts

### 🔬 Robust Testing

- **19 Automated Tests**: Comprehensive test suite covering all core functionality
- **100% Pass Rate**: All tests passing with edge case coverage
- **Input Validation**: Protection against invalid data (negative priorities, zero durations)
- **Constraint Testing**: Verified filtering and scheduling logic

## 📸 Demo

### Main Interface
*Screenshot coming soon - Run `streamlit run app.py` to see the live interface*

### Key Screens
1. **Owner Profile Setup**: Create your profile with time availability and preferences
2. **Pet Management**: Add multiple pets and select which one to manage
3. **Task Creation**: Add care tasks with priority, duration, category, and recurrence
4. **Optimized Schedule**: View your daily schedule with priority indicators and reasoning

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Project Structure

```
pawpal-starter/
├── app.py                 # Streamlit UI
├── pawpal_system.py       # Core business logic (CareTask, Pet, Owner, Scheduler)
├── main.py               # Terminal testing script
├── tests/
│   └── test_pawpal.py    # Comprehensive test suite
├── uml_diagram.md        # System architecture documentation
├── reflection.md         # Development reflection
└── README.md            # This file
```

### Development Workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

### Running Tests

The project includes a comprehensive test suite covering all core functionality:

```bash
python -m pytest tests/test_pawpal.py -v
```

For a quick summary:
```bash
python -m pytest
```

### Test Coverage

The test suite includes **19 tests** covering:

1. **Task Completion & Due Status** - Verifies task completion logic and recurring task behavior
2. **Task Addition** - Ensures tasks are properly added to pets
3. **Priority-Based Sorting** - Confirms scheduler sorts tasks by priority (highest first)
4. **Time Budget Constraints** - Validates scheduler respects owner's available time
5. **Multi-Pet Task Aggregation** - Tests task collection across multiple pets
6. **Input Validation** - Checks error handling for invalid inputs (negative priority, invalid duration)
7. **Constraint Filtering** - Verifies category-based task filtering
8. **Scheduler Reasoning** - Ensures scheduler provides explanation for generated plans
9. **Completed Task Exclusion** - Confirms non-recurring completed tasks are excluded from schedules

### Edge Cases Tested

- Empty task lists
- Tasks with equal priorities
- Tasks that exceed available time budget
- Owners with no pets
- Pets with no tasks
- Non-existent task editing
- Constraint filtering with no matches

### Confidence Level

⭐⭐⭐⭐⭐ **5/5 Stars**

The system demonstrates high reliability with:
- ✅ 100% test pass rate (19/19 tests)
- ✅ Comprehensive coverage of happy paths and edge cases
- ✅ Robust input validation
- ✅ Proper handling of time constraints and priorities
- ✅ Correct filtering and aggregation logic
- ✅ Clear separation of concerns (data model, business logic, UI)

The PawPal+ system is production-ready for pet care scheduling with confidence in its scheduling algorithm, error handling, and multi-pet task management capabilities.
