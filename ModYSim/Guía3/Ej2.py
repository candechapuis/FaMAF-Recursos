# El desarrollo del ejercicio para encontrar el valor teórico
# de la probabilidad de ganar está en el archivo Guía3-Resoluciones.pdf
# en el ejercicio 2.
import random
import numpy as np

# un experimento
def experimento():
    u = random.random()

    if u < 0.5:
        x = random.random() + random.random()
    else:
        x = random.random() + random.random() + random.random()

    return int(x >= 1)

# estimación
def estimar_probabilidad(Nsim):
    return np.mean([experimento() for _ in range(Nsim)])

def estimar_probabilidad2(Nsim):
    exitos = 0

    for _ in range(Nsim):
        resultado = experimento()

        if resultado == 1:
            exitos += 1

    probabilidad = exitos / Nsim

    return probabilidad


# tabla
ns = [100, 1000, 10000, 100000, 1000000]

for n in ns:
    print(f"n = {n}: {estimar_probabilidad2(n)}")

print("\nValor teórico:", 2/3)