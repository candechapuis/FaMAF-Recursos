import random 

def g(x):
    return x/(x**2-1)

def h(y):
    return g(y+2)

def estimar_integralg(Nsim):
    suma = 0
    for _ in range(Nsim):
        suma += h(random.random())
    return suma / Nsim

sims = [1000, 5000, 10000]
for s in sims:
    print(f"estimación de la integral 5b) para {s} simulaciones: {estimar_integralg(s)}")