from random import random
from math import log

def exponencial():
    U = 1 - random()
    return -log(U)

def t_inversa():
    Y = exponencial()
    U = random()
    return U**(1/Y)
