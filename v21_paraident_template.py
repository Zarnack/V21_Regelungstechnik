# -*- coding: utf-8 -*-
########################### Abschnitt 1 ###################################
import numpy as np
import scipy.integrate as sci
import scipy.optimize as sco
import matplotlib.pyplot as plt

# Wenn True werden nur u und eta über den Tastschritten angezeigt
plot_raw_data = True


########################### Abschnitt 2 ################################### 

# Daten laden, erste Zeile auslassen, da dort Spaltennamen stehen
Data = np.loadtxt(XXX, skiprows=1)


########################### Abschnitt 3 ###################################

# Wenn plot_raw_data == True werden u und etaAbs über den Abtastschritten
# geplottet. Das Skript wird anschließend beendet
if plot_raw_data:

    u = Data[:,6]
    etaAbs = Data[:,7]
    
    plt.figure()
    plt.plot(u, hold=True)
    plt.plot(etaAbs)
    plt.legend(['u (PWM)', 'eta'])
    plt.xlabel('Index')
    plt.ylabel('u bzw. eta in U/min')
    plt.show()
    
    quit()
 
    
########################### Abschnitt 4 ###################################    

# Daten zurechtschneiden
iStart = XXX
iStop =  XXX  
Data = Data[iStart:iStop,:]

# Alle Größen in SI-Einheiten laden [t] = s, [eta] = s^{-1}!
t = XXX
u = XXX            # PWM-Wert der Motorspannung
etaAbs = XXX       # Lüfterdrehzahl in s^{-1}
etaDot = XXX       # Zeitableitung der Lüfterdrehzahl in s^{-2}

# Hilfsgrößen
etaAbs0 = XXX      # Lüfterdrehungszahl für u = 0
eta = XXX          # Differenz-Lüfterdrehzahl bezogen auf etaAbs0


########################### Abschnitt 5 ###################################

# Systemdynamik (rechte Seite Dgl. PT1-Glied)
def pt1_sys(x, t, T_para, K_para, t_data, u_data):
    
    # u an der Stelle t im durch t_data und u_data definierten Verlauf
    u = u_data[max(0, len(t_data[t_data<=t])-1)]
    
    xDot = XXX  # hier rechte Seite Dgl. implementieren     
    return xDot


########################### Abschnitt 6 ###################################

# Kostenfunktional für Simplex-Algorithmus
def cost_functional_pt1(Para, t_data, u_data, eta_data):
    T, K = Para
    
    # Simulation System mit Parametern T und K für den Eingangssignalverlauf 
    # t_data, u_data, [:,0] sorgt dafür, dass etaSim ein 1-dim. Array ist
    etaSim = sci.odeint(XXX)[:,0]  
    
    # Berechnung Kostenfunktional 
    J = np.sum(XXX)   
    return J


########################### Abschnitt 7 ###################################
# Parameteridentifikation (MKQ)

Phi = np.column_stack([XXX, XXX])
y = XXX
a = XXX     # Nutzen Sie np.linalg.inv, @, .T (siehe Anleitung)

# Parameter ausgeben
T_MKQ = XXX
km_MKQ = XXX
print('MKQ                  : T = %f ms, km = %f 1/s' % (T_MKQ*1000, km_MKQ))

# Simulation des Systems mit den identifizierten Parametern
etaSim_MKQ = sci.odeint(XXX)


########################### Abschnitt 8 ###################################
# Parameteridentifikation (Simplex-Algorithmus)
    
TInit = 0.5
KInit = 5
xMin = sco.fmin(XXX)

# Parameter ausgeben
T_Simplex, km_Simplex = xMin
print('Simplex (Nelder-Mead): T = %f ms, km = %f 1/s' % (T_Simplex*1000, km_Simplex))

# Simulation des Systems mit den identifizierten Parametern
etaSim_Simplex = sci.odeint(XXX)


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