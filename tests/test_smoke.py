"""Smoke tests: verifican que el paquete 'poker' se importa y funciona."""
from poker.game import deck_of_cards, full_name_suit


def test_deck_has_52_unique_cards():
    deck = deck_of_cards()
    assert len(deck) == 52
    assert len(set(deck)) == 52


def test_full_name_suit_hearts():
    assert full_name_suit("H") == "Hearts"
