import pytest
import re
from calculator import add, sub, mul, div  # Assuming calculator module exports these

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

    with pytest.raises(TypeError, match=re.escape("Arguments must be numbers (int or float)")):
        add('a', 4)

def test_sub():
    assert sub(5, 3) == 2
    assert sub(0, 7) == -7
    assert sub(-3, -3) == 0

    with pytest.raises(TypeError, match=re.escape("Arguments must be numbers (int or float)")):
        sub('a', 4)

def test_mul():
    assert mul(2, 3) == 6
    assert mul(-1, 3) == -3
    assert mul(0, 10) == 0

    with pytest.raises(TypeError, match=re.escape("Arguments must be numbers (int or float)")):
        mul('a', 4)

def test_div():
    assert div(6, 2) == 3
    assert div(-9, 3) == -3
    assert div(10, 5) == 2

    with pytest.raises(TypeError, match=re.escape("Arguments must be numbers (int or float)")):
        div('a', 4)

    with pytest.raises(ZeroDivisionError):
        div(5, 0)
