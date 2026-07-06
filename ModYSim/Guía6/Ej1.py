from random import gauss
from math import sqrt


def normal_estándar(d):
    mediaX = gauss(0,1)
    n = 1
    Scuad = 1
    while n < 100 or sqrt(Scuad/n) > d:
        n += 1
        mediaAnt = mediaX
        mediaX = mediaAnt + (gauss(0,1)-mediaAnt)/n 
        Scuad = Scuad * (1 - 1/(n-1)) + n*(mediaX - mediaAnt)**2
    return n, mediaX, Scuad

print(f"datos generados: {normal_estándar(0.1)[0]}")
print(f"media muestral: {normal_estándar(0.1)[1]}")
print(f"varianza muestral: {normal_estándar(0.1)[2]}")

