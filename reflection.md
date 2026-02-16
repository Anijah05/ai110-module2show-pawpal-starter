# PawPal+ Project Reflection

## 1. System Design

Core user actions

- Add a pet and owner profile with basic details.
- Create or edit care tasks with duration and priority.
- Generate and view a daily care plan based on constraints.

a. Initial design

I designed four classes: Owner, Pet, CareTask, and Scheduler. The Owner class stores owner info, preferences, and a list of pets, and can add pets and aggregate tasks across all pets. The Pet class stores pet details and a list of tasks, and can add or edit those tasks. The CareTask class represents a single care activity with duration, priority, category, and recurrence metadata. The Scheduler class takes tasks plus constraints and produces a daily plan along with reasoning.

b. Design changes

My design definitely changed during implementation. The most significant addition was the is_completed field to CareTask. I hadn't originally planned for this, but once I started writing the is_due() method, I realized I needed a way to track task completion. The interesting challenge was making recurring tasks stay "due" even after being marked complete, since tasks like feeding happen every day and shouldn't disappear from future schedules.

Another change was fixing a bug in the constraint filtering logic. My initial implementation would return all tasks when no matches were found for a category filter. For example, if you searched for "exercise" tasks but only had "feeding" tasks, it would show everything rather than an empty list. That didn't make sense, so I revised it to return an empty list when there are no matches, which is much more intuitive.

I also added a mark_complete() method rather than having users directly modify the is_completed field. This encapsulation made the code cleaner and easier to test, and it felt like the right way to handle state changes in the task objects.

Finally, I streamlined how the scheduler generates reasoning. Instead of requiring a separate method call, the reasoning is now automatically generated and stored as part of generate_plan(). It seemed silly to make reasoning optional when transparency about scheduling decisions is such an important feature.

---

## 2. Scheduling Logic and Tradeoffs

a. Constraints and priorities

The scheduler considers three main constraints. First is the time budget, which is a hard constraint. Tasks must fit within the owner's available_minutes, and this is enforced strictly - any task that would cause the schedule to exceed the budget gets excluded. I made this strict because you can't create more time in a day, so it represents a real physical limit.

Second is task priority, which works as the optimization criterion. Tasks are sorted by priority on a 1-10 scale in descending order, so higher priority tasks get scheduled first. This ensures critical activities like medication or feeding happen before optional activities like extra playtime.

Third is category filtering, which is an optional constraint. Users can filter by category (feeding, exercise, grooming, etc.) to focus on specific types of care if they want to.

I decided time budget and priority were most critical because they reflect real constraints that pet owners face. Time is genuinely finite - people have work, other obligations, and can't just spend unlimited time on pet care. Priority matters because some tasks really are more urgent than others. Giving medicine can't wait, but brushing fur can happen tomorrow if needed. Category filtering adds useful flexibility without overcomplicating the core algorithm.

b. Tradeoffs

The main tradeoff I made was choosing a greedy algorithm over an optimal scheduling solution. My scheduler selects the highest priority tasks that fit in the time budget, one by one. This isn't mathematically optimal - there could be cases where selecting multiple lower-priority tasks would give you more "total value" than fewer high-priority ones. A dynamic programming approach could theoretically find the perfect combination of tasks to maximize total priority within the time constraint.

However, I think the greedy approach is the right choice for this scenario. First, it's simple and fast with O(n log n) time complexity, which means it'll work smoothly even with many tasks. Second, it's transparent - users can easily understand why tasks were selected or excluded, which builds trust in the system. Third, it matches how people actually think about pet care. Pet owners don't think about maximizing total priority points; they think "I need to give medicine first, then feed them, then everything else." The greedy approach mirrors this natural decision-making process.

For a pet care app like this, an explainable algorithm that matches user intuition is more valuable than a mathematically optimal but complex one. If this were scheduling hundreds of tasks for a commercial pet care facility, I might consider more sophisticated optimization. But for individual pet owners managing a handful of daily tasks, simple and understandable wins.

---

## 3. AI Collaboration

a. How you used AI

I used Claude Code as an AI assistant throughout the entire development process. During the design phase, I had the AI generate initial class structures based on my UML requirements and help me brainstorm method signatures and relationships between classes. We also explored different scheduling algorithm options and discussed their tradeoffs.

In the implementation phase, the AI wrote complete method implementations for all four classes, created a comprehensive test suite with 19 test cases, and helped me integrate the Streamlit UI with the backend logic using st.session_state for persistence.

During debugging, the AI helped identify and fix a constraint filtering bug where the method was returning all tasks when it should have returned an empty list. It also caught a test logic error in my time budget test and helped validate input error handling throughout the system.

For documentation, the AI generated UML diagrams in Mermaid.js format, wrote the comprehensive README with a detailed features list, and helped structure these reflection responses.

The most helpful types of prompts were specific task requests like "Implement the generate_plan() method with priority-based sorting and time budget constraints." Testing requests like "Create comprehensive tests covering edge cases like empty task lists and equal priorities" were also very effective. For debugging, questions like "Why is this test failing - is it the test logic or the implementation?" helped isolate problems quickly. Architecture questions about how to properly use Streamlit's session state were crucial for making the UI work correctly.

b. Judgment and verification

One clear example where I didn't accept an AI suggestion as-is was with the time budget test. The AI initially generated a test that expected both a 45-minute task and a 30-minute task to fit in a 60-minute budget. The test comment even said "would exceed budget" but the assertion still expected both tasks to be scheduled.

I caught this by reading the test code carefully and doing the math myself: 45 + 30 = 75 minutes, which exceeds the 60-minute budget. The test was checking for the wrong thing. The intent was clearly to verify budget constraints, but the expected values were incorrect.

My verification strategy throughout the project was to always read generated code line-by-line before accepting it, run tests immediately to catch logic errors, verify mathematical calculations manually, and check that test assertions actually match their stated intent. When debugging, I analyzed both the test code and the implementation to figure out where the problem really was.

The key lesson here is that AI is excellent at generating syntactically correct code - code that will compile and run without errors. But semantic correctness is different. The AI can write code that does the wrong thing in a perfectly valid way. Humans need to verify that the logic actually makes sense, especially for calculations, edge cases, and design tradeoffs.

---

## 4. Testing and Verification

a. What you tested

I created 19 comprehensive tests covering nine core behavior categories. The first category was task completion and due status, with tests verifying that non-recurring tasks get excluded after completion while recurring tasks remain due. This is important because the core scheduling logic depends on is_due() working correctly.

I tested task addition to verify that tasks are properly added to pets, which is fundamental for data integrity. Priority-based sorting got two tests to ensure tasks are sorted correctly by priority and that equal priorities are handled properly, since the scheduling algorithm relies entirely on correct ordering.

Time budget constraints got three tests covering different scenarios: verifying the scheduler respects available time, handling exact time budget matches, and returning an empty plan when all tasks exceed the budget. These tests ensure schedules are realistic and achievable.

Multi-pet task aggregation had three tests checking that tasks are collected from all pets, empty pet lists are handled gracefully, and pets without tasks don't break the system. This is critical since multi-pet support is a key feature.

Input validation tests check that negative priorities raise errors, zero or negative durations raise errors, and editing non-existent tasks raises errors. These prevent invalid data from corrupting the system.

Constraint filtering tests verify category filtering works correctly, no constraints includes all tasks, and no matching tasks returns an empty list rather than showing everything. The scheduler reasoning test confirms explanations include owner name, time, and preferences, which is important for transparency. Finally, completed task exclusion verifies that completed non-recurring tasks don't get scheduled again, preventing duplicate work.

b. Confidence

I'm very confident the scheduler works correctly - I'd rate it around 95%. This confidence comes from having 100% of tests passing (all 19 tests), thorough coverage of both happy paths and edge cases, comprehensive error handling, and manual confirmation through the Streamlit UI. The algorithm itself is also relatively simple, which makes it easier to reason about and less likely to have hidden bugs.

If I had more time, there are ten additional edge cases I'd want to test. Time-of-day scheduling would be important since the current system only considers duration, not when tasks happen. Task dependencies like "feed before walk" type constraints would be valuable. I'd want to test concurrent task conflicts where two tasks happen at the same time, and what happens with task priority ties when there's limited time. Performance testing with very large datasets (1000+ tasks) would be good to verify scalability. Testing invalid constraint format strings, negative available_minutes that should be validated at Owner creation, unicode in task titles for international support, partial task completion scenarios, and dynamic priority adjustment as tasks become more urgent would all strengthen confidence in the system.

The 5% uncertainty comes from knowing that real-world usage often reveals unexpected edge cases that testing doesn't catch. Performance hasn't been tested at scale, and there are UI/UX edge cases like rapid button clicking or network issues that might cause problems I haven't anticipated.

---

## 5. Reflection

a. What went well

I'm most satisfied with the clean separation of concerns in the architecture. The data models (CareTask, Pet, Owner) are pure data containers with minimal business logic. The business logic (Scheduler) is completely isolated as a testable scheduling algorithm. And the UI layer (app.py) is just a Streamlit interface that imports and uses the logic layer without mixing concerns.

This architecture made the project easy to work with in several ways. I could test scheduling logic independently of the UI, which made test-driven development actually practical. Each class has a single, clear responsibility, so it's easy to understand what different parts of the code do. I could add new features without major refactoring since responsibilities are clearly divided. And when tests failed, the isolated components made it straightforward to figure out what was actually wrong.

The comprehensive test suite with 19 tests and a 100% pass rate gave me real confidence that the system works correctly and will continue working as I make changes. That peace of mind is valuable.

c. What you would improve

If I had another iteration, there are several things I'd improve. The biggest one is adding time-of-day scheduling, since the current system only considers duration. A real pet owner needs to know "feed at 8am, walk at 9am" not just "feed (10 minutes), walk (30 minutes)."

Implementing task dependencies would be valuable since some tasks must happen in order, like feeding before walking. I could probably model this with a directed acyclic graph and use topological sorting to respect dependencies.

Adding conflict detection and resolution would help - the system should warn when two tasks overlap in time and suggest alternatives or automatic rescheduling. Right now it just assumes tasks happen sequentially.

I could upgrade from the greedy algorithm to dynamic programming to maximize total priority within the time budget, essentially treating it as a knapsack problem. This would be mathematically optimal, though I'd need to make sure the reasoning explanations stayed understandable.

The UI could use improvements like drag-and-drop task reordering, a calendar view of scheduled tasks, task history and completion statistics, and mobile-responsive design.

Data persistence is currently missing - all data is lost on page refresh. Adding SQLite, JSON files, or cloud storage would make this much more practical for real use.

Multi-day planning would extend the system beyond single-day schedules to week-long planning with more sophisticated recurring task patterns.

Finally, performance optimization with caching for large task lists and memoization for repeated scheduling calls would help the system scale better.

b. Key takeaway

The most important thing I learned is that the human's role is system design and verification while AI excels at implementation. Working with Claude Code showed me clear patterns about what AI does exceptionally well versus what requires human judgment.

AI is great at generating boilerplate code like dataclasses and method stubs, implementing well-specified algorithms like priority sorting and filtering, creating comprehensive test suites, writing documentation and explanations, and refactoring code for clarity. These are all tasks where the requirements are clear and the problem is well-defined.

But human judgment is critical for architectural decisions - deciding which classes to create and what their responsibilities should be. Algorithm selection requires understanding tradeoffs between greedy versus optimal approaches and knowing which tradeoffs actually matter for your use case. Semantic correctness is a human responsibility because AI can write syntactically perfect code that does the wrong thing, like that test math error I caught. User experience decisions about what warnings help users and how data should be displayed require human intuition. And scope and priority decisions about essential versus nice-to-have features need human judgment about user needs.

The ideal workflow that emerged is: human designs the system architecture and algorithms, AI implements the design with guidance, human verifies correctness through code review and testing, AI generates comprehensive tests, human validates that tests actually test the right behaviors, and then we iterate with the human making design decisions while AI handles implementation.

The key insight is that AI is a force multiplier for implementation, but the human must be the lead architect who sets the vision, makes design tradeoffs, validates correctness, and ensures the system actually solves the real user problem. This mirrors professional software engineering where senior engineers make architectural decisions while leveraging tools like IDEs, linters, and code generators for implementation efficiency. AI is just a more powerful tool in that toolkit, but it doesn't replace the need for human architectural thinking and judgment.
