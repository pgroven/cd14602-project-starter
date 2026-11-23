# The Flashcard Quizzer

Quiz yourself from a JSON deck in sequential, random, or adaptive order.
From this directory, for example:

```bash
python main.py --file data/glossary.json --mode sequential
python main.py -f data/python_basics.json -m adaptive --stats
```

Decks may be a JSON array or an object containing a `cards` array. The array
must contain at least one card, and each card must have nonempty string
`front` and `back` fields. Invalid decks produce a helpful error.

## Playing

`-f` / `--file` selects the deck. `-m` / `--mode` chooses `sequential`
(the default), `random`, or `adaptive`. Each card is asked once per session.
Answers are compared case-insensitively after trimming surrounding whitespace.
Empty answers are rejected and prompted again without affecting the score.
Type `exit`, press Ctrl+C, or send EOF to end early. The summary shows
completed questions, accuracy, and missed terms, including on an early exit.
Because `exit` is reserved for quitting, it cannot be submitted as an answer.
Feedback is green or red on supported terminals; set `NO_COLOR` to disable
colors.

Each answer updates local history under `~/.flashcard_quizzer/`. A wrong answer
increases that card's unresolved miss count; a correct answer clears it.
Adaptive mode asks cards with the most unresolved misses first, preserving deck
order for ties. `--stats` shows the current deck's saved misses before the quiz;
the session summary is always shown. History is associated with the resolved
deck path and card contents, so moving a deck or changing a card starts new
history for the affected deck or card. Identical cards in the same deck share
history. Do not run simultaneous quizzes on the same deck: concurrent history
updates are not coordinated.

## Architecture

Editable versions: [draw.io](docs/architecture.drawio) and
[D2](docs/architecture.d2).

```mermaid
flowchart TD
    User["User"] --> CLI["main.py: CLI"]
    CLI --> Loader["data_loader.py: validate deck"]
    Loader --> FileHandler["utils/file_handler.py: read JSON"]
    FileHandler --> Deck["JSON deck"]
    CLI --> Factory["QuizModeFactory"]
    Factory --> Sequential["SequentialMode"]
    Factory --> Random["RandomMode"]
    Factory --> Adaptive["AdaptiveMode"]
    Sequential --> Engine["QuizEngine"]
    Random --> Engine
    Adaptive --> Engine
    CLI --> UI["ui.py: quiz interaction"]
    UI --> Engine
    CLI --> History["utils/history.py"]
    UI --> History
    History --> Store["Saved missed-card history"]
    UI --> User
```

## What's in the starter

```
starter/
├── main.py                 # CLI entry point
├── data_loader.py          # Flashcard validation
├── quiz_engine.py          # Quiz strategies, factory, and results
├── ui.py                   # Terminal interaction
├── data/                   # Sample flashcard decks
│   ├── glossary.json       # Array format: [{"front": ..., "back": ...}]
│   └── python_basics.json  # Object format: {"cards": [...]}
├── utils/                  # File and history helpers
├── tests/                  # pytest suite
├── docs/
│   ├── ai_edit_log.md      # AI interaction log (required, 5+ entries)
│   ├── report_template.md  # Final report template (required, 1,000-1,500 words)
│   └── design_patterns.md  # Pattern reference
├── ai_guidance/            # Prompting and code review guides
├── .claude/                # Claude Code configuration and slash commands
└── requirements.txt        # Quality tools: pytest, black, flake8, mypy, ...
```

The two sample decks use the two JSON formats your loader must support. You can add your own decks to `data/`.

## Getting started

1. Install Python 3.9 or newer and open a terminal at the repository root.
2. Create a virtual environment if `.venv` does not already exist. On Windows
   PowerShell:

   ```powershell
   py -3 -m venv .venv
   ```

   On macOS or Linux:

   ```bash
   python3 -m venv .venv
   ```

3. Enter the starter directory and install its development dependencies. On
   Windows PowerShell, use the virtual environment's interpreter directly:

   ```powershell
   cd project\starter
   ..\..\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

   On macOS or Linux:

   ```bash
   cd project/starter
   ../../.venv/bin/python -m pip install -r requirements.txt
   ```

4. Verify the setup and start a quiz. From `project/starter`, on Windows:

   ```powershell
   ..\..\.venv\Scripts\python.exe -m pytest -q
   ..\..\.venv\Scripts\python.exe main.py -f data\glossary.json
   ```

   On macOS or Linux:

   ```bash
   ../../.venv/bin/python -m pytest -q
   ../../.venv/bin/python main.py -f data/glossary.json
   ```

These commands do not require activating the virtual environment. To use the
shorter `python` commands below, first activate `.venv` in your shell.

## Development checks

```bash
python -m pytest --cov=. --cov-report=html   # target: >80% coverage
python -m black --check .
python -m flake8 .
python -m mypy .
```

## What to submit

Check the Instructions page and the rubric for the full list. In short:

- Your complete source code, the `tests/` suite, and the `data/` decks
- `docs/ai_edit_log.md` with at least 5 detailed AI interactions
- The final report, written from `docs/report_template.md` (1,000-1,500 words)
- This README, rewritten to describe **your** application: features, setup, and usage examples

## License

[License](../../LICENSE.txt)
