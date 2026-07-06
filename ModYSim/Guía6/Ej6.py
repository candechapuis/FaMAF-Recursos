from random import random, choices

def media_muestral(datos):
    return sum(datos)/len(datos)

def S2(datos):
    n = len(datos)
    media = media_muestral(datos)
    return sum((d - media)**2 for  d in datos)/(n-1)


def var_boot(datos, B):
    S2_boot = []
    for i in range(B):
        S2_i = S2(choices(datos, k=len(datos)))
        S2_boot.append(S2_i)
    media_S2 = sum(S2_boot) / B
    var_S2_i = sum((m - media_S2)**2 for m in S2_boot) / (B-1)
    return var_S2_i

datos = [5,4,9,6,21,17,11,20,7,10,21,15,13,16,8]
print(f"Estimación bootstrap de la varianza de S²(n) con n = 15:")
print(var_boot(datos, 500))
    