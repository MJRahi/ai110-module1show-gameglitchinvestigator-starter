# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game it *looked* fine — the title, difficulty sidebar, guess box, and the "Developer Debug Info" panel all rendered — but it was effectively unplayable. Even with the secret number visible in the debug panel, I couldn't reliably win, the "Higher/Lower" hints pointed me the wrong way, and starting a "New Game" after a loss left me stuck. Here are the concrete bugs I noticed, with what I expected vs. what actually happened:

- **Secret value flip-flops to a string on even attempts.** I expected the secret to stay a fixed integer for the whole game so my guesses could be compared against it. Instead, on every even-numbered attempt the code did `secret = str(st.session_state.secret)`, so my integer guess was compared to a *string* (e.g. `42` vs `"42"`). That comparison fell into the `TypeError` branch of `check_guess` and did a lexicographic string comparison, which made winning impossible on even attempts and made the hints nonsensical. This is why the secret "seemed to change every time I clicked Submit."
- **The Higher/Lower hint message is backwards.** I expected that guessing too high would tell me to go LOWER. Instead, `check_guess` pairs the `"Too High"` outcome with the message `"📈 Go HIGHER!"` (and `"Too Low"` with `"📉 Go LOWER!"`), so the advice always points the wrong direction.
- **"New Game" doesn't fully reset the state.** I expected the New Game button to start a completely fresh game. Instead it only reset `attempts` and `secret`, leaving `score`, `status`, and `history` stale — so after a win or loss the app stayed stuck on the "Game over"/"You already won" screen.
- **(Supporting bug) `attempts` started at `1` instead of `0`.** This made the "Attempts left" counter off by one from the very first render.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `60` when the secret is `50` (odd attempt) | "Too High" hint that advises going LOWER | Shows "📈 Go HIGHER!" — advice is backwards | none |
| Guess the exact secret (e.g. `42`) on the 2nd (even) attempt | "🎉 Correct!" / a Win | Not counted as a win; the secret is compared as the string `"42"` against the integer `42` | none (the `TypeError` is silently caught inside `check_guess`) |
| Click "New Game 🔁" after the game is already over | Fresh game: score reset to 0, status back to "playing", empty history | Still shows the "Game over" screen; score and history are not reset | none |

---

## 2. How did you use AI as a teammate?

I used **Claude Code** (an AI coding assistant inside VS Code) as my main teammate on this project. I treated it like a pair-programmer: I described the symptoms I saw while playing, asked it to explain the suspicious lines, and then asked it to make targeted changes that I reviewed in the diff before accepting.

- **A correct suggestion.** When I pointed at the line `secret = str(st.session_state.secret)` and asked why the secret "changed" every Submit, the AI explained that converting the secret to a string on even attempts made my integer guess get compared to a string, which fell into the `TypeError` branch of `check_guess` and did a lexicographic comparison. It suggested removing that conversion so the comparison is always int-vs-int. I verified this by reading the new code, re-running the game, and confirming I could win on the 2nd attempt — and the new pytest cases for the hint outcomes passed.
- **A misleading suggestion.** When refactoring `check_guess` into `logic_utils.py`, the AI's first version kept returning a `(outcome, message)` tuple like the original. That looked reasonable, but it was wrong for this project because the existing tests in `tests/test_game_logic.py` assert `check_guess(50, 50) == "Win"` — a single string, not a tuple. I caught it by running `pytest`, which failed on the equality check. I corrected the design so `check_guess` returns just the outcome string and moved the (now-fixed) hint text into a separate `HINT_MESSAGES` map, after which all tests passed.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when I could confirm it two ways: an automated test that turned green, and seeing the correct behavior while actually playing the game. For example, after fixing the backwards Higher/Lower hint, I added two pytest cases — `test_too_high_hint_advises_going_lower` and `test_too_low_hint_advises_going_higher` — that assert a "Too High" guess maps to a message containing "LOWER" and a "Too Low" guess maps to "HIGHER". Running `python3 -m pytest tests/ -v` showed all 5 tests passing (the 3 starter tests plus my 2 new ones), which proved the hint mapping was finally correct. I also ran the app with Streamlit and played a full round to confirm the secret no longer "changes," the hints point the right way, and "New Game" fully resets the board. The AI helped by suggesting the simple, assertion-style test structure (compare the outcome and check the hint text), and by reminding me to keep each test small and focused on one behavior so a failure points straight at the bug.

---

## 4. What did you learn about Streamlit and state?

I learned that Streamlit re-runs your entire script from top to bottom every time the user interacts with the app — every button click, text entry, or checkbox toggle restarts the whole file. I'd explain it to a friend like this: imagine the program is a recipe that gets re-cooked from scratch the moment you touch anything, so any normal variable you created gets thrown away and rebuilt each time. The fix is `st.session_state`, which is like a small backpack that survives between re-runs — you put things you want to keep (the secret number, score, attempts, history) into the backpack, and you only fill it once using an `if "key" not in st.session_state` guard. This project drove the lesson home: the "secret keeps changing" feeling came from mishandling state (converting it to a string mid-game), and "New Game didn't reset" came from forgetting to clear *all* the values in that backpack.

---

## 5. Looking ahead: your developer habits

The habit I most want to reuse is **writing or running a small test before trusting a fix**. Pairing each bug fix with a focused pytest case (and then actually playing the game) caught a mistake the AI introduced and gave me real confidence the bug was gone, not just "looks fixed." A close second is the prompting strategy of pointing the AI at one specific line and asking "explain this step-by-step" instead of asking it to rewrite everything at once.

One thing I'd do differently next time is **review the AI's diff more carefully before accepting it** — the AI kept `check_guess` returning a tuple during the refactor, which silently broke the existing tests, and I only noticed when pytest failed. Checking the change against the existing tests *first* would have saved a round trip.

This project changed how I think about AI-generated code: I now treat it as a fast, knowledgeable teammate whose suggestions still need to be verified, not as an authority — the AI was confidently wrong at least once, and only my own tests and play-testing told me so.
