from random import random
from math import exp, factorial

# Generación usando t. inversa

def t_inversa(k, lamda):
    C = sum([((lamda**j)/factorial(j))*exp(-lamda) for j in range(k+1)])
    U = random()
    i = 0; p = exp(-lamda)/C
    F = p
    while U >= F:
        i += 1
        p *= (lamda / i)
        p = p / C
        F = F + p
    return i

# Generación usando aceptación-rechazo y Y ~ P

def Poisson(lamda):
    U = random()
    i = 0; p = exp(-lamda)
    F = p
    while U >= F:
        i += 1
        p *= lamda / i
        F = F + p
    return i

def rechazo_poisson(k, lamda):
    C = sum([((lamda**j)/factorial(j))*exp(-lamda) for j in range(k+1)])
    while 1:
        y = Poisson(lamda)
        if y > k:
            p_y = 0
        else:
            q_y = (lamda**y * exp(-lamda))/factorial(y)
            p_y = q_y/C
        U = random()
        if U < p_y / (C**-1 * q_y):
            return y
        
# Generación usando aceptación-rechazo con Y ~ U{0, 1,..,k}

def Uniforme(k):
    U = random()
    return int((k*U))

def rechazo_uniforme(k, lamda):
    C = lamda * (k+1)
    denC = sum([((lamda**j)/factorial(j))*exp(-lamda) for j in range(k+1)])
    while 1:
        Y = Uniforme(k)
        U = random()
        p_y = ((lamda**Y * exp(-lamda))/factorial(Y))/denC
        q_y = 1/(k+1)
        if U < p_y / (C * q_y):
            return Y
    
# Estimación P(X>2)

def sim_p2_t_inv(Nsim, k, lamda):
    sum = 0
    for _ in range(Nsim):
        x = t_inversa(k, lamda)
        if (x > 2):
            sum += 1
    prob = sum / Nsim
    return prob

def sim_p2_rechazo_P(Nsim, k, lamda):
    sum = 0
    for _ in range(Nsim):
        x = rechazo_poisson(k, lamda)
        if (x > 2):
            sum += 1
    prob = sum / Nsim
    return prob

def sim_p2_rechazo_U(Nsim, k, lamda):
    sum = 0
    for _ in range(Nsim):
        x = rechazo_uniforme(k, lamda)
        if (x > 2):
            sum += 1
    prob = sum / Nsim
    return prob
    
print(f"P(X > 2) usando t. inversa: {sim_p2_t_inv(1000, 10, 0.7)}")
print(f"P(X > 2) usando rechazo, Y ~ P: {sim_p2_rechazo_P(1000, 10, 0.7)}")
print(f"P(X > 2) usando rechazo, Y ~ U: {sim_p2_rechazo_U(1000, 10, 0.7)}")

denC = sum([((0.7**j)/factorial(j))*exp(-0.7) for j in range(10+1)])
print(f"denc: {denC}")