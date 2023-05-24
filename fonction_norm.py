import numpy as np
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt


##########CONSTANTES#########

f = 500              ## Frequence (en Hz) de l'acquisition des données
t_fin = 15           ##temps final (en s) où l'on considère que les données ensuites ne sont pas à considérer
f_sortie = 1        ##facteur de réduction de la taille du fichier de sortie (on récupère une valeur tous les f_sortie"

largeur_graph = 12         ## Largeur (en cm) du graph enregistré
hauteur_graph = 8          ## Hauteur (en cm) du graph enregistré

Avec_Offset_AxeY = 1          ## Si on veut appliquer un offset pour superposer les graphes au début: mettre 1 sinon 0 

fact = 1000000                          #A ne pas toucher a priori
t_fin_filtre = t_fin*f                  #A ne pas toucher a priori 
n_sortie=int(t_fin_filtre/f_sortie)     #A ne pas toucher a priori 

colonne_extraire = 0               # numéro de la colonne à extraire (0 -> première colonne du fichier txt)

####Calcul la derivée seconde discrete
def derive_second (x, f) :
    derive_second_liste = []
    for i in range(1, len(f)-1) :
        derive_second_values = (f[i+1]+f[i-1]-2*f[i])/(x[i+1]-x[i-1])
        derive_second_liste.append(derive_second_values)
    return derive_second_liste


####moyenne mobile pour le debruitage de la serie (lissage)
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def normalise(brut_data) :
    data_output = []
    time = brut_data[:,0]
    shape = np.shape(brut_data)
    k = 5
    for i in range(1 , shape[1]) :
        temperature = brut_data[:,i]
        temperature_liss = moving_average(temperature, k)
        time_liss = time[:len(temperature_liss)]
        derive_temp_liss = derive_second(time_liss, temperature_liss)
        
        indice_inflexion = derive_temp_liss.index(np.abs(max(derive_temp_liss)))
        #point_inflexion = time[indice_inflexion]
        
        output = temperature[indice_inflexion-4*f : indice_inflexion+3*f]
        data_output.append(output)
        data_output = np.array(data_output)
        
    return data_output