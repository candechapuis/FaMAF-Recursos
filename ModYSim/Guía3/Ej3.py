## El desarrollo del ejercicio para encontrar el valor teórico
# de la probabilidad de ganar está en el archivo Guía3-Resoluciones.pdf
# en el ejercicio 3.
import random
import numpy as np 

# experimento

def experimento():

    u = random.random()

    if u < (1/3):
        x = random.random() + random.random()
    else: 
        x = random.random() + random.random() + random.random()

    return int(x<=2)

# estimación usando Monte Carlo

def estimar_probabilidad_mc(Nsim):
    return np.mean([experimento() for _ in range(Nsim)])

sims = [100, 1000, 10000, 100000, 1000000]

for s in sims:
    print(f"simulaciones = {s}, p(ganar) = {estimar_probabilidad_mc(s)}")
print("Valor teórico de p(ganar): ", 8/9)