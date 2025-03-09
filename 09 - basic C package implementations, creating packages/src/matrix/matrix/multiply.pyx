cdef extern from "mult_matrix.c":
    ctypedef struct matrix_t:
        int rows
        int columns
        double matrix[100][100]

    void mult_matrix(matrix_t* A, matrix_t* B, matrix_t* result)

def mul(list matrix_a, list matrix_b):
    cdef matrix_t A, B, result
    cdef int i, j

    A.rows = len(matrix_a)
    A.columns = len(matrix_a[0]) if A.rows > 0 else 0
    for i in range(A.rows):
        for j in range(A.columns):
            A.matrix[i][j] = matrix_a[i][j]

    B.rows = len(matrix_b)
    B.columns = len(matrix_b[0]) if B.rows > 0 else 0
    for i in range(B.rows):
        for j in range(B.columns):
            B.matrix[i][j] = matrix_b[i][j]

    if A.rows == 0 or B.columns == 0 or A.columns != B.rows:
        raise ValueError("Matrix dimensions are invalid or incompatible for multiplication")

    mult_matrix(&A, &B, &result)

    result_list = []
    for i in range(result.rows):
        row = []
        for j in range(result.columns):
            row.append(int(result.matrix[i][j]))
        result_list.append(row)

    return result_list
