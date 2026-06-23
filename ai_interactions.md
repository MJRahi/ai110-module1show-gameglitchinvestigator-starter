# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code (agent mode): "Move the core game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` into `logic_utils.py`, fix the backwards Higher/Lower hint, and update the import in `app.py` so the game still works."

**What did the agent do?**

- Implemented all four functions in `logic_utils.py` (replacing the `NotImplementedError` stubs).
- Changed `check_guess` to return just the outcome string and added a corrected `HINT_MESSAGES` map (`Too High → Go LOWER`, `Too Low → Go HIGHER`).
- Replaced the inline function definitions in `app.py` with `from logic_utils import (...)` and updated the submit block to use `outcome = check_guess(...)` plus `HINT_MESSAGES[outcome]`.
- Ran `python3 -m pytest tests/` to confirm the suite passed, and launched the app with Streamlit to confirm it boots cleanly.

**What did you have to verify or fix manually?**

I reviewed every diff before accepting it. The agent's first refactor kept `check_guess` returning a `(outcome, message)` tuple, which broke the starter tests that expect a single string (`check_guess(50, 50) == "Win"`); I caught this by running pytest and had it switch to returning only the outcome string with a separate `HINT_MESSAGES` lookup. I also manually confirmed in the live game that the hints now point the correct direction.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number (`-5`) | "Generate pytest edge cases for `parse_guess` covering negative numbers, decimals, very large values, non-numeric text, and empty input." | `test_parse_negative_number` asserts `parse_guess("-5") == (True, -5, None)` | ✅ Yes | A negative is still a valid integer, so it should parse without crashing even if it's outside the secret's range. |
| Decimal (`3.9`) | (same prompt) | `test_parse_decimal_is_truncated` asserts `parse_guess("3.9")` returns `(True, 3, None)` | ✅ Yes | The game only deals in whole numbers, so a decimal should truncate cleanly rather than raise. |
| Very large value (`10^20`) | (same prompt) | `test_parse_very_large_number` asserts the huge value parses to the exact int | ✅ Yes | Python ints are unbounded, so an extreme value must not overflow or error. |
| Non-numeric (`abc`) | (same prompt) | `test_parse_non_numeric_is_rejected` asserts `(False, None, "That is not a number.")` | ✅ Yes | Garbage input should give a friendly error, not a stack trace. |
| Empty input (`""`) | (same prompt) | `test_parse_empty_string_is_rejected` asserts `(False, None, "Enter a guess.")` | ✅ Yes | Submitting nothing should prompt the user instead of crashing the rerun. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Add clear docstrings to every function in logic_utils.py, then run a linter
(ruff) for PEP 8 compliance on logic_utils.py, app.py, and the tests, and
apply the fixes it suggests.
```

**Linting output before:**

```
$ python3 -m ruff check --select E,W,F,I,N --line-length 100 logic_utils.py app.py tests/test_game_logic.py
I001 [*] Import block is un-sorted or un-formatted
  --> app.py:1:1
I001 [*] Import block is un-sorted or un-formatted
 --> tests/test_game_logic.py:1:1
Found 2 errors.
[*] 2 fixable with the `--fix` option.
```

**Changes applied:**

The AI added a module docstring and per-function docstrings to `logic_utils.py`. Ruff then flagged two `I001` import-ordering issues; I applied `ruff check --fix`, which sorted the imports alphabetically — in `app.py` the multi-line `from logic_utils import (...)` block was reordered (`HINT_MESSAGES, check_guess, get_range_for_difficulty, parse_guess, update_score`) and a blank line was added between the stdlib `import random` and the third-party `import streamlit`; in `tests/test_game_logic.py` the single-line import names were alphabetized. After applying, `ruff check` reported "All checks passed!" and all 10 pytest tests still passed.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

_Not attempted._ I only used one AI model (Claude Code) on this project, so there is no second model to compare against. Sections SF8, SF7, and SF9 above document the stretch work I actually completed.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

_Not attempted (single model used)._
