from logic_utils import HINT_MESSAGES, check_guess, parse_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# FIX: New test targeting the backwards-hint bug. A "Too High" guess must advise
# going LOWER, and a "Too Low" guess must advise going HIGHER.
def test_too_high_hint_advises_going_lower():
    outcome = check_guess(60, 50)  # guess is too high
    assert "LOWER" in HINT_MESSAGES[outcome].upper()

def test_too_low_hint_advises_going_higher():
    outcome = check_guess(40, 50)  # guess is too low
    assert "HIGHER" in HINT_MESSAGES[outcome].upper()


# --- Stretch Challenge 1: Advanced Edge-Case Testing ---
# These verify parse_guess handles unusual inputs gracefully instead of crashing.

def test_parse_negative_number():
    # A negative number is still a valid integer and should parse cleanly.
    ok, value, err = parse_guess("-5")
    assert ok is True and value == -5 and err is None

def test_parse_decimal_is_truncated():
    # Decimals should not crash; they truncate to an int.
    ok, value, err = parse_guess("3.9")
    assert ok is True and value == 3 and err is None

def test_parse_very_large_number():
    # Extremely large values should parse without overflow (Python ints are unbounded).
    ok, value, err = parse_guess("100000000000000000000")
    assert ok is True and value == 100000000000000000000 and err is None

def test_parse_non_numeric_is_rejected():
    # Letters should be rejected with a friendly error, not an exception.
    ok, value, err = parse_guess("abc")
    assert ok is False and value is None and err == "That is not a number."

def test_parse_empty_string_is_rejected():
    # An empty submission should prompt the user, not crash.
    ok, value, err = parse_guess("")
    assert ok is False and value is None and err == "Enter a guess."
