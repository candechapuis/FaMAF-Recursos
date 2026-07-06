from random import random 
from math import exp, sqrt

def Monte_Carlo():
    U = random()
    mediaX = exp(U)/sqrt(2*U)
    n = 1
    Scuad = 1
    while n < 100 or sqrt(Scuad/n) > 0.01:
        n += 1
        mediaAnt = mediaX
        U = random()
        mediaX = mediaAnt + (exp(U)/sqrt(2*U)-mediaAnt)/n 
        Scuad = Scuad * (1-1/(n-1)) + n*(mediaX - mediaAnt)**2
    return mediaX

def h(y):
    return ((1/y - 1)**2 * exp(-(1/y -1)**2))/y**2

def Monte_Carlo2(h):
    U = random()
    while U == 0:
        U = random()
    H = h(U)
    mediaX = H
    n = 1
    Scuad = 1
    while n < 100 or 2*sqrt(Scuad/n) > 0.01:
        n += 1
        mediaAnt = mediaX
        U = random()
        while U == 0:
            U = random()
        H = h(U)
        mediaX = mediaAnt + (H - mediaAnt)/n 
        Scuad = Scuad *(1-1/(n-1)) + n*(mediaX - mediaAnt)**2
    return 2*mediaX    

print(f"Monte carlo 1: {Monte_Carlo()}")
print(f"Monte carlo 2: {Monte_Carlo2(h)}")
