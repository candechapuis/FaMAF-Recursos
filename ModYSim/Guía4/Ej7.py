import random
from numpy import exp

def poisson_t_inv_comun(lamda):
    U = random.random()
    i = 0; p = exp(-lamda)
    F = p
    while U >= F:
        i += 1
        p *= lamda / i
        F = F + p
    return i

def poisson_t_inv_opt(lamda):
    p = exp(-lamda); F = p
    for j in range(1, int(lamda) + 1):
        p *= lamda / j
        F += p
    U = random.random()
    if U >= F:
        j = int(lamda) + 1
        while U >= F:
            p *= lamda / j; F += p
            j += 1
        return j - 1
    else:
        j = int(lamda)
        while U < F:
            F -= p; p *= j/lamda
            j -= 1
        return j+1
    
# Cálculo de P(Y>2)

def sim_p2_t_inv_comun(Nsim, lamda):
    sum = 0
    for _ in range(Nsim):
        y = poisson_t_inv_comun(lamda)
        if (y > 2):
            sum += 1
    prob = sum / Nsim
    return prob

def sim_p2_t_inv_opt(Nsim, lamda):
    sum = 0
    for _ in range(Nsim):
        y = poisson_t_inv_opt(lamda)
        if (y > 2):
            sum += 1
    prob = sum / Nsim
    return prob

print(f"P(Y > 2) usando t. inversa común: {sim_p2_t_inv_comun(1000, 10)}")
print(f"P(Y > 2) usando t. inversa optimizada: {sim_p2_t_inv_opt(1000, 10)}")