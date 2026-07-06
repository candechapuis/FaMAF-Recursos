from random import random
from math import sqrt, exp

# 1.a)

def ej1_a():
    U = random()
    if U > 1/4:
        print(f"1er caso, U: {U}")
        return 6-6*(sqrt((1/3)*(1-U)))
    else:
        print(f"2do caso, U: {U}")
        return 2 + 2 * sqrt(U)
    
X = ej1_a()
print(f"X: {X}")
