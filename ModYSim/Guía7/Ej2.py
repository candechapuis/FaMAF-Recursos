from random import random
from scipy.stats import chi2

Nj = [158,172,164,181,160,165]
pj = [1/6] * 6

def estadistico_T(Nj, pj):
    ti = 0
    n = sum(Nj)
    k = len(pj)
    for i in range(k):
        ti += ((Nj[i]-n*pj[i])**2)/(n*pj[i])
    return ti

def prueba_de_Pearson(t0, gl):
    return chi2.sf(t0, gl)

def udiscreta(a,b):
    U = random()
    return int(U * (b - a + 1)) + a

def generar_muestra(n, k, a, b):
    Nj = [0] * k
    for i in range(n):
        Ni = udiscreta(a, b)
        Nj[Ni-1] += 1
    return Nj

def sim_p_valor_uD(Nsim, Nj, pj, a, b):
    p_valor = 0
    n = sum(Nj)
    k = len(pj)
    t0 = estadistico_T(Nj, pj)
    for i in range(Nsim):
        Nj_sim = generar_muestra(n, k, a, b)
        t_sim = estadistico_T(Nj_sim, pj)
        if t_sim >= t0:
            p_valor += 1
    return p_valor / Nsim


t0 = estadistico_T(Nj, pj)
Nsim = 1000
a = 1
b = 6
print(f"t0 = {t0}")
print(f"p-valor para t0 con Pearson = {prueba_de_Pearson(t0,5)}")
print(f"p-valor para t0 con {Nsim} simulaciones: {sim_p_valor_uD(Nsim, Nj, pj, a, b)}")
