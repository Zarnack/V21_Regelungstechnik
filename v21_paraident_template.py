# -*- coding: utf-8 -*-
########################### Abschnitt 1 ###################################
import numpy as np
import scipy.integrate as sci
import scipy.optimize as sco
import matplotlib.pyplot as plt

# Wenn True werden nur u und eta über den Tastschritten angezeigt
plot_raw_data = False


########################### Abschnitt 2 ################################### 

# Daten laden, erste Zeile auslassen, da dort Spaltennamen stehen
Data = np.loadtxt("v21_testdaten.csv", skiprows=1)
########################### Abschnitt 3 ###################################

# Wenn plot_raw_data == True werden u und etaAbs über den Abtastschritten
# geplottet. Das Skript wird anschließend beendet
if plot_raw_data:

    u = Data[:,6]
    etaAbs = Data[:,7]

    plt.figure()
    #plt.figure(figsize=(9, 9))
    plt.plot(u)
    plt.plot(etaAbs)
    plt.legend(['u (PWM)', 'eta'])
    plt.xlabel('Index')
    plt.ylabel('u bzw. eta in U/min')
    plt.yticks(np.arange(0, 3500, 200.0))
    plt.xticks(np.arange(0, 210, 20.0))
    plt.show()
    
    quit()
 
    
########################### Abschnitt 4 ###################################    

# Daten zurechtschneiden
iStart = 0
iStop = 236
Data = Data[iStart:iStop,:]

# Alle Größen in SI-Einheiten laden [t] = s, [eta] = s^{-1}!
t = Data[:, 0]
u = Data[:, 6]            # PWM-Wert der Motorspannung
etaAbs = Data[:, 7] * 1/60     # Lüfterdrehzahl in s^{-1}
etaDot = Data[:, 8] * 1 /60    # Zeitableitung der Lüfterdrehzahl in s^{-2}

# Hilfsgrößen
etaAbs0 = etaAbs[0]   # Lüfterdrehungszahl für u = 0
eta = etaAbs - etaAbs[0]          # Differenz-Lüfterdrehzahl bezogen auf etaAbs0


########################### Abschnitt 5 ###################################

# Systemdynamik (rechte Seite Dgl. PT1-Glied)
def pt1_sys(x, t, T_para, K_para, t_data, u_data):
    
    # u an der Stelle t im durch t_data und u_data definierten Verlauf
    u = u_data[max(0, len(t_data[t_data<=t])-1)]
    
    xDot = (-x + K_para*u_data)/T_para  # hier rechte Seite Dgl. implementieren
    return xDot


########################### Abschnitt 6 ###################################

# Kostenfunktional für Simplex-Algorithmus
def cost_functional_pt1(Para, t_data, u_data, eta_data):
    T, K = Para
    
    # Simulation System mit Parametern T und K für den Eingangssignalverlauf 
    # t_data, u_data, [:,0] sorgt dafür, dass etaSim ein 1-dim. Array ist

    etaSim = sci.odeint(fun, np.zeros(len(eta)), t_data, args=(K, u_data, T))[:, 0]
    
    # Berechnung Kostenfunktional 
    J = np.sum((eta_data-etaSim)**2)
    return J


########################### Abschnitt 7 ###################################
# Parameteridentifikation (MKQ)

Phi = np.column_stack([eta, u])
y = etaDot
a = (np.linalg.inv(Phi.T@Phi))@Phi.T@y     # Nutzen Sie np.linalg.inv, @, .T (siehe Anleitung)

# Parameter ausgeben
T_MKQ = -1/a[0]
km_MKQ = -a[1]/a[0]
print('MKQ                  : T = %f ms, km = %f 1/s' % (T_MKQ*1000, km_MKQ))

# Simulation des Systems mit den identifizierten Parametern


def fun(eta, t, K, u, T):
    return (K * u - eta) / T


etaSim_MKQ = sci.odeint(fun, eta[0], t, args=(km_MKQ, u, T_MKQ))


########################### Abschnitt 8 ###################################
# Parameteridentifikation (Simplex-Algorithmus)
    
TInit = 0.5
KInit = 5
temp = [TInit, KInit]
xMin = sco.fmin(cost_functional_pt1, [TInit,KInit], args=(t,u,eta), disp = 1)

# Parameter ausgeben
T_Simplex, km_Simplex = xMin
print('Simplex (Nelder-Mead): T = %f ms, km = %f 1/s' % (T_Simplex*1000, km_Simplex))

# Simulation des Systems mit den identifizierten Parametern


etaSim_Simplex = sci.odeint(fun, eta[0], t, args=(T_Simplex, u, km_Simplex))


########################### Abschnitt 9 ###################################
# Ergebnis darstellen

plt.figure()
plt.plot(t, etaAbs*60, t, (etaAbs0+etaSim_MKQ)*60, '-+', t, (etaAbs0+etaSim_Simplex)*60, '-x', markersize=8, markevery=5)
plt.ylabel('Lüfterdrehzahl eta (U/min)')
plt.xlabel('Zeit t (s)')
plt.title('Vergleich Messdaten und Identifikation')
plt.legend(['Experiment', 'Identifikation (MKQ)', 'Identifikation (Simplex)'], loc='lower right')
plt.grid()

plt.show()