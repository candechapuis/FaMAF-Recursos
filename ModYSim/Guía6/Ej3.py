from random import random 
from math import sin, pi, sqrt
from scipy.stats import norm

def h(y):
    return sin((y+1)*pi)/(y+1)

def z(alpha):
    return norm.ppf(1-alpha/2)

def Monte_Carlo(h, n_min, alpha, L):
    z_alpha_2 = z(alpha)
    d = L / (2*z_alpha_2)
    media = h(random())
    n = 1
    Scuad = 0
    stats = []
    while n <= n_min or sqrt(Scuad/n) > d:
        n += 1
        media_ant = media
        media = media_ant + (h(random())-media_ant) / n 
        Scuad = Scuad * (1-1/(n-1)) + n* (media - media_ant)**2
        if n == 1000 or n == 5000 or n == 7000:
            stats.append((media, Scuad, intervalo(media, Scuad, n, alpha)))
    return media, Scuad, n, stats

def intervalo(media, Scuad, n, alpha):
    izq = media - z(alpha) * sqrt(Scuad/n)
    der = media + z(alpha) * sqrt(Scuad/n)
    intervalo = f"[{izq:.4f},{der:.4f}]"
    return intervalo

alpha = 0.05
media, Scuad, n, stats = Monte_Carlo(h, 1, alpha, 0.002)

print(f"{'n° sim':<12}{'media m':<12}{'desvío m':<12}{'IC(95%)':<12}")
print(f"{'1000':<12}{stats[0][0]:<12.4f}{sqrt(stats[0][1]):<12.4f}{stats[0][2]:<12}")
print(f"{'5000':<12}{stats[1][0]:<12.4f}{sqrt(stats[1][1]):<12.4f}{stats[1][2]:<12}")
print(f"{'7000':<12}{stats[2][0]:<12.4f}{sqrt(stats[2][1]):<12.4f}{stats[2][2]:<12}")
print(f"{'(min)'}{n:<7}{media:<12.4f}{sqrt(Scuad):<12.4f}{intervalo(media, Scuad, n, alpha):<12}")