from random import random 
from math import tan, pi, sqrt
from time import time

def cauchy_ti(lamda):
    return lamda*tan((random()-0.5)*pi)

def sim_ti(Nsim, lamda):
    inicio = time()
    n = 0
    for i in range(Nsim):
        X = cauchy_ti(lamda)
        if (X < lamda) and (X > -lamda):
            n+=1
    prop = n / Nsim
    tiempo = time() - inicio
    return prop, tiempo

def Cauchy(lamda):
    r = 1/sqrt(pi)
    while 1:
        U = random() * r
        V = random() * 2*r - r
        if U**2 + V**2 < r:
            return (V/U)*lamda

def sim_ratio(Nsim, lamda):
    inicio = time()
    n = 0
    for i in range(Nsim):
        X = Cauchy(lamda)
        if (X < lamda) and (X > -lamda):
            n+=1
    prop = n / Nsim
    tiempo = time() - inicio
    return prop, tiempo

p_1 = 0.5
prop_1, tiempo_t = sim_ti(10000, 1)
prop_1_ratio, tiempo_ratio = sim_ratio(10000, 1)
print(f"prop con t. inv: {prop_1}, tiempo: {tiempo_t}")
print(f"prop con acc-rech: {prop_1_ratio}, tiempo: {tiempo_ratio}")
print(f"valor teo: {p_1}")

