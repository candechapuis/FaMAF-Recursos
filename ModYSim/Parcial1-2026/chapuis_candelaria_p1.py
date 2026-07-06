from math import exp
from random import random

# función con cambio de variable
def h(x):
    y = 4*x - 1
    return exp(-y+exp(-y))

def monte_carlo(N):
    sum = 0
    for i in range(N):
        # genero una va uniforme en (0,1)
        u = random()
        # calculo y acumulo la funcion evaluada en mi uniforme
        sum += h(u)
    # estimo la integral
    integral = (sum * 4) / N
    return integral

N1 = 1000
N2 = 10000
N3 = 100000
print(f"{'N':<10}{'estimación':<10}")
print(f"{N1:<10}{monte_carlo(N1):<10.6f}")
print(f"{N2:<10}{monte_carlo(N2):<10.6f}")
print(f"{N3:<10}{monte_carlo(N3):<10.6f}")