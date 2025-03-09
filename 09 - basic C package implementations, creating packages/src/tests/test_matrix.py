import pytest
from matrix import mul

def test_matrix_multiplication():
    A = [[1, 2], [3, 4]]
    B = [[2, 0], [1, 2]]
    expected_result = [[4, 4], [10, 8]]

    assert mul(A, B) == expected_result

def test_matrix_incompatible_sizes():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[1, 2], [3, 4]]  # Invalid, should be (3xN) to multiply with A (2x3)

    with pytest.raises(ValueError, match="Matrix dimensions are invalid or incompatible for multiplication"):
        mul(A, B)

def test_empty_matrix():
    A = []
    B = [[1, 2], [3, 4]]

    with pytest.raises(ValueError, match="Matrix dimensions are invalid or incompatible for multiplication"):
        mul(A, B)

    A = [[1, 2], [3, 4]]
    B = []

    with pytest.raises(ValueError, match="Matrix dimensions are invalid or incompatible for multiplication"):
        mul(A, B)
