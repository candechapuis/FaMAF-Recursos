from math import inf, log
from random import random

def sim_reparacion(n, s, F_falla, G_reparacion):
    # tiempo de sim transcurrido
    t = 0
    # máquinas averiadas actuales
    r = 0
    # cola máquinas en reparación
    Qr = []
    # tiempos de falla
    Tf = []
    for i in range(n):
        fi = F_falla()
        Tf.append(fi)
    Tf.sort()
    print(f"Luego del sort Tf = {Tf}")
    # tiempo de finalización de reparación actual
    tr = inf
    while r <= s:
        prox_evento = min(min(Tf), tr)
        if prox_evento != tr:
            t = prox_evento
            r += 1
            # Qr.append(prox_evento)
            if r > s:
                print("COLAPSO del sistema")
                break
            if r == 1:
                rep = G_reparacion()
                tr = t + rep
            Tf[0] = inf
            Tf.sort()
        else:
            t = tr 
            # Qr.pop(0)
            r -= 1
            fallaJ = F_falla()
            Tf.append(fallaJ)
            if r > 0:
                rep = G_reparacion()
                tr = t + rep
            else:
                tr = inf
            Tf.sort()
    # registro el tiempo de colapso
    T = t
    return T

def tiempo_falla():
    return -log(1-random()) / 2

def tiempo_reparacion():
    return -log(1-random()) / 3

T = sim_reparacion(6, 4, tiempo_falla, tiempo_reparacion)
print(f"tiempo de colapso del sistema: {T}")




