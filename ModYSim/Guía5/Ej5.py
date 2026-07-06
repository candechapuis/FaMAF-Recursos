from math import log
from random import random

def exponencial(lamda):
    U = 1-random()
    return -log(U)/lamda

def muestra_10_max_min():
    muestra_M = []
    muestra_m= []
    for i in range(10):
        exponenciales = [exponencial(1), exponencial(2), exponencial(3)]
        muestra_M.append(max(exponenciales))
        muestra_m.append(min(exponenciales))
    return muestra_M, muestra_m

M, m = muestra_10_max_min()

print(f"Muestra M: {M}")
print(f"Muestra m: {m}")
