from random import random
from math import sqrt
from time import time

def suma_U():
    U = random()
    V = random()
    return U + V 

def t_inversa():
    U = random()
    if U < 0.5:
        return sqrt(2*U)
    else: 
        return 2 - sqrt(2*(1-U))
    
def rechazo():
    while 1:
        Y = 2 * random() # Y ~ U (0,2)
        U = random()
        if Y < 1:
            f_Y = Y
        else:
            f_Y = 2 - Y
        if U < f_Y:
            return Y
        
# Comparación de eficiencia

def sim_suma_U(Nsim):
    inicio = time()
    e = 0
    for _ in range(Nsim):
        e += suma_U()
    fin = time()
    e = e / Nsim
    return e, fin-inicio

def sim_t_inversa(Nsim):
    inicio = time()
    e = 0
    for _ in range(Nsim):
        e += t_inversa()
    fin = time()
    e = e / Nsim
    return e, fin-inicio

def sim_rechazo(Nsim):
    inicio = time()
    e = 0
    for _ in range(Nsim):
        e += rechazo()
    fin = time()
    e = e / Nsim
    return e, fin-inicio

Nsim = 10000
print(f"Simulación con {Nsim} repeticiones")
print(f"{'método':<10}{'duración':<10}{'esperanza':<11}")
print(f"{'suma':<10}{sim_suma_U(Nsim)[1]:<10.4f}{sim_suma_U(Nsim)[0]:<11.4f}")
print(f"{'t.inversa':<10}{sim_t_inversa(Nsim)[1]:<10.4f}{sim_t_inversa(Nsim)[0]:<11.4f}")
print(f"{'rechazo':<10}{sim_rechazo(Nsim)[1]:<10.4f}{sim_rechazo(Nsim)[0]:<11.4f}")
