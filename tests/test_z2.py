import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Zadania')))
import pytest

from z_2 import WordCard, Dictionary, MAX_SIZE


def test_wordcard_equality():
    card1 = WordCard("apple", "яблоко")
    card2 = WordCard("apple", "яблочко")  # Перевод другой, но слово то же
    card3 = WordCard("dog", "собака")

    assert card1 == card2
    assert card1 != card3


def test_wordcard_hash():
    card1 = WordCard("apple", "яблоко")
    card2 = WordCard("apple", "яблочко")
    card3 = WordCard("dog", "собака")

    cards_set = {card1, card2, card3}
    assert len(cards_set) == 2


def test_wordcard_repr():
    card = WordCard("cat", "кошка")
    assert repr(card) == "WordCard('cat', 'кошка')"

def test_dictionary_init():
    d = Dictionary()
    assert d.name == "Новый словарь"
    assert d.size == MAX_SIZE
    assert d.count == 0
    assert len(d._cards) == 0


def test_dictionary_from_string():
    d = Dictionary.from_string("Test", "dog:пес, cat:кошка, bird:птица")
    assert d.count == 3
    assert d.search("dog") == "пес"
    assert d.search("bird") == "птица"


def test_dictionary_change_name():
    d = Dictionary("Старое имя")
    d.change_name("Новое имя")
    assert d.name == "Новое имя"


def test_add_card_no_duplicates():
    d = Dictionary()
    d.add_card(WordCard("apple", "яблоко"))
    d.add_card(WordCard("apple", "яблочко"))  # Дубль по слову

    assert d.count == 1


def test_add_card_overflow():
    d = Dictionary()
    d.size = 2
    d.add_card(WordCard("a", "1"))
    d.add_card(WordCard("b", "2"))

    with pytest.raises(OverflowError):
        d.add_card(WordCard("c", "3"))


def test_remove_card():
    d = Dictionary()
    d.add_card(WordCard("apple", "яблоко"))
    d.add_card(WordCard("dog", "собака"))

    result = d.remove_card("apple")
    assert result is True
    assert d.count == 1
    assert d.search("apple") is None

    result_fail = d.remove_card("unknown")
    assert result_fail is False
    assert d.count == 1


def test_search():
    d = Dictionary()
    d.add_card(WordCard("apple", "яблоко"))

    assert d.search("apple") == "яблоко"
    assert d.search("banana") is None


def test_size_method():
    d = Dictionary()
    assert d.size_method() == MAX_SIZE

def test_getitem():
    d = Dictionary()
    d.add_card(WordCard("apple", "яблоко"))

    assert d["apple"] == "яблоко"

    with pytest.raises(KeyError):
        _ = d["banana"]  # Должно вызвать ошибку


def test_setitem():
    d = Dictionary()

    d["dog"] = "собака"
    assert d.search("dog") == "собака"
    assert d.count == 1

    d["dog"] = "пёс"
    assert d.search("dog") == "пёс"
    assert d.count == 1

def test_union_operator():
    d1 = Dictionary("D1")
    d1.add_card(WordCard("apple", "яблоко"))
    d1.add_card(WordCard("dog", "собака"))

    d2 = Dictionary("D2")
    d2.add_card(WordCard("dog", "пес"))  # Пересекающееся слово
    d2.add_card(WordCard("cat", "кошка"))

    union_dict = d1 | d2

    assert union_dict is not d1 and union_dict is not d2
    assert union_dict.name == "D1 | D2"
    assert union_dict.count == 3
    assert d1.count == 2
    assert d2.count == 2


def test_intersection_operator():
    d1 = Dictionary("D1")
    d1.add_card(WordCard("apple", "яблоко"))
    d1.add_card(WordCard("dog", "собака"))

    d2 = Dictionary("D2")
    d2.add_card(WordCard("dog", "пес"))
    d2.add_card(WordCard("cat", "кошка"))

    intersection_dict = d1 & d2

    assert intersection_dict.name == "D1 & D2"
    assert intersection_dict.count == 1
    assert intersection_dict.search("dog") is not None
    assert intersection_dict.search("apple") is None


def test_subtraction_operator():
    d1 = Dictionary("D1")
    d1.add_card(WordCard("apple", "яблоко"))
    d1.add_card(WordCard("dog", "собака"))

    d2 = Dictionary("D2")
    d2.add_card(WordCard("dog", "пес"))
    d2.add_card(WordCard("cat", "кошка"))

    sub_dict = d1 - d2

    assert sub_dict.name == "D1 - D2"
    assert sub_dict.count == 1
    assert sub_dict.search("apple") is not None
    assert sub_dict.search("dog") is None


def test_operator_not_implemented():
    d = Dictionary()
    with pytest.raises(TypeError):
        _ = d | "строка"