import math

def gauss_legendre_integral_manual(f, a, b):
    """
    Oblicza całkę funkcji f na przedziale [a, b] za pomocą metody Gaussa-Legendre.
    Węzły i wagi są ustalane ręcznie dla n = 2 lub n = 3.
    
    Parametry:
        f (function): Funkcja do scałkowania.
        a (float): Początek przedziału całkowania.
        b (float): Koniec przedziału całkowania.
        n (int): Liczba węzłów Gaussa (obsługiwane: 2, 3).
    
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


def e_i(i, N, x):
    '''
    Oblicza wartość funkcji ei(x) w zależności od danego N na przydziale [0,2].
    Funkcja ei to funkcja która jest równa 0 dla x-ów oprócz xi, dla którego jest równa 1.

    Parametry:
        i (int): Numer x-a.
        N (int): Łączna ilość podziałów.
        x (float): Wartość dla której jest obliczona ta funkcja.

    Zwraca:
        float: wynik ei(x).
    '''
    
    # Przypadek dla i=0
    if i==0:
        next_x = 2 / N

        if x >= next_x: return 0
        return 1-x/next_x
    
    # Przypadek dla i=/=0
    else:
        x_i = 2*i/N
        next_x = x_i + 2/N
        previous_x = x_i - 2/N

        if x>=next_x or x<=previous_x: return 0
        if x>previous_x and x<=x_i:
            return (x-previous_x) / (x_i - previous_x)
        return 1 - (x - x_i) / (next_x - x_i)