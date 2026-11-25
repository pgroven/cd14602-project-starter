1. I check all unit tests def test_reports_missing_file in test_data_loader.py was change to test file permissions and report what permissions are needed if it fails
2. I added gui.py for future enhancements
Added descriptions to all unit tests

2026-11-25: Asked GitHub Copilot for recommendations on Python logging.
Copilot reviewed console output and history handling and suggested standard
logging, optional diagnostics, privacy safeguards, and focused tests.
AI recomended Don’t log answers, card contents, or full file paths by default.
I dont agree and added this by default

2026-11-25: Asked GitHub Copilot to configure logging with an optional verbose
flag, friendly errors, and tests. Copilot requested clarification about whether
answers, card contents, and file paths should be logged or excluded.
The user chose to include all three by default. Copilot added stderr logging,
verbose-only debug details and tracebacks, and caplog tests for expected and
unexpected failures. All 53 tests passed; Black, flake8, and mypy passed on
the changed Python files. Logs contain sensitive content and must be protected.

3. Manually check unit test descriptions and those were not updated so I had AI update them

2026-11-25: Asked GitHub Copilot to check and update unit test descriptions.
Copilot compared the descriptions with the assertions and clarified the
logging, permission, and shuffle tests without changing test behavior.

4. Reviewed logging manually and log or expiration does not exist  Instructed AI to expire logs every 30 days.

2026-11-25: Copilot noted that the app currently sends logs to stderr rather
than retaining log files and asked how the 30-day retention should work.

The user chose app-managed daily log files under ~/.flashcard_quizzer and
startup cleanup. Copilot retained stderr logging and added UTC-dated files,
deleting only files whose entries are all at least 30 days old. Daily grouping
can add almost one day of retention, and cleanup requires a subsequent startup.

