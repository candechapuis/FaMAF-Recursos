from random import random
from math import sqrt 
from scipy.stats import norm

def Bernoulli_pi():
    X = random() * 2 - 1
    Y = random() * 2 - 1
    if X**2 + Y **2 <= 1:
        return 1
    else: return 0

def Estimar_pi(n_min, d):
    p = Bernoulli_pi()
    n = 1
    while n <= n_min or sqrt(p*(1-p)/n) > d:
        n += 1
        p = p + (Bernoulli_pi() - p) / n
    return p, n


p, n = Estimar_pi(100, 0.01)
print(f"Estimación de proporción: {p:.4f} con {n} simulaciones")
print(f"Estimación de pi: {4*p:.4f}")

def Estimar_pi_IC(n_min, alpha, L):
    p = Bernoulli_pi()
    n = 1
    z_alpha_2 = norm.ppf(1-alpha/2)
    d = L / (2*z_alpha_2*4)
    while n <= n_min or sqrt((p*(1-p)) / n) > d:
        n += 1
        p = p + (Bernoulli_pi()-p) / n
    intervalo = f"[{4*p-z_alpha_2*4*sqrt((p*(1-p))/n):.4f},{4*p+z_alpha_2*4*sqrt((p*(1-p))/n):.4f}]"
    return intervalo, p, n

n_min = 100
alpha = 0.05
intervalo_01, p_01, n_01 = Estimar_pi_IC(n_min, alpha, 0.1)
intervalo_005, p_005, n_005 = Estimar_pi_IC(n_min, alpha, 0.05)
intervalo_0001, p_0001, n_0001 = Estimar_pi_IC(n_min, alpha, 0.001)
print(f"{'L':<12}{'sims':<12}{'pi':<12}{'IC(95%)':<12}")
print(f"{'0.1':<12}{n_01:<12}{4*p_01:<12.4f}{intervalo_01:<12}")
print(f"{'0.05':<12}{n_005:<12}{4*p_005:<12.4f}{intervalo_005:<12}")
print(f"{'0.001':<12}{n_0001:<12}{4*p_0001:<12.4f}{intervalo_0001:<12}")


