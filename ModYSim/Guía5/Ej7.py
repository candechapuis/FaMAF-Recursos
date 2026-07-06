from time import time
from random import random
from math import log, exp
import numpy as np

# Transformada Inversa

def t_inversa():
    U = random()
    return exp(U)

# Aceptación-Rechazo

def a_r():
    while 1:
        Y = random() * (exp(1)-1) + 1 #Y ~ U (1,e)
        #tengo Y~U(0,1) y quiero Y~(a,b) continua hago Y*(b-a)+a
        U = random()
        if U < 1/Y:
            return Y

# Comparación de eficacia y eficiencia

def sim_t_inversa(Nsim):
    inicio = time()
    sim = 0
    for _ in range(Nsim):
        sim += t_inversa()
    sim = sim / Nsim
    fin = time()
    return sim, fin-inicio

def sim_a_r(Nsim):
    inicio = time()
    sim = 0
    for _ in range(Nsim):
        sim += a_r()
    sim = sim / Nsim
    fin = time()
    return sim, fin-inicio

# Estimación de P(X<=2)

def sim_p2(Nsim):
    sumX1 = 0
    sumX2 = 0
    for _ in range(Nsim):
        X1 = t_inversa()
        X2 = a_r()
        if X1 <= 2:
            sumX1 += 1
        if X2 <= 2:
            sumX2 += 1
    p2X1 = sumX1 / Nsim
    p2X2 = sumX2 / Nsim
    return p2X1, p2X2


Nsim = 10000
print(f"Simulación con {Nsim} repeticiones")
print(f"{'método':<15}{'duración':<10}{'esperanza':<11}{'P(X<=2)'}")
e_ti, tiempo_ti = sim_t_inversa(Nsim)
e_ar, tiempo_ar = sim_a_r(Nsim)
e_teo = 1.718
p2_ti, p2_ar = sim_p2(Nsim)
p2_teo = 0.6931
print(f"{'t. inversa':<15}{tiempo_ti:<10.4f}{e_ti:<11.4f}{p2_ti:<10.4f}")
print(f"{'rechazo':<15}{tiempo_ar:<10.4f}{e_ar:<11.4f}{p2_ar:<10.4f}")
print(f"{'teórico':<15}{'-':<10}{e_teo:<11.4f}{p2_teo:<10.4f}")
