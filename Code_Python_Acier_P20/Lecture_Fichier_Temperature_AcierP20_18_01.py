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

from Code_Python_Revetement_ZrO2_40_microns.Function_ExtractData_txt import CalculTemperature

plt.close("all")







"""________________________________________________________________________"""
"""       DEBUT PARAMETRES DU MODELE      """
f = 500              ## Frequence (en Hz) de l'acquisition des données
t_fin = 15           ##temps final (en s) où l'on considère que les données ensuites ne sont pas à considérer
f_sortie = 1        ##facteur de réduction de la taille du fichier de sortie (on récupère une valeur tous les f_sortie"

largeur_graph = 12         ## Largeur (en cm) du graph enregistré
hauteur_graph = 8          ## Hauteur (en cm) du graph enregistré

Avec_Offset_AxeY = 1          ## Si on veut appliquer un offset pour superposer les graphes au début: mettre 1 sinon 0 

fichier1 = 'AcierP20-repet1-traite.txt' #20221004_100905_Surveillance_RMS.txt #
fichier2 = 'AcierP20-repet2-traite.txt'
##fichier3 = '20221019_121806_Surveillance_RMS_15-11.txt'
##fichier4 = '20221019_123100_Surveillance_RMS_15-11.txt'
##fichier5 = '20221019_103854_Surveillance_RMS_14-11.txt'
##fichier6 = '20221019_105022_Surveillance_RMS_14-11.txt'
##fichier7 = '20221019_110524_Surveillance_RMS_14-11.txt'
##fichier8 = '20221019_111730_Surveillance_RMS_14-11.txt'
##fichier9 = '20221005_132117_Surveillance_RMS_40.txt'
##fichier10 = '20221005_134849_Surveillance_RMS_40.txt'
##fichier11 = '20221005_141254_Surveillance_RMS_40.txt'
##fichier12 = '20221005_143707_Surveillance_RMS.txt' 
##fichier13 = '20221005_144912_Surveillance_RMS.txt'
##fichier14 = '20221005_152309_Surveillance_RMS.txt'
##fichier15 = '20221005_154117_Surveillance_RMS.txt'
##fichier16 = '20221005_155456_Surveillance_RMS.txt'
##fichier17 = '20221005_160725_Surveillance_RMS.txt'
##fichier18 = '20221005_163108_Surveillance_RMS.txt'
##fichier19 = '20221005_164450_Surveillance_RMS.txt'


nom_fichier_sortie_png = 'AcierP20.png'
nom_fichier_sortie_txt = 'Temperature_filtre'

##  TRES IMPORTANT: IL FAUT QUE LE FICHIER .TXT comporte "." plutôt que "," 

colonne_extraire = 0               # numéro de la colonne à extraire (0 -> première colonne du fichier txt)

"""       FIN PARAMETRES DU MODELE      """
"""________________________________________________________________________"""




 
fact = 1000000                          #A ne pas toucher a priori
t_fin_filtre = t_fin*f                  #A ne pas toucher a priori 
n_sortie=int(t_fin_filtre/f_sortie)     #A ne pas toucher a priori 


# STEP 1 Lecture du fichier et extraction de la colonne numéro  colonne_extraire
Temperature  = np.loadtxt( fichier1 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
Temperature2 = np.loadtxt( fichier2 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature3 = np.loadtxt( fichier3 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature4 = np.loadtxt( fichier4 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature5 = np.loadtxt( fichier5 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature6 = np.loadtxt( fichier6 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature7 = np.loadtxt( fichier7 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature8 = np.loadtxt( fichier8 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature9 = np.loadtxt( fichier9 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature10 = np.loadtxt( fichier10 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature11 = np.loadtxt( fichier11 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature12 = np.loadtxt( fichier12 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature13 = np.loadtxt( fichier13 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature14 = np.loadtxt( fichier14 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature15 = np.loadtxt( fichier15 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature16 = np.loadtxt( fichier16 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature17 = np.loadtxt( fichier17 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature18 = np.loadtxt( fichier18 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )
##Temperature19 = np.loadtxt( fichier19 , skiprows=1, max_rows=t_fin_filtre,  usecols=colonne_extraire )

# STEP 2 Application de la fonction CalculTemperature pour transformer les données
[vt,T_vf]   = CalculTemperature(Temperature,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
[vt2,T_vf2] = CalculTemperature(Temperature2 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt3,T_vf3] = CalculTemperature(Temperature3 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt4,T_vf4] = CalculTemperature(Temperature4 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt5,T_vf5] = CalculTemperature(Temperature5 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt6,T_vf6] = CalculTemperature(Temperature6 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt7,T_vf7] = CalculTemperature(Temperature7 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt8,T_vf8] = CalculTemperature(Temperature8 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt9,T_vf9] = CalculTemperature(Temperature9 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt10,T_vf10] = CalculTemperature(Temperature10 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt11,T_vf11] = CalculTemperature(Temperature11 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt12,T_vf12] = CalculTemperature(Temperature12 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt13,T_vf13] = CalculTemperature(Temperature13 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt14,T_vf14] = CalculTemperature(Temperature14 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt15,T_vf15] = CalculTemperature(Temperature15 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt16,T_vf16] = CalculTemperature(Temperature16 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt17,T_vf17] = CalculTemperature(Temperature17 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt18,T_vf18] = CalculTemperature(Temperature18 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)
##[vt19,T_vf19] = CalculTemperature(Temperature19 ,f,t_fin_filtre,fact,n_sortie,f_sortie,Avec_Offset_AxeY)

# STEP 3 Affichage
plt.rc('font', size=8)

fig, ax = plt.subplots()
ax.set_xlabel("Time [s]")
ax.set_ylabel("Temperature [°C]")
ax.grid(True,linestyle='--')

ax.plot(vt,T_vf,'b-',label='Fichier 1')
ax.plot(vt2,T_vf2,'r-',label='Fichier 2')
##ax.plot(vt3,T_vf3,'g-',label='Fichier 3')
##ax.plot(vt4,T_vf4,'k-',label='Fichier 4')
##ax.plot(vt5,T_vf5,'m-',label='Fichier 5')
##ax.plot(vt6,T_vf6,'c-',label='Fichier 6')
##ax.plot(vt7,T_vf7,'y-',label='Fichier 7')
##ax.plot(vt8,T_vf8,'b', linestyle=(0, (5, 10)),label='Fichier 8')
##ax.plot(vt9,T_vf9,'r', linestyle=(0, (5, 10)),label='Fichier 9')
##ax.plot(vt10,T_vf10,'g', linestyle=(0, (5, 10)),label='Fichier 10')
##ax.plot(vt11,T_vf11,'k', linestyle=(0, (5, 10)),label='Fichier 11')
##ax.plot(vt12,T_vf12,'m', linestyle=(0, (5, 10)),label='Fichier 12')
##ax.plot(vt13,T_vf13,'c', linestyle=(0, (5, 10)),label='Fichier 13')
##ax.plot(vt14,T_vf14,'y', linestyle=(0, (5, 10)),label='Fichier 14')
##ax.plot(vt15,T_vf15,'b', linestyle=(0, (1, 10)),label='Fichier 15')
##ax.plot(vt16,T_vf16,'r', linestyle=(0, (1, 10)),label='Fichier 16')
##ax.plot(vt17,T_vf17,'g', linestyle=(0, (1, 10)),label='Fichier 17')
##ax.plot(vt18,T_vf18,'k', linestyle=(0, (1, 10)),label='Fichier 18')
##ax.plot(vt19,T_vf19,'m', linestyle=(0, (1, 10)),label='Fichier 19')


plt.legend(loc='upper right') #,labelcolor='linecolor')


fig.set_size_inches(largeur_graph/2.54, hauteur_graph/2.54, forward=True)
fig = plt.gcf()
fig.savefig(nom_fichier_sortie_png, dpi=300)
plt.show()



# STEP 4 Sauvegarde
#fig.savefig(nom_fichier_sortie_png, dpi=300)

mat = np.array([vt,T_vf,vt2,T_vf2])
mat= mat.T

np.savetxt(nom_fichier_sortie_txt +'.txt',mat,fmt='%.5f')




