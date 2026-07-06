from random import random 
from math import log

def Poisson_homogeneo(lamda, T):
    t = -log(1-random())/lamda
    Eventos = []
    while t <= T:
        Eventos.append(t)
        t += -log(1-random())/lamda
    return Eventos, len(Eventos)
