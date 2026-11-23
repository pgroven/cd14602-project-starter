# AI Edit Log

**Instructions:** Use this document to track all your interactions with AI assistants during the project. This log will help you reflect on your AI collaboration process and demonstrate your learning journey.

## How to Use This Log

For each AI interaction, create a new entry with the following structure:

### Entry Template
```
## [Date] - [Brief Description]

**Context:** What were you trying to accomplish?
**AI Tool Used:** Claude/ChatGPT/Copilot/etc.
**Prompt/Request:** What exactly did you ask the AI?
**AI Response:** Summary of what the AI generated (don't copy entire code blocks)
**Changes Made:** What modifications did you make to the AI's suggestions?
**Reasoning:** Why did you make those changes?
**Outcome:** What was the final result?
**Lessons Learned:** What did you learn from this interaction?
```

---

## Example Entry

> This entry shows the expected level of detail. It does **not** count toward your five required entries. Delete it before you submit.

### 2024-01-15 - Flashcard Loader Validation

**Context:** I needed a module that loads flashcards from a JSON file and rejects bad data with a clear message instead of a traceback.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Create `data_loader.py` with a function that loads flashcards from a JSON file. Support both a plain list of `{"front", "back"}` objects and a `{"cards": [...]}` wrapper. Raise a custom exception with a helpful message if the file is missing, the JSON is malformed, or a card has no `back`. Use type hints."

**AI Response:** Claude generated a `load_flashcards()` function and a `FlashcardLoadError` exception. It handled both JSON formats and a missing file, but it caught every exception with a bare `except:` and only checked for `front`.

**Changes Made:** 
- Replaced the bare `except:` with specific `FileNotFoundError` and `json.JSONDecodeError` handlers
- Added validation that every card has non-empty `front` and `back` strings
- Added the card's position to the error message so the user can find the bad entry

**Reasoning:** 
- A bare `except:` hides real bugs, including `KeyboardInterrupt`
- A card without a `back` would break the quiz loop later, far from the cause
- A message that names the bad card is far easier to act on

**Outcome:** The loader now rejects bad decks with one readable line, and `test_load_missing_required_field` passes.

**Lessons Learned:** 
- AI covered the happy path well but under-specified the error handling
- Naming the exact failure cases in the prompt produced better code than asking for "error handling"
- Each requirement in the prompt should map to a test

---

## Your Log Entries

### 2026-11-23 - Count AI edit log words

**Context:** The user wanted the word count of the AI interaction log.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Count the words in `ai_edit.log.md`.
**AI Response:** Counted whitespace-separated tokens in `docs/ai_edit_log.md`, interpreting the filename as a reference to the existing log.
**Changes Made:** No project content was changed.
**Reasoning:** Whitespace token counting gives a reproducible whole-file count including headings and Markdown.
**Outcome:** The log contained 3,259 whitespace-separated tokens at the time of the count.
**Lessons Learned:** Confirm the intended document when the requested filename differs slightly from the actual file.

### 2026-11-23 - Explain code and performance metrics

**Context:** The report includes a code quality metrics section and asks about performance optimizations.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Explain code metrics and performance measurements in relation to this application.
**AI Response:** Explained how to interpret LOC, coverage, and lint findings, and analyzed the algorithms and history file I/O.
**Changes Made:** No report or application code was changed.
**Reasoning:** No runtime benchmark had been run, so measured performance needed to be distinguished from complexity analysis.
**Outcome:** Provided report guidance and noted the existing metrics' scope and age.
**Lessons Learned:** Do not present algorithmic complexity as benchmark data.

### 2026-11-23 - Explain code organization

**Context:** The project report asks how the code is organized.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Explain the code organization.
**AI Response:** Mapped the CLI, data loader, quiz engine, interface, utilities, and tests to their separate responsibilities.
**Changes Made:** No application code changes were made.
**Reasoning:** The request was for a report-oriented explanation.
**Outcome:** Prepared a concise description of the modular structure and separation of concerns.
**Lessons Learned:** Explain both module responsibilities and how control flows between them.

### 2026-11-23 - Explain design patterns

**Context:** The report asks for an explanation of design patterns used in the project.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Explain the design patterns used.
**AI Response:** Verified the quiz mode abstraction, concrete modes, factory, and engine integration, then explained Strategy and Factory.
**Changes Made:** No application code changes were made.
**Reasoning:** The request was for a report-oriented explanation.
**Outcome:** Explained how interchangeable quiz strategies and the factory work together.
**Lessons Learned:** Describe patterns in terms of their concrete roles in the program.

### 2026-11-23 - Explain core and additional features

**Context:** The report template asks the author to list core and additional features.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Explain the core functionality and additional features.
**AI Response:** Distinguished required quiz behavior from enhancements and outlined report-ready feature bullets based on the implementation.
**Changes Made:** No application or report content was changed.
**Reasoning:** The request was for explanation and guidance on categorizing the implemented features.
**Outcome:** Provided a suggested core/additional feature breakdown.
**Lessons Learned:** Separate baseline requirements from quality-of-life features in the report.

### 2026-11-23 - Explain report overview and summary

**Context:** The report template asks for an Executive Summary and a Project Overview.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Explain the project overview and summary.
**AI Response:** Explained the difference between the brief whole-project summary and the detailed problem/solution/features overview, with draft language based on the implemented CLI.
**Changes Made:** No report content was changed.
**Reasoning:** The user asked for clarification rather than an edit to the report.
**Outcome:** Provided guidance and example text for both sections.
**Lessons Learned:** Keep the executive summary concise and use the overview to explain the problem and design details.

### 2026-11-19 - Count report words

**Context:** The project report has a word-count requirement.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** How many words are in `report_template.md`?
**AI Response:** Counted whitespace-separated tokens in the complete file.
**Changes Made:** No report changes were made.
**Reasoning:** A whole-file count gives a clear baseline while including template text and Markdown.
**Outcome:** The file contained 1,157 whitespace-separated tokens at the time of the count.
**Lessons Learned:** Template instructions and Markdown can inflate a report word count.

### 2026-11-19 - Check lint results

**Context:** The project report asks for a linting score.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** What is the linting score?
**AI Response:** Ran flake8 with its issue count enabled.
**Changes Made:** No application code changes were made.
**Reasoning:** Flake8 reports violations rather than a numerical score.
**Outcome:** Flake8 reported zero violations.
**Lessons Learned:** Report the linter's actual metric rather than inventing a score.

### 2026-11-19 - Count functions and classes

**Context:** The project report asks about code structure.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** How many functions and classes are there?
**AI Response:** Counted Python definitions in the application and test files, distinguishing methods from standalone functions.
**Changes Made:** No application code changes were made.
**Reasoning:** Methods and test helpers affect the count depending on how functions are defined.
**Outcome:** The application has 11 classes, 11 standalone functions, and 8 methods. Test files add 35 function definitions, including nested helpers.
**Lessons Learned:** State whether methods, nested helpers, and tests are included in counts.

### 2026-11-19 - Measure test coverage

**Context:** The project report asks for the test coverage percentage.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** What is the test coverage percentage?
**AI Response:** Ran pytest with coverage restricted to the application modules, excluding test files.
**Changes Made:** No application code changes were made.
**Reasoning:** Application-only coverage is more informative than including the test files themselves.
**Outcome:** All 44 tests passed; reported application statement coverage was 95% (222 of 233 statements). Subprocess execution was not included in the coverage measurement.
**Lessons Learned:** Define the measurement scope when reporting coverage.

### 2026-11-19 - Count project code lines

**Context:** The project report asks about code size.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** How many lines of code are there?
**AI Response:** Counted physical lines in the starter's application and test Python files separately, including blank lines and comments.
**Changes Made:** No application code changes were made.
**Reasoning:** Separating application and test files makes the count easier to interpret.
**Outcome:** Counted 377 application lines and 462 test lines, for 839 total.
**Lessons Learned:** State what a line count includes.

### 2026-11-19 - Explain the technology stack

**Context:** The project report asks for the technology stack.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** What technology stacks are used?
**AI Response:** Reviewed the application, requirements, and README and summarized the runtime, data format, development tools, and diagram formats.
**Changes Made:** No application code changes were made.
**Reasoning:** The request was for an explanation of the existing project.
**Outcome:** Provided a stack summary that distinguishes the CLI's standard-library runtime from development tools.
**Lessons Learned:** A listed dependency is not necessarily used by the application at runtime.

### 2026-11-19 - Explain core functionality

**Context:** The project functionality needed an explanation.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Explain the core functionality.
**AI Response:** Reviewed the CLI, loader, quiz modes, interaction, and history handling, then explained how a quiz works.
**Changes Made:** No application code changes were made.
**Reasoning:** The request was for an explanation, not a feature change.
**Outcome:** Provided a summary grounded in the existing implementation.
**Lessons Learned:** Verify behavior in the source before describing it.

### 2026-11-19 - Document development setup

**Context:** Contributors need steps to set up and run the project locally.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Add steps to get a development environment running in the README.
**AI Response:** Added virtual environment, dependency installation, test, and quiz commands for Windows PowerShell and macOS/Linux.
**Changes Made:** Updated the starter README.
**Reasoning:** Explicit interpreter paths avoid relying on shell activation and address the earlier PowerShell path issue.
**Outcome:** The documented Windows test command passed using the existing virtual environment; environment creation and installation were not rerun.
**Lessons Learned:** Document the working directory and interpreter explicitly.

### 2026-11-19 - Improve input validation and errors

**Context:** The quiz already validates decks and handles several file and history errors, but some input edge cases need clearer behavior.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Add input validation and error handling. The user chose to reprompt for blank answers and leave `exit` unchanged.
**AI Response:** Added blank-answer validation and friendly errors for invalid Unicode, overly nested JSON, and history location failures.
**Changes Made:** Updated the loader, quiz UI, file and history helpers, README, and focused tests.
**Reasoning:** Invalid answers should not affect the score, and malformed inputs or unavailable history locations should not cause raw tracebacks.
**Outcome:** All 44 tests passed; Black, flake8, and mypy checks passed.
**Lessons Learned:** Define invalid-input behavior before changing the quiz interaction and test failures at the relevant boundaries.

### 2026-11-19 - Add editable architecture diagrams

**Context:** The existing Mermaid architecture diagram also needed editable draw.io and D2 versions.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Add a draw.io and D2 diagram.
**AI Response:** Created equivalent architecture diagrams and linked them from the starter README.
**Changes Made:** Added `docs/architecture.drawio` and `docs/architecture.d2`; updated the README.
**Reasoning:** Both formats give readers editable alternatives to the Mermaid diagram.
**Outcome:** D2 compiled successfully; the draw.io XML and its node and edge references validated. The draw.io application was not available for a visual check.
**Lessons Learned:** Validate diagram source and connections, and report when visual validation is unavailable.

### 2026-11-19 - Add an architecture diagram

**Context:** The project README needed a diagram of the application.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Add a Mermaid diagram.
**AI Response:** Added a flowchart showing the CLI, deck loading, quiz strategies, interface, and saved history.
**Changes Made:** Updated the starter README.
**Reasoning:** A diagram makes the application's components and interactions easier to understand.
**Outcome:** The README includes a Mermaid architecture diagram. The preview opened, but the syntax validator required a Mermaid sign-in.
**Lessons Learned:** Verify diagram relationships against the implementation.

### 2026-11-19 - Verify tests and lint

**Context:** The project requires all tests to pass and flake8 to report no errors.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Ensure all tests pass and flake8 reports no linting errors.
**AI Response:** Ran the full pytest suite and flake8 against the starter directory using the project virtual environment.
**Changes Made:** No application code changes were needed.
**Reasoning:** Both checks passed without changes.
**Outcome:** All 37 tests passed; flake8 exited successfully with no reported errors.
**Lessons Learned:** Run both the complete test suite and lint check against the project directory.

### 2026-11-19 - Verify design patterns

**Context:** The quiz engine must use Strategy and Factory patterns.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Ensure the patterns can be checked in `quiz_engine.py`.
**AI Response:** Inspected the quiz mode abstraction, its three implementations, the factory, and the CLI's factory call.
**Changes Made:** No application code changes were needed.
**Reasoning:** The existing implementation already uses both requested patterns.
**Outcome:** `QuizEngine` delegates ordering to a `QuizMode`, and `QuizModeFactory` selects the implementation from the CLI mode.
**Lessons Learned:** Verify that patterns are both defined and used at their integration points.

### 2026-11-19 - Quiz strategies and CLI

**Context:** Phase 1 provides validated decks; the quiz engine and interface are next.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Implement sequential, random, and adaptive modes with Strategy and Factory patterns, plus a CLI with file, mode, stats, colored feedback, and graceful exit handling. The user clarified that `--stats` should show saved missed-card history before the quiz, while the session summary remains automatic.
**AI Response:** Implemented the three quiz strategies, their factory, answer checking, a terminal interface, and per-deck adaptive history that persists across sessions.
**Changes Made:** Added the quiz engine, interface, history helper, and tests; updated the CLI and README. History records unresolved misses after each answer and clears a card's count when it is answered correctly.
**Reasoning:** Separate strategies make ordering selectable; saving each completed answer preserves progress after an early exit.
**Outcome:** 37 tests passed, including a two-process adaptive-history test; reported total coverage was 99%. Black, flake8, and mypy checks passed.
**Lessons Learned:** Clarify CLI flag semantics when they overlap an existing requirement, and test persistence across actual process boundaries.

### 2026-11-19 - Plan the Flashcard Quizzer

**Context:** The project needs a modular, typed CLI with JSON validation, quiz strategies, and session statistics.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Create the Flashcard Quizzer with the specified modules, three quiz modes, tests, and support for both JSON deck formats; the request also identifies Phase 1 as the data layer. The user clarified that only Phase 1 should be implemented now and that adaptive mode should eventually remember missed cards between sessions.
**AI Response:** Reviewed the project guidance and sample decks, then implemented typed JSON loading, validation, a validation CLI, and tests.
**Changes Made:** Added `data_loader.py`, `utils/file_handler.py`, and tests; updated `main.py` and the starter README. The quiz engine and adaptive persistence were deferred.
**Reasoning:** Phase 1 needs a usable way to exercise validation without implementing later quiz behavior.
**Outcome:** Both sample deck formats load; missing files, malformed JSON, and invalid cards produce friendly errors. All 19 tests passed, as did Black, flake8, and mypy checks on the changed Python files.
**Lessons Learned:** Resolve scope and persistence requirements before designing the data and quiz layers, and verify both valid and invalid inputs.

### 2026-11-18 - PowerShell virtual environment path error

**Context:** Installing dependencies failed because PowerShell could not recognize a Python executable path beginning with `/c:/`.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Diagnose the error from `python -m pip install -r requirements.txt`.
**AI Response:** Suggested using the virtual environment's Windows-style Python path or activating the environment, and identified the project requirements file.
**Changes Made:** No project files were changed.
**Reasoning:** The error concerned the executable path rather than a reported dependency conflict.
**Outcome:** The assistant confirmed that the virtual environment executable existed. Its installation check used system Python, not the virtual environment.
**Lessons Learned:** Verify which interpreter runs pip; PowerShell requires a valid Windows executable path.

### 2026-11-19 - Check development tool installation

**Context:** The development environment needed black, pytest, mypy, and flake8.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Install black, pytest, mypy, and flake8.
**AI Response:** Checked the project virtual environment and found all four tools already installed.
**Changes Made:** No packages or project files were changed; the Python environment was configured to use the project virtual environment.
**Reasoning:** Reinstalling packages was unnecessary because they were already present.
**Outcome:** Confirmed the installed versions and their locations in `.venv`.
**Lessons Learned:** Check the intended environment before installing dependencies.

### 2026-11-19 - Check development requirements

**Context:** The four development tools needed to be listed in the project requirements.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Add black, pytest, mypy, and flake8 to `requirements.txt`.
**AI Response:** Found all four already listed in `project/starter/requirements.txt` and noted its Git status.
**Changes Made:** No project files were changed.
**Reasoning:** Adding duplicate requirements was unnecessary.
**Outcome:** The file already contained all requested tools; Git showed it staged for deletion with the current copy untracked.
**Lessons Learned:** Check existing requirements and Git status before modifying dependencies.

### 2026-11-19 - Record AI interactions

**Context:** AI collaboration should be documented in the project log.
**AI Tool Used:** GitHub Copilot
**Prompt/Request:** Write all AI interactions to `ai_edit_log.md`.
**AI Response:** Recorded the interactions visible in this conversation and attempted to save the logging preference for future repository work.
**Changes Made:** Added entries to this log.
**Reasoning:** The project requires an accurate record of AI collaboration.
**Outcome:** The visible interactions were documented; saving the repository memory was unavailable.
**Lessons Learned:** Record interactions as they happen so the log remains complete.

### [Date] - [Brief Description]

**Context:** 

**AI Tool Used:** 

**Prompt/Request:** 

**AI Response:** 

**Changes Made:** 

**Reasoning:** 

**Outcome:** 

**Lessons Learned:** 

---

### [Date] - [Brief Description]

**Context:** 

**AI Tool Used:** 

**Prompt/Request:** 

**AI Response:** 

**Changes Made:** 

**Reasoning:** 

**Outcome:** 

**Lessons Learned:** 

---

## Tips for Effective AI Collaboration

### 1. Be Specific in Your Requests
- ❌ "Write a function"
- ✅ "Write a function that validates email addresses using regex, returns a boolean, and includes proper error handling"

### 2. Provide Context
- Include relevant code snippets
- Explain the larger goal
- Mention any constraints or requirements

### 3. Review and Understand
- Never copy AI code without understanding it
- Ask for explanations of complex logic
- Test the code before accepting it

### 4. Iterate and Refine
- Use follow-up questions to improve the code
- Ask for alternative implementations
- Request code reviews and suggestions

### 5. Document Your Process
- Keep detailed notes in this log
- Explain your decision-making process
- Track what works and what doesn't

## Common AI Collaboration Patterns

### Code Generation
- Initial implementation of classes/functions
- Boilerplate code creation
- Test case generation

### Code Review
- Ask AI to review your code for issues
- Request suggestions for improvements
- Get feedback on code structure

### Problem Solving
- Debugging help
- Algorithm suggestions
- Architecture advice

### Learning and Explanation
- Ask for explanations of complex concepts
- Request examples of design patterns
- Get guidance on best practices

## Reflection Questions

As you work through the project, consider these questions:

1. **What types of tasks did AI help with most effectively?**
2. **Where did you need to make the most modifications to AI suggestions?**
3. **What patterns did you notice in AI strengths and weaknesses?**
4. **How did your prompting technique improve over time?**
5. **What would you do differently in future AI collaborations?**

## Summary Statistics

At the end of your project, fill out these statistics:

- **Total AI interactions:** ___
- **Lines of AI-generated code used:** ___
- **Lines of AI-generated code modified:** ___
- **Most helpful AI interaction:** ___
- **Most challenging AI interaction:** ___
- **Biggest lesson learned:** ___

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.