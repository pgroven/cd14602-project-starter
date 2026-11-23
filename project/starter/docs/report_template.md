# AI-Assisted Development Project Report

**Student Name:** [Phillip Groven]  
**Project Title:** [AI Flashcard Quizzer]  
**Date:** [11-20-2026]

## Executive Summary

Provide a brief overview of your project (2-3 paragraphs):
The Flashcard Quizzer is a Python command-line app for studying terms from JSON flashcard decks. Users can practice cards in sequential, random, or adaptive order. It checks answers without regard to case, provides immediate feedback, and reports session accuracy and missed terms.

The app validates deck data and saves missed-card history between sessions so adaptive mode can prioritize cards that need more practice. AI assistants helped with implementation and review; the code and tests were checked with pytest, flake8, Black, and mypy.

- What application did you build?
- What were the main features and functionality?
- How did you collaborate with AI throughout the development process?

## Project Overview

### Problem Statement
Problem Statement: Reviewing flashcards in a fixed order can make it harder to focus on terms that need extra practice. The app provides a command-line way to study JSON decks and revisit missed cards.

Solution Approach: The CLI parses file and mode options. A data loader validates the deck, and the quiz engine uses Strategy and Factory patterns to select sequential, random, or adaptive ordering. The interface handles answers, feedback, and session summaries; saved history supports adaptive practice across sessions.

Final Features: List the working modes, JSON formats, validation and error handling, blank-answer behavior, graceful exit options, adaptive history, and session statistics. Don’t call it an AI-powered application; AI assisted its development.

Describe the problem your application solves or the need it addresses.
This AI quiz provides a good example of the ease of designing and building an AI application.

### Solution Approach
Explain your approach to solving the problem, including:
- Key design decisions were based on the Product Requirements.
- Technology stack used
Python
### Final Features
List the features you implemented:
- The Flashcard Quizzer loads a JSON deck, presents each card’s front, and checks the user’s answer against its back. Answers are case-insensitive; empty answers prompt the user again.

quiz_engine.py provides three modes: sequential, random, and adaptive. Adaptive mode asks previously missed cards first, using history saved between sessions.

At the end, the app shows the number of questions answered, accuracy, and missed terms. Users can quit with exit or Ctrl+C

- [ ] Core functionality #2
For the report, separate the features the quiz needs to work from enhancements:

Core functionality

Load and validate flashcards from either supported JSON format.
Ask each card and check answers without regard to capitalization.
Offer sequential, random, and adaptive quiz modes.
Show correct/incorrect feedback and a session summary with accuracy and missed terms.

I’ll distinguish the features essential to the quiz from enhancements, based on the implementation and report template.

Read , lines 18 to 42
Completed with input: {
  "path": "C:\\Users\\Admin\\git\\cd14602-project-starter\\project\\starter\\docs\\report_template.md",
  "view_range": [
    18,
    42
  ]
}

Read , lines 1 to 42
Completed with input: {
  "path": "C:\\Users\\Admin\\git\\cd14602-project-starter\\project\\starter\\README.md",
  "view_range": [
    1,
    42
  ]
}

Read 
Completed with input: {
  "path": "C:\\Users\\Admin\\git\\cd14602-project-starter\\project\\starter\\ui.py"
}

Read , lines 1 to 110
Completed with input: {
  "path": "C:\\Users\\Admin\\git\\cd14602-project-starter\\project\\starter\\quiz_engine.py",
  "view_range": [
    1,
    110
  ]
}

Read , lines 1 to 75
Completed with input: {
  "path": "C:\\Users\\Admin\\git\\cd14602-project-starter\\project\\starter\\utils\\history.py",
  "view_range": [
    1,
    75
  ]
}

"Apply Patch" failed
Completed with input: "*** Begin Patch\n*** Update File: project/starter/docs/ai_edit_log.md\n@@\n ## Your Log Entries\n \n+### 2026-11-23 - Explain core and additional features\n+\n+**Context:** The report template asks the author to list core and additional features.\n+**AI Tool Used:** GitHub Copilot\n+**Prompt/Request:** Explain the core functionality and additional features.\n+**AI Response:** Distinguished required quiz behavior from enhancements and outlined report-ready feature bullets based on the implementation.\n+**Changes Made:** No application or report content was changed.\n+**Reasoning:** The request was for explanation and guidance on categorizing the implemented features.\n+**Outcome:** Provided a suggested core/additional feature breakdown.\n+**Lessons Learned:** Separate baseline requirements from quality-of-life features in the report.\n+\n ### 2026-11-19 - Count functions and classes\n*** End Patch\n"
Tool execution failed: Failed to apply patch: Error: Failed to find expected lines in c:\Users\Admin\git\cd14602-project-starter\project\starter\docs\ai_edit_log.md:
## Your Log Entries

### 2026-11-19 - Count functions and classes

Read , lines 55 to 75
Completed with input: {
  "path": "C:\\Users\\Admin\\git\\cd14602-project-starter\\project\\starter\\docs\\ai_edit_log.md",
  "view_range": [
    55,
    75
  ]
}

Edit 

For the report, separate the features the quiz needs to work from enhancements:

**Core functionality**
- Load and validate flashcards from either supported JSON format.
- Ask each card and check answers without regard to capitalization.
- Offer sequential, random, and adaptive quiz modes.
- Show correct/incorrect feedback and a session summary with accuracy and missed terms.

**Additional features**
- Save missed-card history between sessions; adaptive mode prioritizes cards with more misses.
- Show saved misses with `--stats`.
- Reprompt on blank answers and exit gracefully on `exit`, Ctrl+C, or EOF.
- Use terminal colors when supported, with a `NO_COLOR` option.
- Report helpful errors for invalid decks or unreadable history.

These are suggestions for categorizing the implemented features; describe them in your own words in the report.

## AI Collaboration Experience

### AI Tools Used
List the AI tools/assistants you worked with:
- [X] Claude
- [X] GitHub Copilot
- [ ] ChatGPT
- [ ] Other: ________

### Collaboration Workflow
Describe your typical workflow when working with AI:
1. How did you structure your requests/prompts?
   Requests to AI were structured with extreme detail setting boundaries of what the final outcome should look like.
2. What types of tasks did you ask AI to help with?
   AI was used for coding but manualy reviewed for readability and completeness
3. How did you review and validate AI-generated code?
   Code was reviewed vsually and by running unit tests and hands on testing of the  Quiz.
4. What was your process for refining AI suggestions?
   Defining each task completely in a single step helped break down multiple tasks
### Most Valuable AI Interactions
Document 3-5 specific examples where AI assistance was particularly helpful:
AI was particularly helpful in getting the initial python code started.

#### Example 1: [Brief Title]
**Context:** What were you trying to accomplish?
**AI Prompt:** What did you ask the AI to do?
**AI Response:** What code/suggestions did it provide?
**Your Changes:** What modifications did you make and why?
**Outcome:** What was the final result?

#### Example 2: [Brief Title]
**Context:** 
**AI Prompt:** 
**AI Response:** 
**Your Changes:** 
**Outcome:** 

[Continue for additional examples...]

### Challenges with AI Collaboration
Describe any difficulties you encountered:
- What types of requests did AI struggle with?
AI  did not struggle with any requests but did ask clarificatoin on quiz behavior.
- When did you need to significantly modify AI suggestions?
Significant modification of AI suggestions was not needed.
- What patterns did you notice in AI strengths/weaknesses?

## Software Engineering Practices

### Code Quality Measures
Document the practices you implemented:
- [X] Code formatting (Black, isort)
- [X] Linting (flake8, mypy)
- [X] Type hints
- [X] Documentation/comments
- [X] Error handling

### Testing Strategy
Describe your approach to testing:
- What types of tests did you write?
- What was your test coverage percentage?
- How did you ensure code reliability?
- Did you use test-driven development?

### Design Patterns Used
The project uses two patterns in quiz_engine.py:

Strategy: QuizMode defines a shared order() interface. SequentialMode, RandomMode, and AdaptiveMode each implement a different card ordering. QuizEngine uses whichever strategy it receives, keeping quiz logic separate from ordering logic.
Factory: QuizModeFactory maps the selected mode name to the right strategy object. The CLI passes that object to QuizEngine, so mode selection is kept separate from quiz execution.
Together, these patterns make it easier to select or add a quiz mode without rewriting the quiz engine.

### Code Structure and Organization
Explain how you organized your code:
The project is organized into modules with separate responsibilities:

main.py parses command-line options and coordinates the app.
data_loader.py reads and validates flashcards.
quiz_engine.py handles answer checking, session statistics, and the quiz-mode strategies.
ui.py manages prompts, feedback, and summaries.
utils/ contains JSON file handling and saved-history utilities.
tests/ contains loader, engine, and CLI tests. Sample decks are in data/.
The flow is: the CLI loads and validates a deck, selects a quiz strategy, then passes cards to the engine and interface. Utilities persist missed-card history separately from the quiz logic.

Report-ready summary: “I organized the application into focused modules to separate command-line handling, deck validation, quiz logic, user interaction, and file/history utilities. This separation makes the code easier to test and maintain. Tests are grouped by loader, engine, and CLI behavior.”
- How you maintained separation of concerns
- Any refactoring you performed

## Technical Challenges and Solutions

### Challenge 1: [Brief Title]
**Problem:** Describe the technical challenge you faced
Getting the base code started wa a challenge and AI was able to ge me started.  I learned how to handle AI uses and strentgths.


## Code Quality Analysis

### Metrics
Provide quantitative measures of your code quality:
- Lines of code: The Python project has 839 physical lines: 377 application lines and 462 test lines. This includes blank lines and comments.
- Test coverage: _95__%
Application statement coverage is 95% (222 of 233 statements). All 44 tests passed. Subprocess execution was not included in the coverage measurement.
- Number of functions/classes:
Read skill `python-fact-grounded-coding`
Completed with input: {"skill":"python-fact-grounded-coding"}

Search for `^\s*(?:async\s+)?def\s+|^\s*class\s+`

Edit 

The application has **11 classes** and **19 functions**: 11 standalone functions and 8 methods.

The test files add 35 function definitions, including helpers.
- Linting score: 
Flake8 reported 0 linting violations.

### Self-Assessment
Rate yourself (1-5, 5 being excellent) and provide justification:
- **Code Readability:** __5_ - Why?  Existing code is small code flow path is easy to follow.
- **Code Maintainability:** __5_ - Why?  Existing code is compartmentalzied satistying the product requrements.
- **Test Quality:** __4_ - Why?  There are many testing that check for positive, negative and security issues. 
The score is 4 as there are always improvements that can be made
- **Documentation:** _5__ - Why?  Code flow with matching diagrams are documented for anyone to follow.

## Learning Outcomes

### Technical Skills Developed
What new technical skills did you acquire or improve?
- New skills I learned were Programming concepts, Tools and frameworks, testing practices and code organization

### AI Collaboration Skills
What did you learn about working with AI assistants?
- Effective prompting techniques requried very specific input and required output
- Code review and validation strategies
- When to rely on AI vs. manual coding.  AI can be used for many tasks if the complexiity is not too great.
-  AI has limitations when the application concept is new to AI and can drop existing features of code that    already exist.
### Software Engineering Insights
What software engineering principles did you better understand?
-All of the  design patterns, testing strategies and code organization were new to me.

## Reflection

### What Worked Well
Reflect on the most successful aspects of your project:
- Which AI collaboration strategies were most effective?
- What software engineering practices had the biggest impact?
- What are you most proud of in your final code?

### What Could Be Improved
Identify areas for future improvement:
- What would you do differently next time?
- Which aspects of your code could be enhanced?
- How could you improve your AI collaboration process?

### Future Enhancements
If you had more time, what features would you add?
- An API interface would be very useful and more real world like.

- New functionality
  An API based on  Flask would be a great enhancement.  Flask is a lightweight micro-framework with minimal built-in structure. It is ideal for small services and rapid prototypes
- Better user experience
   A better user experience would log the username and record quiz progress
- Performance optimizations
  Since the deck is so small performance optimizatoins were not needed.
## Conclusion

Summarize your key takeaways from this project:
- How has your understanding of AI-assisted development evolved? 
  This is the first app I have code from the ground up so the process has been invaluable.
- What software engineering practices will you continue to use?
  Allowing AI offer insight can be valuable.


## Appendices

### Appendix A: AI Interaction Log
Reference your detailed AI interaction log (`ai_edit_log.md`) and highlight key entries.
AI interaction is logged in ai_edit.log.md
### Appendix B: Code Statistics
Include any relevant code metrics, test results, or performance measurements.

### Appendix C: Additional Resources
I used youtube and google to do a deep dive on the programming concepts

---

**Total Report Length:** Aim for 3259 words  
**Due Date:** [12-23-2026]  
**Submission Instructions:** [Insert submission details]