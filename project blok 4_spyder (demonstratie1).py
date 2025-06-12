# -*- coding: utf-8 -*-
"""
Created on wed jun 4 20:18:10 2025

@authors: Onno Dijkman en Gilles Honsbeek
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parameters van het systeem
m = 0.3       # massa, hoe kleiner des te lager de responstijd
k = 44.6       # veerconstante
c = 2*np.sqrt(m*k)     # kritische demping


# Inlezen van versnelling uit CSV
data = pd.read_csv('versnellingsprofiel_glad.csv')  
tijd = data['# tijd (s)'].values
aandrijving = data[' versnelling (m/s^2)'].values
Nstap = len(tijd)
dt = tijd[1] - tijd[0]  # aangenomen dat tijdstappen gelijk zijn

# Voorgedefinieerde constanten voor de numerieke oplossing
a = (k - 2 * m / dt**2) / (m / dt**2 + c / (2 * dt))
b = (m / dt**2 - c / (2 * dt)) / (m / dt**2 + c / (2 * dt))
F0e = m * aandrijving / (m / dt**2 + c / (2 * dt))  # omgerekende kracht

# Beginvoorwaarden
x0 = 0
v0 = 0

# maakt leeg array aan voor veeruitwijking en zet eerste stapje
x = np.zeros(Nstap)
x[0] = x0
x[1] = x0 + dt * v0

# Numerieke oplossing met de aangedreven kracht uit versnellingsprofiel, vult array van veeruitwijking
for ti in range(1, Nstap - 1):
    x[ti + 1] = -a * x[ti] - b * x[ti - 1] + F0e[ti]

# Plot van veeruitwijking in de tijd
plt.figure()
plt.plot(tijd, x)
plt.xlabel("Tijd (s)")
plt.ylabel("Uitwijking (m)")
plt.title("Respons van de massa op versnellingsprofiel")
plt.grid()
plt.show()

#berekening van de versnelling uit de uitwijking van de veer, geeft een array
a_uit_uitwijking = (k * x) / m

#plot van de het versnellingsprofiel
plt.figure()
plt.plot(tijd, aandrijving, label="Versnelling van versnellingsprofiel")
plt.plot(tijd, a_uit_uitwijking, label="Versnelling berekend met veeruitwijking")
plt.title("versnellingsporfiel en berekende versnelling uit veeruitwijking")
plt.ylabel("Versnelling (m/s^2)")
plt.xlabel("tijd (s)")
plt.grid()
plt.legend()
plt.show()

# Bepaalt de responstijd als het tijdsverschil tussen de piek van de systeemrespons en de piek van de input (versnellingsprofiel)
responstijd = tijd[np.argmax(a_uit_uitwijking)] - tijd[np.argmax(aandrijving)]
print('Responstijd van het systeem (100%):', responstijd, 's')

# bepaalt de responstijd voor 95% van de maximale uitwijking 
responstijd_95 = tijd[np.argmax(a_uit_uitwijking >= 0.95 * np.max(a_uit_uitwijking))] - tijd[np.argmax(aandrijving)]
print("Responstijd (95%):", responstijd_95, "s")

#Zet de uitwijking en versnelling in een csv bestand
uitwijking = pd.DataFrame({"tijd (s)": tijd,
    "uitwijking (m)": x})
uitwijking.to_csv("uitwijking.csv", index=False)

versnelling_veer = pd.DataFrame({"tijd (s)": tijd,
    "versnelling": aandrijving})

versnelling_veer.to_csv("versnelling.csv", index=False)
