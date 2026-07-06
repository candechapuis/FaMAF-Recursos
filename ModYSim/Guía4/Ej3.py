import random
import statistics as stats

# generación de v.a uniforme discreta {1...n}

def udiscreta(n):
    U = random.random()
    return int(n * U) + 1

# experimento

def experimento():
    N = 0
    resultados = list(range(2,13))
    while len(resultados) > 0:
        dado1 = udiscreta(6)
        dado2 = udiscreta(6)
        suma = dado1 + dado2
        if suma in resultados:
            resultados.remove(suma)
        N += 1
    return N

# estadísticas

def estadísticas(Nsim):
    resultados = [experimento() for _ in range(Nsim)]
    return stats.mean(resultados), stats.stdev(resultados)

# probabilidades

def probabilidades(Nsim):
    prob15 = 0
    prob9 = 0
    for _ in range(Nsim):
        sim = experimento()
        if sim >= 15:
            prob15 += 1
        if sim <= 9:
            prob9 += 1
    prob15 = prob15/Nsim
    prob9 = prob9/Nsim
    return prob15, prob9

# estimaciones

sims = [100, 1000, 10000, 100000]
print(f"{'nsim':<10}{'media':<12}{'desv':<12}{'P(N>=15)':<12}{'P(N<=9)':<12}")
print("-"*58)
for s in sims:
    media, desv = estadísticas(s)
    p15, p9 = probabilidades(s)
    print(f"{s:<10}{media:<12.4f}{desv:<12.4f}{p15:<12.4f}{p9:<12.4f}")



