"""Tests for the poker CLI and non-CLI helpers."""
from click.testing import CliRunner

from poker.game import (
    build_poker_hand,
    cli,
    deck_of_cards,
    display_poker_hand,
    evaluate_poker_hand,
    full_name_suit,
    play_poker_hand,
    simulate_hands,
)

# --- CLI: info ---


def test_info_lists_all_ranks():
    runner = CliRunner()
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    for hand in [
        "Royal Flush",
        "Straight Flush",
        "Four of a Kind",
        "Full House",
        "Flush",
        "Straight",
        "Three of a Kind",
        "Two Pair",
        "One Pair",
        "High Card",
    ]:
        assert hand in result.output


def test_info_probability_flag():
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "--probability"])
    assert result.exit_code == 0
    assert "1 in" in result.output


# --- CLI: deal ---


def test_deal_default_one_hand():
    runner = CliRunner()
    result = runner.invoke(cli, ["deal"])
    assert result.exit_code == 0
    assert result.output.count("Hand Rank:") == 1


def test_deal_multiple_hands():
    runner = CliRunner()
    result = runner.invoke(cli, ["deal", "--hands", "3"])
    assert result.exit_code == 0
    assert result.output.count("Hand Rank:") == 3


# --- CLI: play ---


def test_play_command_runs():
    runner = CliRunner()
    result = runner.invoke(cli, ["play", "--name", "Alice", "--bet", "5"])
    assert result.exit_code == 0
    # Winner is random, so accept any of the three outcomes
    assert any(msg in result.output for msg in ["Alice wins", "Alice loses", "tie"])


# --- CLI: interactive ---


def test_interactive_one_round():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["interactive", "--name", "Bob", "--rounds", "1", "--money", "100"],
        input="10\n",
    )
    assert result.exit_code == 0
    assert "Rounds: 1" in result.output
    assert "Money:" in result.output


# --- play_poker_hand: branches del ganador ---


def test_play_poker_hand_hand1_wins():
    royal = ["10H", "JH", "QH", "KH", "AH"]
    high = ["2H", "5D", "8C", "JH", "KH"]
    assert play_poker_hand(royal, high)["winner"] == "Hand 1"


def test_play_poker_hand_hand2_wins():
    royal = ["10H", "JH", "QH", "KH", "AH"]
    high = ["2H", "5D", "8C", "JH", "KH"]
    assert play_poker_hand(high, royal)["winner"] == "Hand 2"


def test_play_poker_hand_tie():
    two_pair_a = ["10H", "10D", "JH", "JS", "KH"]
    two_pair_b = ["9H", "9D", "QH", "QS", "KH"]
    assert play_poker_hand(two_pair_a, two_pair_b)["winner"] == "Tie"


# --- Helpers: cobertura de branches ---


def test_full_name_suit_all_suits():
    assert full_name_suit("H") == "Hearts"
    assert full_name_suit("D") == "Diamonds"
    assert full_name_suit("C") == "Clubs"
    assert full_name_suit("S") == "Spades"
    assert full_name_suit("X") == "Unknown"


def test_display_poker_hand_all_ranks():
    ranks = display_poker_hand()
    assert len(ranks) == 10
    assert ranks["Royal Flush"] == 10
    assert ranks["High Card"] == 1


def test_simulate_hands_count():
    hands = simulate_hands(deck_of_cards(), 5)
    assert len(hands) == 5
    assert all(len(h) == 5 for h in hands)


def test_build_poker_hand_examples_are_valid():
    """Cada ejemplo de build_poker_hand debe evaluarse a su propia etiqueta."""
    for rank_name, cards in build_poker_hand().items():
        assert evaluate_poker_hand(cards) == rank_name, (
            f"El ejemplo de '{rank_name}' evalúa como "
            f"'{evaluate_poker_hand(cards)}'"
        )
