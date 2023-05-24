import scipy.special as sp
import numpy as np
import math
import xlwings 
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import figure


def CalculTemperature(Temperature,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY):
    res_t = fact*np.ones(t_fin_filtre)
    vect_t = np.ones(t_fin_filtre)
    vt = np.ones(n_sortie)
    Temperature_vf = np.ones(n_sortie)
    
    
    Moy = 0
    n = 300
    for i in range(0,n):
        Moy = Moy + Temperature[i]

    Moy = Moy/(n)
    

    if (Moy< 50):
        Moy_Corr = 30
        k_test = -1
        Moy_dec = Moy+0.045
    else:
        Moy_Corr = 80
        Moy_dec = Moy-0.9
        k_test = 1
        
    for i in range(0,t_fin_filtre):
        vect_t[i] = i/f
    
    for i in range(0,t_fin_filtre-4):
        if (k_test>0):
            if (Temperature[i]<Moy_dec and Temperature[i+1]<Moy_dec and Temperature[i+2]<Moy_dec and Temperature[i+3]<Moy_dec and Temperature[i+4]<Moy_dec):
                res_t[i] = i/f
        
            else:
                res_t[i] = fact

        else:
            if (Temperature[i]>Moy_dec and Temperature[i+1]>Moy_dec and Temperature[i+2]>Moy_dec and Temperature[i+3]>Moy_dec and Temperature[i+4]>Moy_dec):
                res_t[i] = i/f
        
            else:
                res_t[i] = fact

    t_debut = min(res_t)

    for i in range(0,t_fin_filtre):
        vect_t[i] = vect_t[i] - t_debut


    for i in range(0,n_sortie):
        vt[i] = vect_t[f_sortie*i]
        if(k_test>0):
            Temperature_vf[i] = Temperature[f_sortie*i] + (Moy_Corr-Moy)*Avec_Offset_AxeY
        else:
            Temperature_vf[i] = Temperature[f_sortie*i] + (Moy_Corr-Moy)*Avec_Offset_AxeY
    return [vt,Temperature_vf]
