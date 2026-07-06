from random import random
from math import log, inf, sqrt

# Ej. 7a)

def lamda_t(t):
    r = t % 10
    if 0 <= r <= 5:
        return 3*r + 4
    else: 
        return -3*r + 34

def tiempo_de_llegadaPNO(lamda_t, lamda, t):
    llegada = t + (-log(1-random()) / lamda)
    U = random()
    while U >= lamda_t(llegada) / lamda:
        llegada += -log(1-random()) / lamda
        U = random()
    return llegada - t

def tiempo_de_svcioE(lamda):
    return -log(1-random()) / lamda

def sim_unico_servidor(generador_tA, lamda_t, lamda_tA, generador_tS, lamda_tS , T):
    # tiempo de simulación transcurrido
    t = 0
    # número de llegadas hasta t
    NA = 0
    # tiempos de llegada
    A = []
    # número de salidas hasta t
    ND = 0
    # tiempos de salida
    D = []
    # clientes en el sistema en el instante t
    n = 0
    # servicios en cola
    S = []
    # genero el primer tiempo de llegada (Poisson no homogéneo)
    T0 = generador_tA(lamda_t, lamda_tA, t)
    tA = T0
    tD = inf
    while tA < inf or tD < inf:
        prox_evento = min(tA, tD)
        if prox_evento == tA:
            t = tA
            NA += 1
            n += 1
            S.append(n)
            A.append(t)
            tA = t + generador_tA(lamda_t, lamda_tA, t)
            if tA > T:
                tA = inf
            if n == 1:
                s = generador_tS(lamda_tS)
                tD = t + s
        elif prox_evento == tD:
            t = tD
            ND += 1
            n -= 1
            S.append(n)
            D.append(t)
            if n == 0:
                tD = inf
            else:
                s = generador_tS(lamda_tS)
                tD = t + s
    return A, D, S

A, D, S = sim_unico_servidor(tiempo_de_llegadaPNO, lamda_t, 19, tiempo_de_svcioE, 13, 100)
print(f"Tiempos de llegada: {A}")
print(f"Tiempos de salida: {D}")
print(f"Servicios en la cola(histórico): {S} ({len(A), len(D)} llegadas en total)")

#Ej. 7b)

def generar_P():
    A, D, S = sim_unico_servidor(tiempo_de_llegadaPNO, lamda_t, 19, 
                                 tiempo_de_svcioE, 13, 
                                 100)
    n = len(D)
    P = sum([D[i] - A[i] for i in range(n)]) / n
    return P 

def media_P(d, n_min):
    media = generar_P()
    n = 1
    Scuad = 0
    while n <= n_min or sqrt(Scuad/n) > d:
        n += 1
        media_ant = media
        media = media_ant + (generar_P() - media_ant) / n
        Scuad =  Scuad * (1 - 1 /(n-1)) + n*(media - media_ant)**2
    return media, n

media, sims = media_P(0.01, 100)
print("Estimación del tiempo promedio que tarda en ser procesada una solicitud:")
print(media)
print(f"Simulaciones requeridas para la estimación: {sims}")

# Ej. 7c)

def generar_Y(T):
    A, D, S = sim_unico_servidor(tiempo_de_llegadaPNO, lamda_t, 19, 
                                 tiempo_de_svcioE, 13, 
                                 T)
    if D[-1] > T:
        return 1
    else: return 0

def prop_soli_tardia(d, n_min, T):
    p = generar_Y(T)
    n = 1
    while n <= n_min or sqrt(p* (1-p) / n) > d:
        n += 1
        p = p + (generar_Y(T) - p) / n 
    return p, n

p_T, n_T = prop_soli_tardia(0.01, 100, 100)
print("P(alguna solicitud se completa luego de T):")
print(p_T)
print(f"Simulaciones requeridas para la estimación: {n_T}")

    
            
        
  



    
