#include <stdio.h>

typedef struct {
    int rows;
    int columns;
    double matrix[10][10];
} matrix_t;

void mult_matrix(matrix_t *A, matrix_t *B, matrix_t *result) {
    if (A->rows <= 0 || A->columns <= 0 || B->rows <= 0 || B->columns <= 0) {
        fprintf(stderr, "Error: Invalid matrix dimensions\n");
        return;
    }
    if (A->columns != B->rows) {
        fprintf(stderr, "Error: Incompatible matrix dimensions\n");
        return;
    }
    for (int i = 0; i < A->rows; i++) {
        for (int j = 0; j < B->columns; j++) {
            result->matrix[i][j] = 0;
            for (int k = 0; k < A->columns; k++) {
                result->matrix[i][j] += A->matrix[i][k] * B->matrix[k][j];
            }
        }
    }
    result->rows = A->rows;
    result->columns = B->columns;
}
