from random import random
from math import log

# Genero los i's

def generar_I():
    U = random()
    if U < 0.5:
        return 1
    if U < 0.8:
        return 2
    else:
        return 3
    
def generar_X():
    medias = [3, 5, 7]
    i = generar_I() - 1
    lamda = medias[i]**-1
    U = 1 - random()
    return -log(U) / lamda

# Estimación de la esperanza

def sim_X(Nsim):
    sum = 0
    for _ in range(Nsim):
        sum += generar_X()
    return sum / Nsim

Nsim = 10000
e = sim_X(Nsim)
v_t = 4.4
print(f"Valor teórico de E[X]: {v_t}")
print(f"Estimación: {e}")
