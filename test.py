A = [[1, 2], ['X', 'Y']]

B = A.copy()

print(A is B)

# False

print(A[0] is B[0])

# True

print(A[0][1] is B[0][1])

# True