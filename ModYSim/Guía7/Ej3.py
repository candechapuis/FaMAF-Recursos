from random import random

Xj = [0.12, 0.18, 0.06, 0.33, 0.72, 0.83, 0.36, 0.27, 0.77, 0.74]

def estadístico_D(Xj, F):
    n = len(Xj)
    Xj.sort()
    posibles_d = []
    for i in range(n):
        dif1 = ((i+1)/n)-F(Xj[i])
        dif2 = F(Xj[i])-(i/n)
        posibles_d.append(dif1)
        posibles_d.append(dif2)
    d = max(posibles_d)
    return d

def sim_p_valor_KS(Nsim, Xj):
    d = estadístico_D(Xj, lambda x: x)
    p_valor = 0
    for i in range(Nsim):
        Uj_sim = []
        for j in range(len(Xj)):
            Uj_sim.append(random())
        Uj_sim.sort()
        d_sim = estadístico_D(Uj_sim, lambda x: x)
        if d_sim >= d:
            p_valor += 1
    return p_valor / Nsim

d = estadístico_D(Xj, lambda x: x)
Nsim = 1000
p_valor = sim_p_valor_KS(Nsim, Xj)
print(f"d = {d}")
print(f"Aprox. p-valor con Kolmogorov-Smirnov: {p_valor} ")