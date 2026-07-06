import random
import time
from scipy.stats import binom

def bin_t_inversa(n,p): #optimización usando E[X] = n*p
    p_j = (1-p)**n
    F = p_j
    c = p/(1-p)
    for j in range (0,int(n*p)): # j = np-1 y calculo hasta F(np)
        p_j *= c * (n-j)/(j+1) 
        F += p_j
    # F = F(np)
    U = random.random()
    j = n*p 
    if U >= F: # j = np+1 o más pues F(np) <= U < F(np+1)
        while U >= F: 
            p_j *= c * (n-j)/(j+1)
            F += p_j 
            j += 1 
        x = j
        return x
    else:
        while U < F: # j = np o menos pues F(np-1) <= U < F(np)
            F-= p_j
            p_j *= (c**-1) * (j+1)/(n-j) 
            j -=1 
        x = j + 1
        return x
    
x = bin_t_inversa(10, 0.3)
print(f"X binomial (t inversa): {x}")

def bernoulli(p):
    U = random.random()
    if U < p:
        return 1
    else:
        return 0

def binomial_sim(n,p):
    sum = 0
    for _ in range(n):
        sum += bernoulli(p)
    return sum 

x= binomial_sim(10,0.3)
print(f"X binomial (simulacion): {x}")

# Comparación de eficiencias

def sim_bin_ti(Nsim, n, p):
    inicio = time.time()
    for _ in range (Nsim):
        _ = bin_t_inversa(n,p)
    fin = time.time()
    tiempo = fin - inicio
    return tiempo

def sim_bin_sim(Nsim, n, p):
    inicio = time.time()
    for _ in range (Nsim):
        _ = binomial_sim(n,p)
    fin = time.time()
    tiempo = fin - inicio
    return tiempo

Nsim = 10000
n = 10
p = 0.3
print(f"Tiempo binomial t. inversa:", sim_bin_ti(Nsim, n, p))
print(f"Tiempo binomial simulacion:", sim_bin_sim(Nsim, n, p))

# Estimacion de valor esperado y proporcion de valores límite

def sim_ti_stats(Nsim, n, p): #uso monte carlo para estimar E[X]
    sum = 0
    ceros = 0
    dieces = 0
    for _ in range(Nsim):
        v_a = bin_t_inversa(n,p)
        sum += v_a
        if v_a == 0:
            ceros += 1
        if v_a == 10:
            dieces += 1
    E = sum / Nsim
    p_dieces = (dieces * 100) / Nsim
    p_ceros = (ceros * 100) / Nsim
    return E, p_dieces, p_ceros

def sim_bsim_stats(Nsim, n, p): #uso monte carlo para estimar E[X]
    sum = 0
    ceros = 0
    dieces = 0
    for _ in range(Nsim):
        v_a = binomial_sim(n,p)
        sum += v_a
        if v_a == 0:
            ceros += 1
        if v_a == 10:
            dieces += 1
    E = sum / Nsim
    p_dieces = (dieces * 100) / Nsim
    p_ceros = (ceros * 100) / Nsim
    return E, p_dieces, p_ceros

print(f"T. inversa")
E_t, d_t, c_t = sim_ti_stats(Nsim, n, p)
print(f"Valor esperado: {E_t}")
print(f"Proporcion dieces y ceros: {d_t}, {c_t}")
print(f"Simulacion")
E_s, d_s, c_s = sim_bsim_stats(Nsim, n, p)
print(f"Valor esperado: {E_s}")
print(f"Proporcion dieces y ceros: {d_s}, {c_s}")
print("Probabiidades teóricas")
print(f"Valor esperado: {n*p}")
p_teo_dieces = binom.pmf(10, 10, 0.3) * 100
p_teo_ceros = binom.pmf(0, 10, 0.3) * 100
print(f"Proporcion dieces y ceros: {p_teo_dieces}, {p_teo_ceros}")