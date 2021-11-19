import random

def sparse_matrix_by_dense_vector_multiplication(A, b):
    result = []
    for row in A:
        result_entry = False
        for j in row:
            if b[j]:
                result_entry = not(result_entry)
        result.append(result_entry)
    return result

def sequence_of_iterates(A, b, nb_of_iterates):
    result = []
    for i in range(nb_of_iterates):
        if i==0:
            result.append(b)
        else:
            last_element = result[-1]
            new_element = sparse_matrix_by_dense_vector_multiplication(A, last_element)
            result.append(new_element)
    return result


def dot_product(u, v):
    result =  False
    for bool_u, bool_v in zip(u, v):
        result ^= (bool_u and bool_v)
    return result 

def update(C, B, m): 
    Lc = len(C)
    for i_B, b in enumerate(B):
        i_C = i_B + m
        if i_C < Lc:
            C[i_C] ^= b
            # what is the complexity of accessing an element in a list? logarithmic or linear?
            # If access is linear, it makes the complexity of update quadratic whereas it should be linear. 
        else:
            C.append(b)
                
def Berlekamp_Massey(seq):
    
    C = [True]                 ### C is the returned list of linear feedbacks.
    B = [True]                 ### B is a copy of the last shortest-than-it-is-now value of C. This value must be stored because it is used to update C.
    L = 0                      ### L is len(C)-1
    m = 1                      ### m is the number of iteration since the length of C changed.
                               ### m is also the index of the last value of seq that we know C generates correctly minus the the index of the last value of seq that B generates correctly.
    # print('L:', L)
    # print('C:', C)
    # print('B:', B)
    # print('m:', m)
    # print()
        
    for n in range(len(seq)):
        # print('n:', n)
        # print('C:', C)
        if n-L-1<0:
            seq_slice = seq[n::-1]
        else:
            seq_slice = seq[n:n-L-1:-1]
        # print('seq_slice:', seq_slice)
        d = dot_product(C, seq_slice)
        # print('d:', d)
        # print('L:', L)
        
        if not(d):
            # print('case d=0')
            m += 1
        elif 2*L <= n:
            # print('case d=1 and 2L \leq n -> increments the length of C.')
            T = C.copy()
            update(C, B, m) # modifies C in-place.
            L = n + 1 - L
            B = T 
            m = 1
        else:
            # print("case d=1 and 2L > n -> doesn't increment the length of C.")
            update(C, B, m) # modifies C in-place.
            m += 1
        # print('L:', L)
        # print('C:', C)
        # print('B:', B)
        # print('m:', m)
        # print()
    
    return C

def verify_LFSR(seq, C):
    for i in range(len(seq)-len(C)+1):
        if dot_product(reversed(C), seq[i:i+len(C)]):
            print("C doesn't generate seq :(")
            return
    print("C generates seq :)")


def is_zero(b):
    for b_entry in b:
        if b_entry:
            return False
    return True   
   
def solve_system(A, b):
    
    nb_rows = len(A)
    # nb_columns = len(b) # it is assumed for now that nb_rows == nb_columns
    
    bk = b.copy()
    y = [False for _ in range(nb_rows)]
    d = 0
    
    while not is_zero(bk):
        
        seq_vectors = sequence_of_iterates(A, bk, 2*(nb_rows-d))
        u = [bool(random.randint(0, 1)) for _ in range(nb_rows)]
        # print('u:', u)
        seq_scalars = [dot_product(u, v) for v in seq_vectors]
        C = Berlekamp_Massey(seq_scalars)
        # print('C:', C)
        
        ## add C(A)b to y
        # print('reversed(C[:-1])', list(reversed(C[:-1])))
        # print('seq_vectors[:len(C)-1]', seq_vectors[:len(C)-1])
        for c, s in zip(reversed(C[:-1]), seq_vectors[:len(C)-1]):
            if c:
                update(y, s, 0) # bitwise XOR s to y. (y is modified in-place)
        # print('y:', y)
        
        bk = sparse_matrix_by_dense_vector_multiplication(A, y)
        update(bk, b , 0) # bitwise XOR b to bk. (bk is modified in-place)
        # print('bk:', bk)
        
        d += len(C)-1
        # print('d:', d)
        
        # print()
    
    return y
    
 

def main():
    ########### square matrix for now.
    row1 = [0, 2]
    row2 = [0, 1, 2]
    row3 = [0, 1, 2]
    A = [row1, row2, row3]
    b = [False, True, True]
    
    ########### test sparse_matrix_by_dense_vector_multiplication
    # A_times_b = sparse_matrix_by_dense_vector_multiplication(A, b)
    # print(A_times_b)
    
    ########### test sequence_of_iterates
    # nb_of_iterates = 6
    # six_iterates = sequence_of_iterates(A, b, nb_of_iterates)
    # print(six_iterates)
    
    ########### test dot_product
    # u = [True, False]
    # v = [True, True]
    # b = dot_product(u, v)
    # print(b)
    
    ########### test update
    # C = [True, False, True, True]
    # B = [False, True]
    # m = 3
    # update(C, B, m)
    # print(C)
    
    ########### test Berlekemp_Massey
    # seq = [True, False, True, True, False, False, True, False, False]
    # C = Berlekamp_Massey(seq)
    # print('seq:', seq)
    # print('C:', C)
    # verify_LFSR(seq, C)
    
    ########### test solve_system
    y = solve_system(A, b)
    print(y)

    
if __name__ == '__main__':
    main()


