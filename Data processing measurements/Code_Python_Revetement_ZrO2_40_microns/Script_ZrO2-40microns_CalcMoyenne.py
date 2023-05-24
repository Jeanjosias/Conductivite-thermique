# -*- coding: utf-8 -*-
"""
Code réalisant:

    STEP 1:  Lecutre de fichier .txt dans lequel on supprimer la première ligne (entête du fichier), lire un certain nombre de lignes
    et pour une ou plusieurs collones;

    STEP 2: Transformer les données afin de pouvoir superposer les graphes à la même échelle
    
    STEP 3: Affichage du graphe final

    STEP 4: Enregistrement du fichier .txt de sortie et d'une image.png

    Les paramètres d'entrés du modèle :
    
        - f : fréquence en Hz d'acquisition des données (afin de pouvoir déterminer à quel temps la mesure a été réalisée
        - t_fin : le temps final (en s) où l'on considère que les données ensuites ne sont pas à considérer
        - f_sortie: facteur de réduction de la taille du fichier de sortie (on récupère une valeur tous les f_sortie"
        - largeur_graph et hauteur_graph: Largeur et hauteur (en cm) du graph enregistrer

"""
import scipy.special as sp
import numpy as np
import math
import xlwings 
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import figure

##from Function_ExtractData_txt import CalculTemperature

plt.close("all")







"""________________________________________________________________________"""
"""       DEBUT PARAMETRES DU MODELE      """
f = 500              ## Frequence (en Hz) de l'acquisition des données
t_fin = 15           ##temps final (en s) où l'on considère que les données ensuites ne sont pas à considérer
f_sortie = 25        ##facteur de réduction de la taille du fichier de sortie (on récupère une valeur tous les f_sortie"

largeur_graph = 20         ## Largeur (en cm) du graph enregistré
hauteur_graph = 15          ## Hauteur (en cm) du graph enregistré

Avec_Offset_AxeY = 1          ## Si on veut appliquer un offset pour superposer les graphes au début: mettre 1 sinon 0 

fichier1 = 'ZrO2-40microns-repet1.txt'
fichier2 = 'ZrO2-40microns-repet2.txt'
fichier3 = 'ZrO2-40microns-repet3.txt'
##fichier4 = '20221019_123100_Surveillance_RMS_15-11.txt'
##fichier5 = '20221019_103854_Surveillance_RMS_14-11.txt'
##fichier6 = '20221019_105022_Surveillance_RMS_14-11.txt'
##fichier7 = '20221019_110524_Surveillance_RMS_14-11.txt'
##fichier8 = '20221019_111730_Surveillance_RMS_14-11.txt'
##fichier9 = '20221004_160317_Surveillance_RMS.txt'
##fichier10 = '20221004_162035_Surveillance_RMS.txt'


nom_fichier_sortie_png = 'ZrO2-40microns_Moy.png'
nom_fichier_sortie_txt = 'ZrO2-40microns_Moy'

##  TRES IMPORTANT: IL FAUT QUE LE FICHIER .TXT comporte "." plutôt que "," 

colonne_extraire = 0                # numéro de la colonne à extraire (0 -> première colonne du fichier txt)

"""       FIN PARAMETRES DU MODELE      """
"""________________________________________________________________________"""




 
fact = 1000000                          #A ne pas toucher a priori
t_fin_filtre = t_fin*f                  #A ne pas toucher a priori 
n_sortie=int(t_fin_filtre/f_sortie)     #A ne pas toucher a priori 


# STEP 1 Lecture du fichier et extraction de la colonne numéro  colonne_extraire
Temperature  = np.loadtxt( fichier1 , skiprows=1, usecols=colonne_extraire )
Temperature2 = np.loadtxt( fichier2 , skiprows=1,  usecols=colonne_extraire )
Temperature3 = np.loadtxt( fichier3 , skiprows=1,   usecols=colonne_extraire )
##Temperature4 = np.loadtxt( fichier4 , skiprows=1,   usecols=colonne_extraire )
##Temperature5 = np.loadtxt( fichier5 , skiprows=1,  usecols=colonne_extraire )
##Temperature6 = np.loadtxt( fichier6 , skiprows=1,  usecols=colonne_extraire )
##Temperature7 = np.loadtxt( fichier7 , skiprows=1,  usecols=colonne_extraire )
##Temperature8 = np.loadtxt( fichier8 , skiprows=1,  usecols=colonne_extraire )
##Temperature9 = np.loadtxt( fichier9 , skiprows=1,  usecols=colonne_extraire )
##Temperature10 = np.loadtxt( fichier10 , skiprows=1,  usecols=colonne_extraire )


def CalculTemperature(Temperature,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY):
    res_t = fact*np.ones(t_fin_filtre)
    vect_t = np.ones(t_fin_filtre)
    vt = np.ones(n_sortie)
    Temperature_vf = np.ones(n_sortie)
    
    indice_reinit = 0
    Offset_correctif = 0   
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
        Moy_dec = Moy-0.5
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

    for i in range(1,t_fin_filtre):
        if ( (vect_t[i-1] < 0) and (vect_t[i] > 0) ) :
            Offset_correctif = vect_t[i]
            
    for i in range(0,t_fin_filtre):
        vect_t[i] = vect_t[i] - Offset_correctif

    for i in range(0,n_sortie):
        vt[i] = vect_t[f_sortie*i]
        if(k_test>0):
            Temperature_vf[i] = Temperature[f_sortie*i] + (Moy_Corr-Moy)*Avec_Offset_AxeY
        else:
            Temperature_vf[i] = Temperature[f_sortie*i] + (Moy_Corr-Moy)*Avec_Offset_AxeY
            
    for i in range(0,n_sortie):
        if ( (vt[i-1] < 0) and (vt[i] > 0) ) :
            Offset_correctif = vt[i]
            
    for i in range(0,n_sortie):
        vt[i] = vt[i] - Offset_correctif

    for i in range(0,n_sortie):
        if (vt[i] == 0) :
            indice_reinit = i 
    
    
    return [vt,Temperature_vf,indice_reinit]




# STEP 2 Application de la fonction CalculTemperature pour transformer les données
[vt1,T_vf1,i1] = CalculTemperature(Temperature  ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
[vt2,T_vf2,i2] = CalculTemperature(Temperature2 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
[vt3,T_vf3,i3] = CalculTemperature(Temperature3 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt4,T_vf4,i4] = CalculTemperature(Temperature4 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt5,T_vf5,i5] = CalculTemperature(Temperature5 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt6,T_vf6,i6] = CalculTemperature(Temperature6 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt7,T_vf7,i7] = CalculTemperature(Temperature7 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt8,T_vf8,i8] = CalculTemperature(Temperature8 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt9,T_vf9,i9] = CalculTemperature(Temperature9 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt10,T_vf10,i10] = CalculTemperature(Temperature10 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)


indice_min = min(i1,i2,i3)
indice_max = max(i1,i2,i3)


indice_delta = indice_max - indice_min

n_sortie_off = n_sortie - indice_delta


vt1_cor = [0] * (n_sortie_off)
T_vf1_corr = [0] * (n_sortie_off)

vt2_cor = [0] * (n_sortie_off)
T_vf2_corr = [0] * (n_sortie_off)

vt3_cor = [0] * (n_sortie_off)
T_vf3_corr = [0] * (n_sortie_off)

##vt4_cor = [0] * (n_sortie_off)
##T_vf4_corr = [0] * (n_sortie_off)

##vt5_cor = [0] * (n_sortie_off)
##T_vf5_corr = [0] * (n_sortie_off)

##vt6_cor = [0] * (n_sortie_off)
##T_vf6_corr = [0] * (n_sortie_off)

##vt7_cor = [0] * (n_sortie_off)
##T_vf7_corr = [0] * (n_sortie_off)

##vt8_cor = [0] * (n_sortie_off)
##T_vf8_corr = [0] * (n_sortie_off)

##vt9_cor = [0] * (n_sortie_off)
##T_vf9_corr = [0] * (n_sortie_off)

##vt10_cor = [0] * (n_sortie_off)
##T_vf10_corr = [0] * (n_sortie_off)

#vt11_cor = [0] * (n_sortie_off)
#T_vf11_corr = [0] * (n_sortie_off)

TVF_MOY = [0] * (n_sortie_off)





def ResizeVect(vt,T_vf,ind,ind_min,n_s):
    vt_cor = [0] * (n_s)
    T_vf_corr = [0] * (n_s)
    indice_corr = ind - ind_min
    
    if (ind == indice_min):
        for k in range(0,n_s):
            vt_cor[k]    = vt[k]
            T_vf_corr[k] = T_vf[k]
    else: 
        for k in range(0,n_s):
            vt_cor[k]    = vt[k + indice_corr]
            T_vf_corr[k] = T_vf[k + indice_corr]

    return [vt_cor,T_vf_corr]


[vt1_cor,T_vf1_corr] = ResizeVect(vt1,T_vf1,i1,indice_min,n_sortie_off)
[vt2_cor,T_vf2_corr] = ResizeVect(vt2,T_vf2,i2,indice_min,n_sortie_off)
[vt3_cor,T_vf3_corr] = ResizeVect(vt3,T_vf3,i3,indice_min,n_sortie_off)
##[vt4_cor,T_vf4_corr] = ResizeVect(vt4,T_vf4,i4,indice_min,n_sortie_off)
##[vt5_cor,T_vf5_corr] = ResizeVect(vt5,T_vf5,i5,indice_min,n_sortie_off)
##[vt6_cor,T_vf6_corr] = ResizeVect(vt6,T_vf6,i6,indice_min,n_sortie_off)
##[vt7_cor,T_vf7_corr] = ResizeVect(vt7,T_vf7,i7,indice_min,n_sortie_off)
##[vt8_cor,T_vf8_corr] = ResizeVect(vt8,T_vf8,i8,indice_min,n_sortie_off)
##[vt9_cor,T_vf9_corr] = ResizeVect(vt9,T_vf9,i9,indice_min,n_sortie_off)
##[vt10_cor,T_vf10_corr] = ResizeVect(vt10,T_vf10,i10,indice_min,n_sortie_off)



T_vf_min = [0] * (n_sortie_off)
T_vf_max = [0] * (n_sortie_off)

T_vf_list= np.array([T_vf1_corr, T_vf2_corr, T_vf3_corr])

#print (T_vf_list[0,0])

MAX = 0 
MIN = 100000
for n in range(0,3):
    if(T_vf_list[n,n_sortie_off-1]>MAX): 
        MAX = T_vf_list[n,n_sortie_off-1]
        for k in range(0,n_sortie_off):
            T_vf_max[k] = T_vf_list[n,k] 
            
for n in range(0,3):
    if(T_vf_list[n,n_sortie_off-1]<MIN): 
        MIN = T_vf_list[n,n_sortie_off-1]
        for k in range(0,n_sortie_off):
            T_vf_min[k] = T_vf_list[n,k] 


#
#
#
#for i in range(0,9):
    

for k in range(0,n_sortie_off):
        TVF_MOY[k]    = (T_vf1_corr[k] + T_vf2_corr[k]+ T_vf3_corr[k])/3

# STEP 3 Affichage
plt.rc('font', size=8)



fig, ax = plt.subplots()
ax.set_xlabel("Time [s]")
ax.set_ylabel("Temperature [°C]")
ax.grid(True,linestyle='--')
#
##ax.plot(vt1,T_vf1,'b-',label='Fichier 1')
##ax.plot(vt2,T_vf2,'r-',label='Fichier 2')
##ax.plot(vt3,T_vf3,'g-',label='Fichier 3')
#ax.plot(vt4,T_vf4,'k-',label='Fichier 4')
#ax.plot(vt5,T_vf5,'m-',label='Fichier 5')
#ax.plot(vt6,T_vf6,'y-',label='Fichier 6')
#ax.plot(vt7,T_vf7,'b--',label='Fichier 7')
#ax.plot(vt8,T_vf8,'r--',label='Fichier 8')
#ax.plot(vt9,T_vf9,'g--',label='Fichier 9')
#ax.plot(vt10,T_vf10,'k--',label='Fichier 10')









##fig, ax = plt.subplots()
##ax.set_xlabel("Time [s]")
##ax.set_ylabel("Temperature [°C]")
##ax.grid(True,linestyle='--')
ax.set(ylim=(50, 90), 
 #      xlim=(0, 12), 
       )

##ax.plot(vt1_cor,T_vf1_corr,'b-',label='EXP 1')
##ax.plot(vt2_cor,T_vf2_corr,'r-',label='EXP 2')
##ax.plot(vt3_cor,T_vf3_corr,'g-',label='EXP 3')
##ax.plot(vt4_cor,T_vf4_corr,'k-',label='EXP 4')
##ax.plot(vt5_cor,T_vf5_corr,'m-',label='EXP 5')
##ax.plot(vt6_cor,T_vf6_corr,'y-',label='EXP 6')
##ax.plot(vt7_cor,T_vf7_corr,'b--',label='EXP 7')
##ax.plot(vt8_cor,T_vf8_corr,'r--',label='EXP 8')
##ax.plot(vt9_cor,T_vf9_corr,'g--',label='EXP 9')
##ax.plot(vt10_cor,T_vf10_corr,'k--',label='EXP 10')


ax.plot(vt1_cor,T_vf_min,'k-',label='Min')
ax.plot(vt1_cor,T_vf_max,'k-',label='Max')
ax.plot(vt1_cor,TVF_MOY,'k--',label='Moyenne')
##plt.fill_between(vt1_cor, T_vf_min,T_vf_max,interpolate=True,alpha=0.25, color='k')

##mpl.rcParams["legend.labelcolor"]='linecolor'
plt.legend(loc='upper right') ##,labelcolor='linecolor')

fig.set_size_inches(largeur_graph/2.54, hauteur_graph/2.54, forward=True)
fig = plt.gcf()
fig.savefig(nom_fichier_sortie_png, dpi=300)
plt.show()



# STEP 4 Sauvegarde

mat = np.array([vt1_cor,T_vf_min,T_vf_max,TVF_MOY]) 
mat= mat.T
np.savetxt(nom_fichier_sortie_txt+'.txt',mat,fmt='%.5f')




