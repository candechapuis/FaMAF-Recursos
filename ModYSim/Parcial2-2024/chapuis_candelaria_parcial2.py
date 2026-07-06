from random import random
from math import sqrt

# Ej. 1b)
print("================ Ejercicio 1 ================")
def algo_x(p):
    while 1:
        Y = int(random() * 4)
        U = random()
        f_Y = p[Y]
        if U < f_Y / 0.35: # 1.4 * 0.25 = c * P(Y=y)
            return Y 
        
p = [0.13, 0.22, 0.35, 0.3]
print(f"Y generada: {algo_x(p)}\n")

# Ej. 2b)
print("================ Ejercicio 2 ================")
def ejercicio2():
    U = random()
    if U < 2/3:
        return sqrt(3.375*(U**3)) # 27/8 = 3.375
    else:
        return 3*U-1
    
# Estimación de P(X > 4), que claramente será 0 pues 0<= X < 2
def p_4(Nsim):
    cuatros = 0
    for _ in range(Nsim):
        X = ejercicio2()
        if X > 4:
            cuatros += 1
    cuatros = cuatros / Nsim
    return cuatros

print(f"X generada: {ejercicio2()}")
print(f"P(X > 4): {p_4(10000)}\n")


print("================ Ejercicio 4 ================")

def area(N):
    exitos = 0
    for _ in range(N):
        X = -1.5+3*random()
        Y = -1.5+3*random()
        if X**2 + (Y-abs(X)**(3/2))**2 <= 1:
            exitos += 1
    return 9 * exitos / N
 
print(f"Área bajo la curva: {area(10000):.6f}")