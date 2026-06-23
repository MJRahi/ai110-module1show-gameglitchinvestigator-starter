# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** It is a Streamlit number-guessing game: the app picks a secret number within a range that depends on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–200), and the player tries to guess it within a limited number of attempts, using "Too High / Too Low" hints and a running score.
- [x] **Detail which bugs you found.** (1) The secret was converted to a string on even attempts, so guesses were compared int-vs-string and the secret seemed to "change" every Submit; (2) the Higher/Lower hint messages were backwards; (3) "New Game" only reset `attempts` and `secret`, leaving stale `score`, `status`, and `history`; (4) `attempts` started at `1`, making "Attempts left" off by one. Full reproduction steps are in [reflection.md](reflection.md).
- [x] **Explain what fixes you applied.** Removed the string conversion so the secret stays an integer; corrected the hint mapping (`Too High → Go LOWER`, `Too Low → Go HIGHER`); made "New Game" reset score/status/history and regenerate the secret from the current difficulty range; initialized `attempts` to `0`; and refactored the core logic into `logic_utils.py` with passing pytest coverage.

## 📸 Demo Walkthrough

A sample game on Normal difficulty (secret = 50), following the fixed behavior end-to-end:

1. The app starts a new game and shows "Attempts left: 8". The secret (50) is visible in the "Developer Debug Info" panel.
2. User enters a guess of `40` → game returns **"Too Low"** with the hint **"📈 Go HIGHER!"** (advice now points the correct way).
3. User enters a guess of `70` → game returns **"Too High"** with the hint **"📉 Go LOWER!"**.
4. User enters a guess of `60` → still **"Too High → Go LOWER!"**; the score and attempt counter update after each guess.
5. User enters `50` → **"🎉 Correct!"**, balloons appear, and the game shows the final score and switches to the "won" state.
6. User clicks **"New Game 🔁"** → score resets to 0, status returns to "playing", history is cleared, and a fresh secret is drawn for the current difficulty.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python3 -m pytest tests/ -v
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0
collected 12 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  8%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 16%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 25%]
tests/test_game_logic.py::test_too_high_hint_advises_going_lower PASSED  [ 33%]
tests/test_game_logic.py::test_too_low_hint_advises_going_higher PASSED  [ 41%]
tests/test_game_logic.py::test_parse_negative_number PASSED              [ 50%]
tests/test_game_logic.py::test_parse_decimal_is_truncated PASSED         [ 58%]
tests/test_game_logic.py::test_parse_very_large_number PASSED            [ 66%]
tests/test_game_logic.py::test_parse_non_numeric_is_rejected PASSED      [ 75%]
tests/test_game_logic.py::test_parse_empty_string_is_rejected PASSED     [ 83%]
tests/test_game_logic.py::test_proximity_bullseye PASSED                 [ 91%]
tests/test_game_logic.py::test_proximity_far_guess_is_cold PASSED        [100%]

============================== 12 passed in 0.02s ===============================
```

## 🚀 Stretch Features

- [x] **Challenge 1 — Advanced Edge-Case Testing.** Added 5 edge-case pytest cases (negative numbers, decimals, very large values, non-numeric text, empty input) for `parse_guess`; all pass (see Test Results above). Prompts and reasoning are documented in [ai_interactions.md](ai_interactions.md) (SF7).
- [x] **Challenge 3 — Professional Documentation & Linting.** Added docstrings to every function in `logic_utils.py` and ran `ruff` for PEP 8 compliance; fixed the import-ordering issues it flagged. Details in [ai_interactions.md](ai_interactions.md) (SF9).
- [x] **Challenge 4 — Enhanced Game UI.** Added structured, user-friendly output without changing the core game logic:
  - **Hot/Cold proximity emojis** — a new `proximity_label(guess, secret, low, high)` helper in [logic_utils.py](logic_utils.py) reports how close each guess is (🎯 Bullseye → 🔥 Burning hot → ♨️ Hot → 🙂 Warm → ❄️ Cold → 🧊 Freezing), scaled to the difficulty's range. Shown after each guess in `app.py`.
  - **Color-coded hints** — in the submit block of [app.py](app.py), the hint is rendered green on a win (`st.success`), red when too high (`st.error`), and blue when too low (`st.info`) instead of a single yellow warning.
  - **Session summary table** — `app.py` now stores each attempt as a structured row and renders a `st.table` "📋 Session Summary" (Attempt, Guess, Result, Hint, Proximity) at the bottom of the page.
  - Covered by two new tests (`test_proximity_bullseye`, `test_proximity_far_guess_is_cold`).
