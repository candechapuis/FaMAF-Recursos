from math import inf, log, sqrt
from random import random
from scipy.stats import norm

# Ej. 9a)

def lamda_t(t):
    x = t % 8
    if x <= 4:
        return 2.5*x + 4
    else: 
        return -2.5*x + 24
    
def tiempo_llegadaPNH(lamda_t, lamda, t):
    llegada = t + (-log(1-random())) / lamda
    U = random()
    while U >= lamda_t(llegada) / lamda:
        llegada += (-log(1-random())) / lamda
        U = random()
    return llegada - t

def tiempo_servicioE(lamda):
    return -log(1-random()) / lamda

def sim_svcio_enserie(gen_tA, lamda_t, lamda_tA,
                      gen_tS, lamda_tS1, lamda_tS2,
                      T):
    # tiempo de simulación
    t = 0
    # llegadas hasta t
    NA = 0
    # tiempos de llegadas a svcio 1 y svcio 2 de cliente i (índice)
    A1 = []
    A2 = []
    # salidas hasta t
    ND = 0
    # tiempos de salida de cliente i (indice)
    D = []
    # cientes en svcio 1 y 2
    n1 = n2 = 0
    # tiempos de svcio 1 y 2
    TS1 = [] 
    TS2 = []
    # colas en svcio 1, 2 y total
    Q1 = []
    Q2 = []
    QT = []
    # genero el 1° tA (tiempo prox llegada)
    tA = gen_tA(lamda_t, lamda_tA, t)
    # fin svcio 1 y 2
    t1 = t2 = inf
    while tA < inf or t1 < inf or t2 < inf:
        prox_evento = min(tA, t1, t2)
        if prox_evento == tA:
            t = tA
            NA += 1
            # registro el tiempo en el que llegó el cliente al svcio 1
            A1.append(t)
            n1 += 1
            # registro nuevo cliente en cola
            Q1.append(max(n1-1, 0))
            QT.append(max(n1-1, 0)+max(n2-1, 0))
            # genero prox llegada
            tA = t + gen_tA(lamda_t, lamda_tA, t)
            if tA > T:
                tA = inf
            if n1 == 1:
                # genero tiempo fin de svcio 1 (atiendo el cliente)
                tT1 = gen_tS(lamda_tS1)
                t1 = t + tT1
                TS1.append(tT1)
        elif prox_evento == t1:
            t = t1 
            # registro el tiempo en el que llegó el cliente al svcio 2
            A2.append(t)
            n1 -= 1
            # registro baja de cliente en cola
            Q1.append(max(n1-1, 0))
            QT.append(max(n1-1, 0)+max(n2-1, 0))
            if n1 == 0:
                t1 = inf
            else:
                tT1 = gen_tS(lamda_tS1)
                t1 = t + tT1
                TS1.append(tT1)
            n2 += 1
            # registro nuevo cliente en cola
            Q2.append(max(n2-1, 0))
            QT.append(max(n1-1, 0)+max(n2-1, 0))
            if n2 == 1:
                tT2 = gen_tS(lamda_tS2)
                t2 = t + tT2
                TS2.append(tT2)
        else:
            t = t2
            # registro el tiempo en el que el cliente salió
            D.append(t)
            ND += 1
            n2 -= 1
            # registro baja de cliente en cola
            Q2.append(max(n2-1, 0))
            QT.append(max(n1-1, 0)+max(n2-1, 0))
            if n2 == 0:
                t2 = inf
            else: 
                tT2 = gen_tS(lamda_tS2)
                t2 = t + tT2
                TS2.append(tT2)
    # devuelvo los tiempos de llegada a c/ svcio, 
    # los tiempos de svcio, 
    # la evolución de los trabajos en cola,
    # y el tiempo total en sistema por cliente
    TTS = [D[i]-A1[i] for i in range(len(D))]
    return A1, A2, TS1, TS2, Q1, Q2, QT, TTS


T = 16
A1, A2, TS1, TS2, Q1, Q2, QT, TTS = sim_svcio_enserie(tiempo_llegadaPNH, lamda_t, 14,
                                  tiempo_servicioE, 15, 12,
                                  T)

print(f"Tiempos de llegada svcio 1: {A1}")
print(f"Tiempos de llegada svcio 2: {A2}")
print(f"Tiempos de svcio1: {TS1}")
print(f"Tiempos de svcio2: {TS2}")
print(f"Tiempos totales en sistema: {TTS}")
print(f"Evolución cola S1: {Q1}")
print(f"Evolución cola S2: {Q2}")
print(f"Evolución cola total: {QT}")
print(f"E[clientes atendidos]: {((4+14)/2)*T}")
print(f"clientes totales: {len(A1), len(A2)}")

#Ej. 9b)

def media_TS(gen_tA, lamda_t, lamda_tA,
                      gen_tS, lamda_tS1, lamda_tS2,
                      T):
    A1, A2, TS1, TS2, Q1, Q2, QT, TTS = sim_svcio_enserie(gen_tA, lamda_t, lamda_tA,
                                                            gen_tS, lamda_tS1, lamda_tS2,
                                                            T)
    media = sum(TTS) / len(TTS)
    return media

def estimacion_media_TS(gen_tA, lamda_t, lamda_tA,
                      gen_tS, lamda_tS1, lamda_tS2,
                      T,
                      d, n_min):
    X = media_TS(gen_tA, lamda_t, lamda_tA,
                      gen_tS, lamda_tS1, lamda_tS2,
                      T)
    media = X
    n = 1
    Scuad = 0
    while n <= n_min or sqrt(Scuad/n) > d:
        n += 1
        media_ant = media
        X = media_TS(gen_tA, lamda_t, lamda_tA,
                      gen_tS, lamda_tS1, lamda_tS2,
                      T)
        media = media_ant + (X - media_ant) / n
        Scuad = Scuad * (1 - 1 /(n-1)) + n*(media - media_ant)**2
    return media, n, Scuad

d, n_min = 0.01, 100
media_TTS, sims, Scuad = estimacion_media_TS(tiempo_llegadaPNH, lamda_t, 14,
                                  tiempo_servicioE, 15, 12,
                                  T,
                                  d, n_min)

print("Estimación del tiempo promedio que tarda en ser procesada una solicitud:")
print(media_TTS)
print(f"Simulaciones requeridas para la estimación: {sims}")

def intervalo95(media, alpha, scuad, n):
    z_alpha2 = norm.ppf(1-alpha/2)
    print(f" z: {z_alpha2}")
    izq = media - z_alpha2 * sqrt(scuad/n)
    der = media + z_alpha2 * sqrt(scuad/n)
    return izq, der

print(f"intervalo de confianza 95%: {intervalo95(media_TTS, 0.05, Scuad, sims)}")




