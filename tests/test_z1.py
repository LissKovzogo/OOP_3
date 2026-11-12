import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Zadania')))
import pytest
from z_1 import  SmartNumber, create_finder


def test_smart_number_gt(capsys):

    a = SmartNumber(10)
    b = SmartNumber(5)
    assert (a > b) is True

    captured = capsys.readouterr()
    assert "[Перегрузка >]: Сравниваем 10 > 5" in captured.out


def test_smart_number_lt(capsys):

    a = SmartNumber(3)
    b = SmartNumber(8)
    assert (a < b) is True

    captured = capsys.readouterr()
    assert "[Перегрузка <]: Сравниваем 3 < 8" in captured.out


def test_smart_number_eq(capsys):

    a = SmartNumber(7)
    b = SmartNumber(7)
    c = SmartNumber(9)

    assert (a == b) is True
    assert (a == c) is False

    captured = capsys.readouterr()
    assert "[Перегрузка ==]: Проверяем 7 == 7" in captured.out


def test_smart_number_repr():

    num = SmartNumber(42)
    assert repr(num) == "42"
    assert str(num) == "42"

def test_finder_max_default(capsys):
    finder = create_finder()
    numbers = [SmartNumber(5), SmartNumber(12), SmartNumber(3), SmartNumber(8)]

    result = finder(numbers)

    assert result.value == 12
    captured = capsys.readouterr()
    assert "[Перегрузка >]: Сравниваем" in captured.out


def test_finder_min(capsys):
    finder = create_finder(type="min")
    numbers = [SmartNumber(5), SmartNumber(12), SmartNumber(3), SmartNumber(8)]

    result = finder(numbers)

    assert result.value == 3
    captured = capsys.readouterr()
    assert "[Перегрузка <]: Сравниваем" in captured.out


def test_finder_empty_list():
    finder_max = create_finder()
    finder_min = create_finder("min")

    assert finder_max([]) is None
    assert finder_min([]) is None


def test_closure_behavior(capsys):
    finder1 = create_finder("max")
    finder2 = create_finder("min")

    list1 = [SmartNumber(1), SmartNumber(10)]
    list2 = [SmartNumber(1), SmartNumber(10)]

    capsys.readouterr()

    assert finder1(list1).value == 10
    out_max = capsys.readouterr().out
    assert "[Перегрузка >]" in out_max
    assert "[Перегрузка <]" not in out_max

    assert finder2(list2).value == 1
    out_min = capsys.readouterr().out
    assert "[Перегрузка <]" in out_min
    assert "[Перегрузка >]" not in out_min