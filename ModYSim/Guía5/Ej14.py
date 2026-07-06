from random import random 
from math import log

def lamda_t1(t):
    return 3 + (4/(t+1))


def Poisson_no_homo(lamda_t, t_cota, T):
    eventos = []
    lamda = lamda_t(t_cota)
    t = -log(1-random()) / lamda
    while t <= T:
        U = random()
        if U < lamda_t(t) / lamda:
            eventos.append(t)
        t += -log(1-random()) / lamda
    return eventos, len(eventos)

def Poisson_no_homo_mejora1(T):
    interv = [1,2,3]
    lamda = [7,5,(13/3)]
    j = 0
    t = -log(1-random()) / lamda[j]
    eventos = []
    while t <= T:
        if t <= interv[j]:
            U = random()
            if U < (3 + 4/(t+1)) / lamda[j]:
                eventos.append(t)
            t += -log(1-random())/lamda[j]
        else: 
            t = interv[j] + (t-interv[j]) * lamda[j] / lamda[j+1]
            j+=1
    return eventos
