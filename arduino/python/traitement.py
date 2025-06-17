# analyse.py
# Traitement des données issues de l'acquisition Arduino

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def lire_fichier(nom_fichier):
    """Lit un fichier texte ligne par ligne et renvoie une liste de float."""
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
    L = []
    for ligne in lignes:
        L.append(float(ligne.strip()))
    return L

# 1) Chargement des données (fichier généré par Arduino)
data = lire_fichier('python/data/acq3_pendule_tige1_masse1.txt')

# 2) Construction de l'axe temps
n = len(data)
pas = 1/100          # correspond à delay(10) soit 10 ms
t = np.linspace(0, n*pas, n)

# 3) Détermination de l'enveloppe par un modèle cosinus amorti
def cosinus_amorti(x, A, omega, phi, gamma):
    return A * np.exp(-gamma * x) * np.cos(omega * x + phi)

# ajustement des paramètres
params, _ = curve_fit(cosinus_amorti, t, data)
A_fit, omega_fit, phi_fit, gamma_fit = params

# calcul de l'enveloppe exponentielle
enveloppe = A_fit * np.exp(-gamma_fit * t)

# 4) Affichage des courbes
plt.plot(t,
         cosinus_amorti(t, A_fit, omega_fit, phi_fit, gamma_fit),
         linewidth=0.8,
         label='Cosinus amorti')

plt.fill_between(t,
                 cosinus_amorti(t, A_fit, omega_fit, phi_fit, gamma_fit),
                 enveloppe,
                 alpha=0.5,
                 label='Enveloppe')

plt.fill_between(t,
                 cosinus_amorti(t, A_fit, omega_fit, phi_fit, gamma_fit),
                 -enveloppe,
                 alpha=0.5)

plt.title("$\\delta$ = " + str(round(gamma_fit, 3)) + " s$^{-1}$" +
          "\nT = " + str(round(2*np.pi/omega_fit, 3)) + " s")
plt.xlabel("Temps (s)", fontsize=14)
plt.ylabel("Accélération (g)", fontsize=14)
plt.legend()
plt.grid()
plt.savefig('results/graphique.png', dpi=300)
plt.show()
