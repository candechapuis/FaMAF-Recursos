from math import exp, sqrt
from random import random
from scipy.stats import expon, binom, chi2, norm


print("------------------ Ejercicio 2 ------------------ ")

Xj = [15.22860536, 40.60145536, 33.67482894, 44.03841737, 15.69560109,
    16.2321714, 25.02174735, 30.34655637, 3.3181228, 5.69447539,
    10.1119561, 49.10266584, 3.6536329, 35.82047148, 3.37816632,
    36.72299321, 50.67085322, 3.25476304, 20.12426236, 20.2668814,
    17.49593589, 2.70768636, 14.77332745, 1.72267967, 23.34685662,
    8.46376635, 9.18330789, 9.97428217, 2.33951729, 137.51657441,
    9.79485269, 10.40308179, 1.57849658, 6.26959703, 4.74251574,
    1.53479053, 34.74136011, 27.47600572, 9.1075566, 1.88056595,
    27.59551348, 6.82283137, 12.45162807, 28.01983651, 0.36890593,
    7.82520791, 3.17626161, 46.91791271, 38.08371186, 41.10961135]

def F_exp(x):
    return expon.cdf(x, scale=1/0.05)

def estadistico_D(Xj, F):
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

def sim_p_valor_KS_u(Nsim, Xj):
    p_valor = 0
    d = estadistico_D(Xj, F_exp)
    n = len(Xj)
    for i in range(Nsim):
        Uj = [random() for j in range(n)]
        d_sim = estadistico_D(Uj, lambda x: x)
        if d_sim >= d:
            p_valor += 1
    return p_valor / Nsim

def sim_p_valor_KS_exp(Nsim, Xj):
    p_valor = 0
    d = estadistico_D(Xj, F_exp)
    n = len(Xj)
    for i in range(Nsim):
        Xj_sim = [expon.rvs(scale=1/0.05) for j in range(n)]
        d_sim = estadistico_D(Xj_sim, F_exp)
        if d_sim >= d:
            p_valor += 1
    return p_valor / Nsim 

Nsim = 1000
d = estadistico_D(Xj, F_exp)
p_valor_u = sim_p_valor_KS_u(Nsim, Xj)
p_valor_exp = sim_p_valor_KS_exp(Nsim, Xj)
print(f"estadístico d: {d}")
print(f"p_valor aprox. con {Nsim} simulaciones de v.a uniformes:")
print(p_valor_u)
print(f"p_valor aprox. con {Nsim} simulaciones de v.a exponenciales:")
print(p_valor_exp)

print("------------------ Ejercicio 3 ------------------ ")

Ni = [38, 144, 342, 287, 164, 25]

def estimar_p(Ni, n):
    tam = sum(Ni)
    p_est = sum([Ni[i]*i for i in range(6)])/(tam*n)
    return p_est

def calcular_pi_est(Ni, n, p_est):
    pi = [binom.pmf(i, n, p_est) for i in range(n+1)]
    return pi

p_est = estimar_p(Ni, 5)
pi = calcular_pi_est(Ni, 5, p_est)

def estadistico_T(Ni, pi):
    ti = 0
    n = sum(Ni)
    k = len(pi)
    for i in range(k):
        ti += ((Ni[i]-n*pi[i])**2)/(n*pi[i])
    return ti

def sim_p_valor_bin(Nsim, Ni, pi, p_est):
    p_valor = 0
    n = sum(Ni)
    k = len(pi)
    t0 = estadistico_T(Ni, pi)
    for i in range(Nsim):
        Xi_sim = binom.rvs(n=5, p=p_est, size=n)
        Ni_sim = [sum(Xi_sim == i) for i in range(k)]
        p_est_sim = estimar_p(Ni_sim, 5)
        pi_est = calcular_pi_est(Ni_sim, 5, p_est_sim)
        t_sim = estadistico_T(Ni_sim, pi_est)
        if t_sim >= t0:
            p_valor += 1
    return p_valor / Nsim

t0 = estadistico_T(Ni, pi)
print(f"t0 = {t0}")
p_valor_chi = chi2.sf(t0, 4)
print(f"p-valor según prueba de Pearson para t0: {p_valor_chi}")
p_valor_sim = sim_p_valor_bin(1000, Ni, pi, p_est)
print(f"p-valor según simulaciones para t0: {p_valor_sim}")


print("------------------ Ejercicio 4 ------------------ ")

def calculo_z(alpha):
  return norm.ppf(1-alpha/2)

def h(y):
    x= y + 2
    return exp(-x)*(1-x**4)

# max_iter = 0, simulo hasta que se cumpla L < 0.002
# max_iter = n, hago n simulaciones
def estimar_int(alpha, L, h, max_iter=0):
    z_alfa_2 = calculo_z(alpha)
    d = L / (2 * z_alfa_2)
    media = h(random())
    Scuad, n = 0, 1
    while n <= 100 or sqrt(Scuad/n) > d:
        n += 1
        X = h(random())
        media_ant = media
        media = media_ant + (X - media_ant) / n
        Scuad = Scuad * (1 - 1 /(n-1)) + n*(media - media_ant)**2
        if n == max_iter:
            break
    izq = media - z_alfa_2 * sqrt(Scuad/n)
    der = media + z_alfa_2 * sqrt(Scuad/n)
    intervalo = (izq, der)
    return media, Scuad, intervalo, n

def estadísticas_sim(alpha, L, h):
    Ns = [1000, 5000, 7000, 0]
    Is = []
    Ss = []
    ICs = []
    for n in Ns:
        I, S, IC, N = estimar_int(alpha, L, h, n)
        Is.append(I)
        Ss.append(sqrt(S))
        ICs.append(IC)
    return Is, Ss, ICs

L = 0.002
alpha = 0.05
I, Scuad, int, n = estimar_int(alpha, L, h)
Is, Ss, ICs = estadísticas_sim(alpha, L, h)
print(f"La estimación para la integral es: {I} con {n} simulaciones")
print(f"Is = {Is}")
print(f"Ss = {Ss}")
print(f"ICs = {ICs}")

