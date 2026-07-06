from random import random
from scipy.stats import chi2

Nj = [141, 291, 132]
pj = [0.25, 0.5, 0.25]

#a)
def estadistico_T(Nj, pj):
    ti = 0
    n = sum(Nj)
    k = len(pj)
    for i in range(k):
        ti += ((Nj[i]-n*pj[i])**2)/(n*pj[i])
    return ti

def prueba_de_Pearson(t0, gl):
    return chi2.sf(t0, gl)

# b)
def generar_muestra():
    blancas = 0
    rosas = 0
    rojas = 0
    for _ in range(564):
        U = random()
        if U < 1/4:
            blancas += 1
        elif U < 3/4:
            rosas += 1
        else:
            rojas += 1
    return [blancas, rosas, rojas]

def sim_p_valor(Nsim, Nj, pj):
    p_valor = 0
    t0 = estadistico_T(Nj, pj)
    for i in range(Nsim):
        Nj_sim = generar_muestra()
        t_sim = estadistico_T(Nj_sim, pj)
        if t_sim >= t0:
            p_valor += 1
    p_valor = p_valor / Nsim
    return p_valor



t0 = estadistico_T(Nj, pj)
Nsim = 1000
print(f"t0 = {t0}")
print(f"p-valor para t0 con Pearson = {prueba_de_Pearson(t0,2)}")
print(f"p-valor con pata t0 {Nsim} simulaciones: {sim_p_valor(Nsim, Nj, pj)}")