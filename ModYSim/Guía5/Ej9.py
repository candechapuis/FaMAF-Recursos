from random import random, gauss, normalvariate
from math import log, sqrt
from statistics import mean, variance

def Normal_rechazo(mu, sigma):
    while True:
        Y1 = -log(1 - random())
        Y2 = -log(1 - random())
        if Y2 >=(Y1-1) ** 2 / 2:
            if random() < 0.5:
                return Y1 * sigma + mu
        return -Y1 * sigma + mu
    
# def MetodoPolar(mu, sigma):
#     Rcuadrado = -2 * log( 1 - random() )
#     Theta= 2 * pi * random()
#     X= sqrt(Rcuadrado) * cos(Theta)
#     Y= sqrt(Rcuadrado) * sen(Theta)
#     return (X * sigma + mu, Y * sigma + mu)
# Ya es una función implementada de python: random.gauss(mu, sigma)

def Polar_Box_Muller(mu, sigma):
    while True:
        V1, V2 = 2 * random()-1, 2 * random()-1
        if V1 ** 2 + V2 ** 2 <= 1:
            S = V1 ** 2 + V2 ** 2
            X = V1 * sqrt(-2 * log(S) / S)
            Y = V2 * sqrt(-2 * log(S) / S)
            return X * sigma + mu, Y * sigma + mu
    
# NV_MAGICCONST = 4 * exp(-0.5) / sqrt(2.0)
# def normalvariate(mu, sigma):
#     while 1:
#         u1 = random()
#         u2 = 1.0 - random()
#         z = NV_MAGICCONST * (u1 - 0.5) / u2
#         zz = z * z / 4.0
#         if zz <= -log(u2):
#             break
#         return mu + z * sigma
# Ya es una función implementada de Python: random.normalvariate(mu, sigma)

def sim(Nsim, mu, sigma):
    expNormal = []
    polarNormal = []
    polarBoxNormalX = []
    polarBoxNormalY = []
    ratioNormal = []
    for i in range(Nsim):
        expNormal.append(Normal_rechazo(mu, sigma))
        polarNormal.append(gauss(mu, sigma))
        polarBoxNormalX.append(Polar_Box_Muller(mu, sigma)[0])
        polarBoxNormalY.append(Polar_Box_Muller(mu, sigma)[1])
        ratioNormal.append(normalvariate(mu, sigma))
    print(f"{'método':<12}{'media':<10}{'varianza':<10}")
    print(f"{'exp':<12}{mean(expNormal):<10.4f}{variance(expNormal):<10.4f}")
    print(f"{'polar':<12}{mean(polarNormal):<10.4f}{variance(polarNormal):<10.4f}")
    print(f"{'polarBox X':<12}{mean(polarBoxNormalX):<10.4f}{variance(polarBoxNormalX):<10.4f}")
    print(f"{'polarBox Y':<12}{mean(polarBoxNormalY):<10.4f}{variance(polarBoxNormalY):<10.4f}")
    print(f"{'ratio':<12}{mean(ratioNormal):<10.4f}{variance(ratioNormal):<10.4f}")

sim(10000, 30, 0.5)