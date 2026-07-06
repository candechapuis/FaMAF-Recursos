import random
import time
from scipy.stats import binom

def t_inversa():
    U = random.random()
    if U < 0.35:
        return 3
    elif U < 0.55:
        return 1
    elif U < 0.75:
        return 4
    elif U < 0.9:
        return 0
    else:
        return 2
    
    
def binomial(n,p):
    p_j = (1-p)**n
    F = p_j
    con = p/(1-p)
    for j in range (0,int(n*p)): # j = np-1 y calculo hasta F(np)
        p_j *= con * (n-j)/(j+1) 
        F += p_j
    # F = F(np)
    U = random.random()
    j = int(n*p) 
    if U >= F: # j = np+1 o más pues F(np) <= U < F(np+1)
        while U >= F: 
            p_j *= con * (n-j)/(j+1)
            F += p_j 
            j += 1 
        return int(j)
    else:
        while U < F: # j = np o menos pues F(np-1) <= U < F(np)
            F-= p_j
            p_j *= (con**-1) * (j+1)/(n-j) 
            j -=1 
        return int(j + 1)
    

def rechazo_bin(n,p):
    p_i = [0.15, 0.2, 0.1, 0.35, 0.2]
    q_i = [0.092, 0.3, 0.368, 0.2, 0.041]
    c = max([p_i[i]/q_i[i] for i in range(n+1)])
    y = binomial(n, p)
    while 1:
        U = random.random()
        if U < p_i[y] / (c * q_i[y]):
            return y 

# Comparación de eficiencias

def sim_t_inv(Nsim):
    inicio = time.time()
    for i in range(Nsim):
        _ = t_inversa()
    fin = time.time()
    tiempo = fin - inicio
    return tiempo

def sim_rechazo(Nsim, n, p):
    inicio = time.time()
    for i in range(Nsim):
        _ = rechazo_bin(n, p)
    fin = time.time()
    tiempo = fin - inicio
    return tiempo

Nsim = 10000
n = 4
p = 0.45
print(f"Tiempo t. inversa: {sim_t_inv(Nsim)}")
print(f"Tiempo aceptación-rechazo: {sim_rechazo(Nsim, n, p)}")

