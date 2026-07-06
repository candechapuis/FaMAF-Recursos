from math import inf, log
from random import random

# Ej. 10a)

def lamda_t(t):
    return 7 - 1/(t+1)

def tiempo_svcio(lamda):
    return -log(1-random()) / lamda

def tiempo_llegada(lamda_t, lamda, t):
    llegada = t + -log(1-random()) / lamda
    U = random()
    while U >= lamda_t(llegada) / lamda:
        llegada += -log(1-random()) / lamda
        U = random()
    return llegada - t 



def sim_servidores_paralelo(gen_tA, lamda_t, lamda_tA,
                            gen_tS, lamda_tS1, lamda_tS2,
                            T):
    # tiempo transcurrido de simulación
    t = 0
    # num llegadas totales
    NA = 0
    # num clientes atendidos por serv 1
    C1 = 0
    # num clientes atendidos por serv 2
    C2 = 0
    # num total de clientes en el sistema
    n = 0
    # num de cliente siendo atendido en cola serv 1
    i1 = 0
    # num de cliente siendo atendido en cola serv 2
    i2 = 0
    # cola de clientes esperando para cada servidor
    Q1 = []
    Q2 = []
    # colas y contadores de clientes de cada servidor (histórico)
    Q1H = [0]
    Q2H = [0]
    q1 = 0
    q2 = 0
    # tiempos de llegada de c/ cliente
    A = {}
    # tiempos de salida de c/ cliente
    D = {}
    # tiempos de servicio y de salidas de servidor 1 y 2
    T1 = []
    T2 = []
    D1 = []
    D2 = []
    # primer tiempo de llegada
    T0 = gen_tA(lamda_t, lamda_tA, t)
    tA = T0
    # tiempos de fin de servicio en cada servidor
    t1 = inf
    t2 = inf
    while tA < inf or t1 < inf or t2 < inf:
        prox_evento = min(tA, t1, t2)
        if prox_evento == tA:
            t = tA
            NA += 1
            A[NA] = t
            tT = gen_tA(lamda_t, lamda_tA, t)
            tA = t + tT
            if tA > T:
                tA = inf
            if i1 == 0:
                i1 = NA
                tS1 = gen_tS(lamda_tS1)
                T1.append(tS1)
                t1 = t + tS1
                D1.insert(i1, t1)
                D[i1] = t1
            elif i2 == 0:
                i2 = NA
                tS2 = gen_tS(lamda_tS2)
                T2.append(tS2)
                t2 = t + tS2
                D2.insert(i2, t2)
                D[i2] = t2
            else:
                if len(Q1) <= len(Q2):
                    Q1.append(NA)
                    q1 += 1
                    Q1H.append(q1)
                else:
                    Q2.append(NA)
                    q2 += 1
                    Q2H.append(q2)
            n += 1
        elif prox_evento == t1:
            t = t1
            C1 += 1
            n -= 1
            D[i1] = t
            if Q1 != []:
                i1 = Q1.pop(0)
                q1 -= 1
                Q1H.append(q1)
                tS1 = gen_tS(lamda_tS1)
                T1.append(tS1)
                t1 = t + tS1
                D1.insert(i1, t1)
                D[i1] = t1
            else:
                i1 = 0
                t1 = inf
        else:
            t = t2
            C2 += 1
            n -= 1 
            D[i2] = t
            if Q2 != []:
                i2 = Q2.pop(0)
                q2 -= 1
                Q2H.append(q2)
                tS2 = gen_tS(lamda_tS2)
                T2.append(tS2)
                t2 = t + tS2
                D2.insert(i2, t2)
                D[i2] = t2
            else:
                i2 = 0
                t2 = inf
    return A, T1, T2, D1, D2, D, Q1H, Q2H

T = 5
A, T1, T2, D1, D2, D, Q1H, Q2H = sim_servidores_paralelo(tiempo_llegada, lamda_t, 7,
                                  tiempo_svcio, 3, 4,
                                  T)

print(f"Tiempos de llegada al sistema: {A}")
print(f"tiempos de salida serv 1: {D1}")
print(f"tiempos de salida serv 2: {D2}")
print(f"tiempos de salida totales: {D}")
print(f"Tiempos de svcio1: {T1}")
print(f"Tiempos de svcio2: {T2}")
print(f"Evolución cola S1: {Q1H}")
print(f"Evolución cola S2: {Q2H}")
print(f"clientes totales: {len(A), len(D1) + len(D2), len(D)}")

            


