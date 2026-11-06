"""Pure poker hand evaluation logic.

Extracted from game.py to make evaluation testable independently
of the CLI (click) and I/O. All functions here are pure: given the
same cards, they always return the same result.
"""
from collections import Counter


def _rank_to_value(rank: str) -> int:
    """Convert a rank symbol ('2'..'10','J','Q','K','A') to a comparable int."""
    if rank == "A":
        return 14
    if rank == "K":
        return 13
    if rank == "Q":
        return 12
    if rank == "J":
        return 11
    if rank in ("T", "10"):
        return 10
    return int(rank)


def evaluate_hand(cards: list[str]) -> str:
    """Return the rank name of a 5-card poker hand.

    Correctly handles all 10 categories, including Royal Flush,
    Straight Flush (with proper consecutive-rank detection) and
    the Wheel straight (A-2-3-4-5).

    Raises ValueError if not exactly 5 cards.
    """
    if len(cards) != 5:
        raise ValueError(f"Expected 5 cards, got {len(cards)}")

    ranks = [_rank_to_value(c[:-1]) for c in cards]
    suits = [c[-1] for c in cards]
    ranks_sorted = sorted(ranks)

    is_flush = len(set(suits)) == 1
    is_wheel = set(ranks) == {14, 2, 3, 4, 5}
    is_straight = (
        len(set(ranks)) == 5 and ranks_sorted[-1] - ranks_sorted[0] == 4
    ) or is_wheel

    counts = sorted(Counter(ranks).values(), reverse=True)

    if is_straight and is_flush:
        if ranks_sorted == [10, 11, 12, 13, 14]:
            return "Royal Flush"
        return "Straight Flush"
    if counts == [4, 1]:
        return "Four of a Kind"
    if counts == [3, 2]:
        return "Full House"
    if is_flush:
        return "Flush"
    if is_straight:
        return "Straight"
    if counts == [3, 1, 1]:
        return "Three of a Kind"
    if counts == [2, 2, 1]:
        return "Two Pair"
    if counts == [2, 1, 1, 1]:
        return "One Pair"
    return "High Card"
