from math import sin, pi 
import matplotlib.pyplot as plt
from scipy.integrate import quad as integration
import copy

N = 15
def get_N():
    print("Wprowadź N: ")
    global N
    N = int(input())

def inverse_matrix(A):
    '''
    Odwraca macierz A za pomocą algorytmu Gaussa-Jordana.
    Zakładamy, że A jest macierzą kwadratową i że można ją odwrócić (det(A) != 0).

    Parametry:
        A (float[][]): Macierz do odwrócenia

    Zwraca:
        IA (float[][]): Odwrócona macierz A
    '''

    A = copy.deepcopy(A)
    IA = [[1 if i == j else 0 for i in range(N)] for j in range(N)]

    def switch_rows(A, IA, i, j):
        A[i], A[j] = A[j], A[i]
        IA[i], IA[j] = IA[j], IA[i]

    for i in range(N):
        if A[i][i] == 0:
            for k in range(i + 1, N):
                if A[k][i] != 0:
                    switch_rows(A, IA, i, k)
                    break
            else:
                raise ValueError("Macierz jest osobliwa i nie można jej odwrócić.")
        
        diag = A[i][i]
        for j in range(N):
            A[i][j] /= diag
            IA[i][j] /= diag

        for k in range(N):
            if k != i:
                factor = A[k][i]
                for j in range(N):
                    A[k][j] -= factor * A[i][j]
                    IA[k][j] -= factor * IA[i][j]

    return IA

def matrix_multiplication(A, B):
    '''
    Mnoży macierz A z macierzą B.
    Zakładamy, że można to zrobić.

    Parametry:
        A (float[][]): Macierz do przemnożenia przez macież B
        B (float[][]): Druga macierz

    Zwraca:
        result (float[][]): Wynik mnożenia
    '''

    result = [0 for _ in range(N)]

    for i in range(N):
        for j in range(N):
            result[i] += A[i][j] * B[j]
    
    return result

def e(i, x):
    '''
    Wylicza wartość e_i(x) w zależności od danego N na przedziale [0, 2].
    Funkcja e_i to funkcja, która jest równa 0 dla x-ów oprócz xi, dla którego jest równa 1.

    Parametry:
        i (int): Numer x-a.
        x (float): x dla którego wyliczana jest ta funkcja

    Zwraca:
        float: Wartość funkcji e_i(x).
    '''
    H = 2/N
    x_i = H * i
    next_x = H * (i+1)
    previous_x = H * (i-1)

    return (
        0 if x >= next_x or x <= previous_x 
        else (x - previous_x) / (x_i - previous_x) if x > previous_x and x <= x_i 
        else 1 - (x - x_i) / (next_x - x_i)
    )
    
def e_prim(i, x):
    '''
    Wylicza wartość e_i'(x) w zależności od danego N na przedziale [0, 2].
    Funkcja e_i' to pochodna funkcji e_i.

    Parametry:
        i (int): Numer x-a.
        x (float): x dla którego wyliczana jest ta funkcja

    Zwraca:
        float: Wartość funkcji e_i'(x).
    '''
    H = 2/N
    x_i = H * i
    next_x = H * (i+1)
    previous_x = H * (i-1)

    return (
        0 if x >= next_x or x <= previous_x 
        else N/2 if x <= x_i 
        else -N/2
    )
    
def E(x):
    if x<=1: return 2
    return 6

def B(i, j): 
    y, err = integration(lambda x: E(x)*e_prim(i,x)*e_prim(j,x), 0, 2, limit = 100)
    return 4*e(i, 0)*e(j, 0) - y
    
def L(i):
    y, err = integration(lambda x: e(i, x) * sin(pi * x), 0, 2, limit = 100)
    return 8 * e(i, 0) + 1000 * y

def final_result(A, x):
    '''
    Oblicza wartość funkcji u(x).

    Parametry:
        A (float[][]): Macierz z alfami o długości N-1
        x (float): Wartość x-a dla którego wyliczamy wynik funkcji u(x) 

    Zwraca:
        res (float): Wynik funkcji u(x)
    '''
    res = 3
    for i in range(N):
        res += A[i] * e(i,x)
    return res

def get_alfas():
    matrix_B = [[B(j,i) for i in range(N)] for j in range(N)]
    matrix_L = [L(i) for i in range(N)]
    return matrix_multiplication(inverse_matrix(matrix_B), matrix_L)

def show_plot():
    alfas = get_alfas()
    x = [i*0.01 for i in range(201)]  # 201 punktów od 0 do 2
    y = [final_result(alfas, x[i]) for i in range(201)]
    plt.plot(x, y, label='y = u(x)', color='blue', linestyle='-', linewidth=2)
    plt.title("Wykres funkcji")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    get_N()
    # z testowania:
    # program najlepiej działa dla N <= 16
    # zaczyna robić dziwne rzeczy dla N >= 23
    # zaczyna wywalać błąd dla N >= 28
    show_plot()