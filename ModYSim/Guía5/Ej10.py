from random import random
from math import pi, sqrt

def Cauchy(lamda):
    r = 1/sqrt(pi)
    while 1:
        U = random() * r
        V = random() * 2*r - r
        if U**2 + V**2 < r:
            return (V/U)*lamda
    
def sim(Nsim, lamda):
    n = 0
    for i in range(Nsim):
        X = Cauchy(lamda)
        if (X < lamda) and (X > -lamda):
            n+=1
    prop = n / Nsim
    return prop

p_1 = 0.5
prop_1 = sim(10000, 1)
print(f"prop con alg: {prop_1}")
print(f"valor teo: {p_1}")
