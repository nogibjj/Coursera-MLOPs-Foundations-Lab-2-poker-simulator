"""Tests for the pure poker hand evaluator."""
import pytest
from poker.hand_evaluator import evaluate_hand


@pytest.mark.parametrize(
    "cards,expected",
    [
        (["10H", "JH", "QH", "KH", "AH"], "Royal Flush"),
        (["9H", "10H", "JH", "QH", "KH"], "Straight Flush"),
        (["10H", "10D", "10C", "10S", "AH"], "Four of a Kind"),
        (["10H", "10D", "10C", "AH", "AD"], "Full House"),
        (["2H", "5H", "8H", "JH", "KH"], "Flush"),
        (["9H", "10D", "JC", "QH", "KH"], "Straight"),
        (["10H", "10D", "10C", "KH", "AH"], "Three of a Kind"),
        (["10H", "10D", "JH", "JS", "KH"], "Two Pair"),
        (["10H", "10D", "JC", "QH", "KH"], "One Pair"),
        (["2H", "5D", "8C", "JH", "KH"], "High Card"),
    ],
)
def test_all_hand_ranks(cards, expected):
    assert evaluate_hand(cards) == expected


# --- Regression tests: these catch bugs in the original implementation ---


def test_royal_flush_is_not_straight_flush():
    """Original bug: lexicographic sorted() never matched '10' + 'A' endpoints."""
    assert evaluate_hand(["AH", "KH", "QH", "JH", "10H"]) == "Royal Flush"


def test_flush_with_distinct_ranks_is_not_straight_flush():
    """Original bug: any flush with 5 distinct ranks was 'Straight Flush'."""
    assert evaluate_hand(["2H", "5H", "8H", "JH", "KH"]) == "Flush"


def test_high_card_with_distinct_ranks_is_not_straight():
    """Original bug: any 5 distinct ranks were classified as 'Straight'."""
    assert evaluate_hand(["2H", "5D", "8C", "JH", "KH"]) == "High Card"


def test_two_pair_is_not_three_of_a_kind():
    """Original bug: two pair was classified as 'Three of a Kind'."""
    assert evaluate_hand(["10H", "10D", "JH", "JS", "KH"]) == "Two Pair"


def test_full_house_is_not_four_of_a_kind():
    """Original bug: full house was classified as 'Four of a Kind'."""
    assert evaluate_hand(["10H", "10D", "10C", "AH", "AD"]) == "Full House"


def test_wheel_straight_ace_low():
    """A-2-3-4-5 is a straight, with ace counting low."""
    assert evaluate_hand(["AH", "2D", "3C", "4S", "5H"]) == "Straight"


def test_wheel_straight_flush():
    """A-2-3-4-5 of the same suit is a Straight Flush (but not Royal)."""
    assert evaluate_hand(["AH", "2H", "3H", "4H", "5H"]) == "Straight Flush"


def test_invalid_card_count_raises():
    with pytest.raises(ValueError):
        evaluate_hand(["AH", "KH"])
