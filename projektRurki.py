import math

def gauss_legendre_integral(f, a, b):
    """
    Oblicza całkę funkcji f na przedziale [a, b] za pomocą metody Gaussa-Legendre.
    Węzły i wagi są ustalane ręcznie dla n = 2 lub n = 3.
    
    Parametry:
        f (function): Funkcja do scałkowania.
        a (float): Początek przedziału całkowania.
        b (float): Koniec przedziału całkowania.
    
    Zwraca:
        float: Przybliżona wartość całki.
    """
    
    # Węzły i wagi
    nodes = [-math.sqrt(3 / 5), 0, math.sqrt(3 / 5)]
    weights = [5 / 9, 8 / 9, 5 / 9]
    
    # Przekształć przedział z [a, b] na [-1, 1]
    transform = lambda x: 0.5 * (b - a) * x + 0.5 * (b + a)
    det_jacobian = 0.5 * (b - a)  # Pochodna transformacji (stała Jacobiana)
    
    # Oblicz sumę ważoną
    integral = 0
    for i in range(3):
        x_transformed = transform(nodes[i])
        integral += weights[i] * f(x_transformed)
    
    return integral * det_jacobian


def e(i, N):
    '''
    Tworzy funkcję ei(x) w zależności od danego N na przedziale [0, 2].
    Funkcja ei to funkcja, która jest równa 0 dla x-ów oprócz xi, dla którego jest równa 1.

    Parametry:
        i (int): Numer x-a.
        N (int): Łączna liczba podziałów.

    Zwraca:
        function: Funkcja ei(x) jako lambda.
    '''
    x_i = 2 * i / N
    next_x = x_i + 2 / N
    previous_x = x_i - 2 / N

    return lambda x: (
        0 if x >= next_x or x <= previous_x 
        else (x - previous_x) / (x_i - previous_x) if x > previous_x and x <= x_i 
        else 1 - (x - x_i) / (next_x - x_i)
    )

def e_prim(i, N):
    '''
    Tworzy funkcję e'(x) w zależności od danego N na przedziale [0, 2].
    Funkcja e' to pochodna funkcji e.

    Parametry:
        i (int): Numer x-a.
        N (int): Łączna liczba podziałów.

    Zwraca:
        function: Funkcja e'(x) jako lambda.
    '''
    x_i = 2 * i / N
    next_x = x_i + 2 / N
    previous_x = x_i - 2 / N

    # tbc


    
def E(x):
    if x<=1: return 2
    return 6

# def B(i,j, N):
#    4 * e(i, N, 0) * e(j, N, 0) - gauss_legendre_integral()