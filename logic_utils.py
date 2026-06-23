"""Core game logic for the Game Glitch Investigator guessing game.

# FIX: Refactored these four functions out of app.py into logic_utils.py with my
# AI coding assistant (Claude Code) so the game logic can be unit-tested
# independently of the Streamlit UI.
"""


def get_range_for_difficulty(difficulty: str):
    """Return the (low, high) inclusive guessing range for a difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret and return the outcome string.

    Returns one of: "Win", "Too High", "Too Low".

    # FIX: The original code in app.py flipped the secret to a string on even
    # attempts, which broke the comparison. With that state bug removed, both
    # guess and secret are always ints, so this is a clean numeric comparison.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


# FIX: The original messages were backwards ("Too High" told the player to go
# HIGHER). These are now correct: too high -> go lower, too low -> go higher.
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
