# coding: utf-8
"""
V21 Skript zum komfortablen Berechnen von Parametern
 
Sie sollten dieses Skript so anpassen, dass Sie im Versuch zusammen mit den experimentell bestimmten Parametern sowie den in der Vorbereitung ermittelten Ausdrücken für die Parameter der Übertragungsfunktion schnell alles weitere berechnen können, um nicht unnötig mit dem Taschenrechner herumhantieren zu müssen.
 
Beachten Sie, dass Sie in SI-Einheiten rechnen!
"""
import numpy as np
import matplotlib.pyplot as mpl


AB = 2.8274e-3  # Ballquerschnitt in m^2 
ASp = 0.4299e-3 # Luftspaltfläche in m^2
g = 9.81        # Erdbeschleunigung in m/s^2
m = 2.8e-3      # Masse des Balls in kg
XXX = 1.23      # nur Platzhaltervariable, damit Skript durchläuft


# Experimentell bestimmte Grunddrehzahl in s^{-1}
eta0 = XXX
print('eta0 = %e s^{-1}' % eta0)


# Formel zur Berechnung von kL
hDotExp = XXX  # experimentell bestimmter Wert für die Fallgeschwindigkeit des Balls in m/s
kL = m * g * (ASp / (AB * hDotExp)) ** 2
print('kL = %e kg/m' % kL)


# Formel zur Berechnung von kV (Wurzel -> np.sqrt(...))
hDotExp = XXX  # experimentell bestimmter Wert für die Steiggeschwindigkeit des Balls in m/s
etaExp = XXX  # experimentell bestimmter Wert für die Lüfterdrehgeschwindigkeit während des Steigens in s^{-1}
kV = (np.sqrt(m * g / kL) * ASp + AB * hDotExp) / etaExp
print('kV = %e m^3' % kV)


# Bestimmte Werte für kM und TM aus Identifikationsskript
kM = XXX
TM = XXX
print('kM = %e s^{-1}, TM = %e s' % (kM, TM))


# Berechnung der Standard-Parameter der Übertragungsfunkion
K = kV / AB
T0 = 1 / kM
T1 = TM
T2 = ASp * np.sqrt(m / (g * kL)) / (2 * AB)
print('K = %e m, T0 = %e s, T1 = %e s, T2 = %e s' % (K, T0, T1, T2))


# Berechnung der Reglerparameter nach dem ... Optimum
Kp = XXX
Ti = XXX
Td = XXX
print('Kp = %e m^{-1}, Ti = %e s, Td = %e s' % (Kp, Ti, Td))

