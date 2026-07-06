import random
import time

probs = [0.11, 0.14, 0.09, 0.08, 0.12, 0.10, 0.09, 0.07, 0.11, 0.09]
probs_s = sorted(probs, reverse=True)
# [0.14, 0.12, 0.11, 0.11, 0.1, 0.09, 0.09, 0.09, 0.08, 0.07]

# Transformadora inversa

def t_inversa():
    U = random.random()
    if U < 0.14:
        return 2
    elif U < 0.26:
        return 5
    elif U < 0.37:
        return 1
    elif U < 0.48:
        return 9
    elif U < 0.58:
        return 6
    elif U < 0.67:
        return 3
    elif U < 0.76:
        return 7
    elif U < 0.85:
        return 10
    elif U < 0.93:
        return 4
    else:
        return 8

# Aceptación y rechazo
def udiscreta(n):
    U = random.random()
    return (n*U)+1

# Con cota mínima
def rechazo_cota():
    while 1:
        y = int(udiscreta(10))
        U = random.random()
        cota = probs[y-1] / 0.14  #c*q(y) = 1.4 * 0.1 
        if U < cota:
            return y

# Con c = 3
def rechazo_3():
    while 1:
        y = int(udiscreta(10))
        U = random.random()
        cota = probs[y-1] / (3 * 0.1)
        if U < cota:
            return y
        
# Método de la urna
cantidades = [int(probs[i] * 100) for i in range(len(probs))]
A = []
for i in range (10):
    A += [i+1]*cantidades[i]

def urna(A, n):
    I = int(udiscreta(n)-1)
    return A[int(udiscreta(n)-1)]  # le resto el 1 para que me dé valores de 0 a n-1

# Comparación de eficiencias
def sim_t_inversa(Nsim):
    inicio = time.time()
    for _ in range(Nsim):
        _ = t_inversa()
    fin = time.time()
    tiempo = fin - inicio
    return tiempo

def sim_rechazo_cota(Nsim):
    inicio = time.time()
    for _ in range(Nsim):
        _ = rechazo_cota()
    fin = time.time()
    tiempo = fin - inicio
    return tiempo

def sim_rechazo_3(Nsim):
    inicio = time.time()
    for _ in range(Nsim):
        _ = rechazo_3()
    fin = time.time()
    tiempo = fin - inicio
    return tiempo

def sim_urna(A, n, Nsim):
    inicio = time.time()
    for _ in range(Nsim):
        _ = urna(A, n)
    fin = time.time()
    tiempo = fin - inicio
    return tiempo

print(f"{'nsim':<10}{'t. inversa':<15}{'rechazo c min':<15}{'rechazo c 3':<15}{'urna':<15}")
print("-"*58)
Nsim = 10000
tiempo_t = sim_t_inversa(Nsim)
tiempo_r_c = sim_rechazo_cota(Nsim)
tiempo_r_3 = sim_rechazo_3(Nsim)
tiempo_urna = sim_urna(A, 100, Nsim)
print(f"{Nsim:<10}{tiempo_t:<15.4f}{tiempo_r_c:<15.4f}{tiempo_r_3:<15.4f}{tiempo_urna:<15.4f}")