from random import random
from math import log

def llegadas_hasta(lamda, T):
    t = -log(1 - random()) / lamda
    aficionados = int((21*random())+20)
    while t <= T:
        t += -log(1-random()) / lamda
        aficionados += int((21*random())+20)
    return aficionados