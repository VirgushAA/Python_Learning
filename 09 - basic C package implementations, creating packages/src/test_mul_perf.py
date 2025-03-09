import time
from itertools import tee
from matrix import mul


def mull(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]


def main():
    x = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    y = [[1, 2], [1, 2], [3, 4]]

    start = time.time()
    result = mull(x, y)
    end = time.time()
    print(f"Python mull result: {result} and execution time: {end - start:.6f} seconds")

    start = time.time()
    result = mul(x, y)
    end = time.time()
    print(f"Cython mul result: {result} and execution time: {end - start:.6f} seconds")


if __name__ == '__main__':
    main()
