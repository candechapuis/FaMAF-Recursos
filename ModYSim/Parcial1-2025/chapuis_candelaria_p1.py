from math import sqrt
from random import random

# EJERCICIO 1

# función con cambio de variable
def h(y):
    x = 6*y + 1
    return sqrt(x+sqrt(x))

def monte_carlo(N):
    sum = 0
    for i in range(N):
        # genero una va uniforme en (0,1)
        u = random()
        # calculo y acumulo la funcion evaluada en mi uniforme
        sum += h(u)
    # estimo la integral
    integral = (sum * 6) / N
    return integral

N1 = 1000
N2 = 10000
N3 = 100000
print(f"{'N':<10}{'estimación':<10}")
print(f"{N1:<10}{monte_carlo(N1):<10.6f}")
print(f"{N2:<10}{monte_carlo(N2):<10.6f}")
print(f"{N3:<10}{monte_carlo(N3):<10.6f}")

# EJERCICIO 2
# a) 

def juego():
    sum = 0
    cant_u = 0
    while sum < 1:
        sum += random()
        cant_u += 1
    return sum, cant_u

# b)

def pares(N):
    impares = 0
    for i in range(N):
        # simulo el juego
        sum, cant_u = juego()
        # cuento 1 si la cantidad de uniformes simuladas fue impar
        if cant_u % 2 != 0:
            impares += 1
    p = impares / N
    return p

print(f"{'N':<10}{'p':<10}")
print(f"{N1:<10}{pares(N1):<10.6f}")
print(f"{N2:<10}{pares(N2):<10.6f}")
print(f"{N3:<10}{pares(N3):<10.6f}")
