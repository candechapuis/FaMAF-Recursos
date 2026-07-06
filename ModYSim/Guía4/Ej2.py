import math
import random
import numpy as np

Nsim = 100
N = 100000

def g(x):
    return math.exp(x/N)

def estimar_sum_g(Nsim, N):
    return N * np.mean([g(random.randint(1,N)) for _ in range(Nsim)])

print(f"Estimación con {Nsim} simulaciones: {estimar_sum_g(Nsim, N)}")

def sum_g_exacta(N):
    sum = 0
    for i in range(1,N):
        sum += g(i)
    return sum

print(f"Valor exacto para los {Nsim} primeros términos: {sum_g_exacta(Nsim)}")
print("Valor exacto:", sum_g_exacta(N))