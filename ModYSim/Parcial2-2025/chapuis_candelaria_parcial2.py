from random import random

# Ej. 1c)

def ejercicio1():
    while 1:
        Y = random()
        U = random()
        f_Y = 30*(Y**2-2*(Y**3)+Y**4)
        if U < f_Y / 1.875:
            return Y 

def esperanza1c(Nsim):
    e = 0
    for _ in range(Nsim):
        e+= ejercicio1()
    e = e / Nsim  
    return e     
    
print(f"1c) Esperanza de X: {esperanza1c(10000)}")

#Ej. 2c)

def codigoX(p):
    U = random()
    X = 10
    prob = p
    F_x = prob
    if U >= F_x:
        X += 1
        prob *= (1-p)
        F_x += prob
    return X

#Ej. 2d)

def esperanza2c(Nsim, p):
    e = 0
    for _ in range(Nsim):
        e += codigoX(p)
    e = e / Nsim
    return e

print(f"2d) Esperanza de X: {esperanza2c(10000, 0.5)}")

