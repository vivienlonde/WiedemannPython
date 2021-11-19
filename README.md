# WiedemannPython
GF(2) Wiedemann algorithm to solve a sparse linear system

## Wie86's first reduction to the invertible square case

### Singular square case

If we apply the algorithm to a singular square matrix and it doesn't return a solution, it produces a linear combination between columns -> one column is eliminated and we iterate with the smaller (non square) matrix.

### Non square case

The non square case is reduced to the square case by considering one row (if A has more rows than columns) or one column (if A has more columns than rows) to be the "b" of the algorithm.
In every case, this gives a linear combination -> one row (or one colmn) is eliminated and we iterate.

### For our needs

Let's define m = nb_rows_A, n = nb_columns_A, r = rank_A.
With this approach,  the algorithm is run (n-r) + (m-r) + 1 times. This is too much if we apply it to the full local parity-check matrix.
Is it possible to use the full chain complex to reduce the local parity-check matrix upfront?

## Wie86's better approach

Instead of reducing A to an (r, r) square invertible matrix, it is possible to add random elements to A and extend it to a (max(m,n), max(m,n)) square matrix. This matrix is invertible with high probability. A solution to the extended problem leads to a solution to the original problem.



