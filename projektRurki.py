import math
import matplotlib.pyplot as plt
import numpy as np

N = 7
def get_N():
    print("Wprowadź N\n")
    global N
    N = input()

def gauss_legendre_integral(f, a, b):
    """
    Oblicza całkę funkcji f na przedziale [a, b] za pomocą metody Gaussa-Legendre.
    
    Parametry:
        f (function): Funkcja do scałkowania.
        a (float): Początek przedziału całkowania.
        b (float): Koniec przedziału całkowania.
    
    Zwraca:
        float: Przybliżona wartość całki.
    """
    
    # Węzły i wagi
    nodes, weights = np.polynomial.legendre.leggauss(5)

    
    # Przekształcenie przedziału z [a, b] na [-1, 1]
    transform = lambda x: 0.5 * (b - a) * x + 0.5 * (b + a)
    det_jacobian = 0.5 * (b - a)  # Pochodna transformacji (stała Jacobiana)
    
    # Obliczenie sumy ważonej
    integral = 0
    for i in range(5):
        x_transformed = transform(nodes[i])
        integral += weights[i] * f(x_transformed)

    
    print(integral*det_jacobian)
    
    return integral * det_jacobian

def inverse_matrix(A):
    # gauss-jordan
    # założenie takie, że jest to macierz kwadratowa

    def switch_rows(A, IA, i, j):
        for k in range(N):
            A[i][k], A[j][k] = A[j][k], A[i][k]
            IA[i][k], IA[j][k] = IA[j][k], IA[i][k]

    def multiply_row(A, IA, i):
        switch = i
        while A[i][i]==0:
            switch+=1
            if A[switch][i] != 0: switch_rows(A, IA, i, switch)

        k = 1 / A[i][i]
        for j in range(N):
            A[i][j] *= k
            IA[i][j] *= k
    
    def substract_row(A, IA, i, j):
        k = A[j][i]
        for t in range(N):
            A[j][t] -= A[i][t] * k
            IA[j][t] -= IA[i][t] * k
        
    IA = [[int(i==j) for i in range(N)] for j in range(N)]

    for i in range(N):
        multiply_row(A, IA, i)
        for j in range(i+1, N):
            substract_row(A, IA, i, j)
    for i in range(N-1, 0, -1):
        for j in range(i-1, -1, -1):
            substract_row(A, IA, i, j)

    return IA

def e(i, x):
    '''
    Wylicza wartość ei(x) w zależności od danego N na przedziale [0, 2].
    Funkcja ei to funkcja, która jest równa 0 dla x-ów oprócz xi, dla którego jest równa 1.

    Parametry:
        i (int): Numer x-a.
        x (float): x dla którego wyliczana jest ta funkcja

    Zwraca:
        float: Wartość funkcji ei(x).
    '''
    x_i = 2 * i / N
    next_x = x_i + 2 / N
    previous_x = x_i - 2 / N

    return (
        0 if x >= next_x or x <= previous_x 
        else (x - previous_x) / (x_i - previous_x) if x > previous_x and x <= x_i 
        else 1 - (x - x_i) / (next_x - x_i)
    )
    
def e_prim(i, x):
    '''
    Wylicza wartość e'(x) w zależności od danego N na przedziale [0, 2].
    Funkcja e' to pochodna funkcji e.

    Parametry:
        i (int): Numer x-a.
        x (float): x dla którego wyliczana jest ta funkcja

    Zwraca:
        float: Wartość funkcji e'(x).
    '''
    x_i = 2 * i / N
    next_x = x_i + 2 / N
    previous_x = x_i - 2 / N

    return (
        0 if x >= next_x or x <= previous_x 
        else 1 / (x_i - previous_x) if x > previous_x and x <= x_i 
        else 1 / (x_i - next_x)
    )
    
def E(x):
    if x<=1: return 2
    return 6

def integral(f):
    return gauss_legendre_integral(f, 0, 1) + gauss_legendre_integral(f, 1, 2)

def B(i, j): 
    return 4 * e(i, 0) * e(j, 0) - integral(
        lambda x: E(x) * e_prim(i, x) * e_prim(j , x)
    )
    
def L(i):
    return 8 * e(i, 0) + 1000 * integral(
        lambda x: e(i, x) * math.sin(math.pi * x)
    )

def matrix_multiplication(A, B):
    # zakładamy że A jest kwadratowa o długości N
    # a B jest o wymiarach 1 x N
    # więc wynik jest listą o długości N

    result = [0 for _ in range(N)]

    for i in range(N):
        for j in range(N):
            result[i] += A[i][j] * B[j]
    
    return result

def final_result(A, x):
    # A - tablica o długości N z alfami
    res = 3
    for i in range(N):
        res += A[i] * e(i,x)
    return res

B = [[B(i,j) for i in range(N)] for j in range(N)]
L = [L(i) for i in range(N)]

for i in range(N):
    print(B[i])

alfas = matrix_multiplication(inverse_matrix(B), L)

# Tworzymy zakres wartości x
x = [i*0.01 for i in range(201)]  # 200 punktów od 0 do 2

# Obliczamy wartości funkcji
y = [final_result(alfas, x[i]) for i in range(201)]

# Rysowanie wykresu
plt.plot(x, y, label='y = u(x)', color='blue', linestyle='-', linewidth=2)

# Dodanie opisu osi i tytułu
plt.title("Wykres funkcji")
plt.xlabel("x")
plt.ylabel("y")

# Dodanie siatki
plt.grid(True)

# Dodanie legendy
plt.legend()

# Wyświetlenie wykresu
plt.show()

