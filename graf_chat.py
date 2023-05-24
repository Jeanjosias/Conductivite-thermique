from tkinter import *
from tkinter.filedialog import askopenfile,askdirectory
import os
import glob  
import numpy as np
#from Code_Python_Acier_P20.Function_ExtractData_txt import *
import pandas as pd
import chardet
import matplotlib as mpl
from matplotlib.pyplot import figure
#from Code_Python_Acier_P20.Lecture_Fichier_Temperature_AcierP20_18_01 import *

class TkProg(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_title("Test Application")
        
        #CONSTANTE
        self.f = 500              ## Frequence (en Hz) de l'acquisition des données
        self.t_fin = 15           ##temps final (en s) où l'on considère que les données ensuites ne sont pas à considérer
        self.f_sortie = 1        ##facteur de réduction de la taille du fichier de sortie (on récupère une valeur tous les f_sortie"
        self.largeur_graph = 12         ## Largeur (en cm) du graph enregistré
        self.hauteur_graph = 8          ## Hauteur (en cm) du graph enregistré
        self.Avec_Offset_AxeY = 1          ## Si on veut appliquer un offset pour superposer les graphes au début: mettre 1 sinon 0 
        self.fact = 1000000                          #A ne pas toucher a priori
        self.t_fin_filtre = self.t_fin*self.f                  #A ne pas toucher a priori 
        self.n_sortie = int(self.t_fin_filtre/self.f_sortie)     #A ne pas toucher a priori 
        self.colonne_extraire = 0               # numéro de la colonne à extraire (0 -> première colonne du fichier txt)
    
        #personaliser fenetre
        self.title("My app")
        self.geometry("1080x720")
        self.config(bg='#41B77F')
        
        #créer Frame
        self.frame = Frame(self, bg='#41B77F')
        
        self.frame11 = Frame(self.frame, bg='#41B77F')
        #variables
        self.storage_input = []   
        self.storage_output = [] 
        self.temp_moyenne = []
        self.storage_temp_moyenne = []
        self.nom_temperature_moyenne = []
        #commandes
        mon_menu = Menu(self)
        self.config(menu=mon_menu)
        
        
        aide = Menu(mon_menu, tearoff=0)
        aide.add_command(label="Aide", command= self.aide)
        
        sortir = Menu(mon_menu, tearoff=0)
        sortir.add_command(label="Sortir", command= self.destroy)
        
        
        mon_menu.add_cascade(label="aide", menu=aide)
        mon_menu.add_cascade(label="sortir", menu=sortir)
        
        label_title = Label(self.frame11, text="Bienvenue sur l'application", font=("Courrier", 40), bg='#41B77F', fg="white")
        label_title.pack()
        
        btn = Button(self.frame11, text ='Ouvrir', command = self.open_file)
        btn.pack()

        valide_calcul = Button(self.frame11, text='Calcul', command= self.normalise)
        valide_calcul.pack()
        
        graph = Button(self.frame11, text='Afficher les graphs', command= self.plot)
        graph.pack()
        
        
        valide_entree = Button(self.frame11, text="Affichez temperature moyenne", command= self.temp_moyen)
        valide_entree.pack()
        
        #nom du fichier a sauvegarder
        self.ajout_save = StringVar()
        entree = Entry(self.frame11, textvariable=self.ajout_save)
        entree.pack()
        
        #ajout bouton
        label_1 = Label(self.frame11, text="Entrez le nom du fichier à sauvegarder", font=("Courrier", 16), bg='#41B77F', fg="white")
        label_1.pack()
        valide_entree = Button(self.frame11, text='Validez', command= self.save_filetxt)
        valide_entree.pack()
        
        reset = Button(self.frame11, text='Nettoyer', command= self.clean)
        reset.pack()
        
        self.frame11.pack(expand=YES)
        
        self.frame12 = Frame(self.frame, bg='#41B77F')
        temperature_moyenne = Button(self.frame12, text='Afficher toutes les courbes moyennes', command= self.plot_temperature_moyenne)
        temperature_moyenne.pack()
        
        self.frame12.pack(expand=YES, side= BOTTOM)
        
        self.frame.pack(expand=YES, side=RIGHT)
        
        self.frame2 = Frame(self, width =600, height =600, bg='#41B77F')
 
        
        photo = PhotoImage(file='image\img1.png')
        image = Label(self.frame2, image=photo)
        image.pack()
        
        self.frame2.pack(expand=YES, side=LEFT)
        
    #Fonctions
    
    def aide(self) : 
        file = open('help.txt', 'r')
        #print("ok")
        file.read()
        
    def open_file(self):
        #file = askopenfile(mode ='r', filetypes =[('All files', '*.xlsx')]) #stocker 
        # le chemin du fichier en tant que variable
        file = askopenfile(mode ='r', filetypes =[('All files', '*.txt')])
        print(type(file))
        print(file)
        #Temperature = np.array(df)
        #file = np.array(file)
        self.storage_input.append(file.name) #add data to storage for next computing
        #if file is not None:
            #content = file.read()
            #print(content)
        #file = file.name #le chemin vers le fichier
    
    def clean(self) :
        self.storage_input = [] #reset the storage
        self.storage_output = []
        self.temp_moyenne = []
        
    #def get_file(self) :
        #dossier = glob.glob("*")
        #for i in range(len(dossier)) :
            #path = dossier[i] + '\\' + ajout.get()
            #if os.path.exists(path) == True :
                #print(path)
                #break
            #else :
                #print("no")
                
    ####Calcul la derivée seconde discrete
    def derive_second (self, x, f) :
        derive_second_liste = []
        for i in range(1, len(f)-1) :
            derive_second_values = (f[i+1]+f[i-1]-2*f[i])/(x[i+1]-x[i-1])
            derive_second_liste.append(derive_second_values)
        return derive_second_liste


    ####moyenne mobile pour le debruitage de la serie (lissage)
    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w


    def normalise(self) :
        #data_output = []
        for j in range(len(self.storage_input)) :
            """
            with open(self.storage_input[j], 'rb') as f:
                result = chardet.detect(f.read())
                encodage = result['encoding']
            
            df = pd.read_csv(self.storage_input[j], encoding=encodage, delimiter='\t')
            """    
            df = pd.read_csv(self.storage_input[j], encoding='ISO-8859-9', delimiter='\t')
            
            shape = np.shape(df)
            
            """
            for i in range(shape[1]) :
                df.iloc[ :, i] = df.iloc[ :, i].str.replace(',', '.')
            """
            df = df.replace(',', '.', regex=True)
        
            df = df.astype(float)
            #df.to_excel('fichier.xlsx', index=False)
            #df = pd.read_csv(self.storage_input[j], delimiter='\t')
            list_temperature = np.array(df)
            shape = np.shape(list_temperature)

            time = np.zeros(shape[0])
            for j in range(1, shape[0]) : 
                time[j] = time[j-1] + 1/self.f
                
            list_temperature = np.c_[time, list_temperature]

            k = len(list_temperature)//10
            #for i in range(1 , shape[1]) :
            for i in range(1 , 2) :
                
                temperature = list_temperature[:,i]
                #time = time[0 : len(temperature)]
                temperature_liss = self.moving_average(temperature, k)
                time_liss = time[:len(temperature_liss)]
                derive_temp_liss = self.derive_second(time_liss, temperature_liss)
                
                #indice_inflexion = np.argmax(derive_temp_liss)
                T = True
                regu = 2*self.f
                while T :
                    indice_inflexion = np.argmax(derive_temp_liss)

                    if temperature[indice_inflexion] - 10 >= temperature[indice_inflexion+regu] :
                        T = False
                    else :
                        derive_temp_liss[indice_inflexion] = 0

                debut = 3
                fin = 15
                output = temperature[indice_inflexion+1-debut*self.f : indice_inflexion+1+fin*self.f]

                time_output = np.ones(len(output))
                time_output[debut*self.f] = 0
                time_output[debut*self.f : ] = np.linspace(0, fin, len(time_output[debut*self.f : ]))
                time_output[: debut*self.f] = np.linspace(-debut, 0, len(time_output[ : debut*self.f]))
                
                self.storage_output.append([time_output, output])
                #print(time_output)
                #data_len.append(len(output))
            
                
            #min_len = min(data_len)    q
            #print(min_len)
            #for i in range(len(data_output)) :
            #    self.storage_output[0][i] = self.storage_output[0][i][:min_len]
            #    self.storage_output[1][i] = self.storage_output[1][i][:min_len]
                
            
    """       

    def function_calcultemperature(self) :
        #print(len(self.storage_input))
        self.normalise()
        for i in range(len(self.storage_input)) :
            path = 'post_'+ str(i) +'txt'
            file = open(path, mode ='r') #stocker le chzmin du fichier en tant que variable
            temperature = np.loadtxt( file , skiprows=1, max_rows=self.t_fin_filtre,  usecols=self.colonne_extraire )
            #temperature = self.storage_input[i][0]
            [self.vt,self.T_vf]   = CalculTemperature(temperature,self.f,self.t_fin_filtre,self.fact,
                                            self.n_sortie,self.f_sortie,self.Avec_Offset_AxeY)
            self.storage_output.append([self.vt, self.T_vf])
            #print(T_vf)
  
    """       

    def plot(self) :
        plt.rc('font', size=8)

        fig, ax = plt.subplots()
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Temperature [°C]")
        ax.grid(True,linestyle='--')
        colour = ['b-', 'r-', 'g-', 'c-', 'm-', 'y-', 'k-',
                  'b--', 'r--', 'g--', 'c--', 'm--', 'y--', 'k--',
                  'b.', 'r.', 'g.']
        #[self.vt,self.T_vf] = self.storage_output
        for i in range(len(self.storage_output)) :
            ax.plot(self.storage_output[i][0], self.storage_output[i][1],colour[i],label= "Fichier" + str(i+1))

        plt.legend(loc='upper right') #,labelcolor='linecolor')

        fig.set_size_inches(self.largeur_graph/2.54, self.hauteur_graph/2.54, forward=True)
        fig = plt.gcf()
        #fig.savefig(nom_fichier_sortie_png, dpi=300)
        plt.show()
        
        
        #Debut d'enregistrement du fichier
        #savewind = Tk()
        #saveframe = Frame(savewind, bg='#41B77F')
        #label_saveframe = Label(saveframe, text="quer pour entrer le nom et cliquez pour enregistrer", font=("Courrier", 40), bg='#41B77F', fg="white")
        #label_saveframe.pack()

    def temp_moyen(self) :
        self.temp_moyenne = np.zeros(len(self.storage_output[0][1]))
        liste_temp_moyenne = []
        moyenne = 0
        variance = 0
        for i in range(len(self.storage_output)) :
            value = self.storage_output[i][1][-1]
            moyenne = moyenne + value
        moyenne = moyenne/len(self.storage_output)
        
        for i in range(len(self.storage_output)) : 
            value = self.storage_output[i][1][-1]
            variance = (value-moyenne)**2 + variance
        variance = variance/len(self.storage_output)
        
        ecart_type = np.sqrt(variance)
        
        bande_acceptation = [moyenne-3*ecart_type, moyenne+3*ecart_type]
        
        for i in range(len(self.storage_output)) :
            value = self.storage_output[i][1][-1]
            if value > bande_acceptation[0] and value < bande_acceptation[1] :
                liste_temp_moyenne.append(self.storage_output[i][1])
                self.temp_moyenne = self.storage_output[i][1] + self.temp_moyenne
                #print(temp_moyenne)
        
        self.temp_moyenne = self.temp_moyenne/len(liste_temp_moyenne)
        
        time = self.storage_output[0][0]
        self.storage_temp_moyenne.append([time, self.temp_moyenne])
        #print(temp_moyenne)
        #print(time)
        plt.legend('Temperature moyenne')
        plt.xlabel("Time [s]")
        plt.ylabel("Temperature [°C]")
        plt.grid(True,linestyle='--')
        plt.plot(time, self.temp_moyenne)
        plt.show()    
                
        
    def plot_temperature_moyenne(self) :
        
        excel_temperature_moyenne = []
        for i in range(len(self.storage_temp_moyenne)) :
            excel_temperature_moyenne.append(self.storage_temp_moyenne[i][1])
        
        excel_temperature_moyenne = np.array(excel_temperature_moyenne)
        excel_temperature_moyenne = excel_temperature_moyenne.T
        excel_temperature_moyenne = np.c_[self.storage_temp_moyenne[0][0], excel_temperature_moyenne]
        
        excel_temperature_moyenne = pd.DataFrame(excel_temperature_moyenne, columns=['time'] + self.nom_temperature_moyenne)
        excel_temperature_moyenne.to_excel('Temperature moyenne.xlsx', index=False)

        #print('ok')
        
        plt.rc('font', size=8)
        fig, ax = plt.subplots()
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Temperature [°C]")
        ax.grid(True,linestyle='--')
        colour = ['b-', 'r-', 'g-', 'c-', 'm-', 'y-', 'k-',
                  'b--', 'r--', 'g--', 'c--', 'm--', 'y--', 'k--',
                  'b.', 'r.', 'g.']
        #[self.vt,self.T_vf] = self.storage_output
        for i in range(len(self.storage_temp_moyenne)) :
            ax.plot(self.storage_temp_moyenne[i][0], self.storage_temp_moyenne[i][1],colour[i],label= self.nom_temperature_moyenne[i])
        
        plt.legend(loc='upper right') #,labelcolor='linecolor')

        fig.set_size_inches(self.largeur_graph/2.54, self.hauteur_graph/2.54, forward=True)
        fig = plt.gcf()
        #fig.savefig(nom_fichier_sortie_png, dpi=300)
        plt.show()
        
    #def save_filetxt(self) :
        
    #    mat = []
    #    for i in range(len(self.storage_output)) :
    #        for j in range(len(self.storage_output[0])) :
    #            mat.append(self.storage_output[i][j])
        
    #    mat = np.array(mat)
    #    mat= mat.T
        
    #    np.savetxt(self.ajout_save.get() +'.txt',mat,fmt='%.5f')     
      

    def save_filetxt(self) :
        
        excel = pd.DataFrame(self.temp_moyenne, columns=['Temperature_moyenne'])
        #print(excel)
        #print(self.ajout_save.get())
        #print(type(self.ajout_save.get()))
        excel.to_excel(self.ajout_save.get() + '.xlsx', index=False)
        self.nom_temperature_moyenne.append(self.ajout_save.get())
        #np.save_excel(self.ajout_save.get() +'.txt',self.temp_moyenne,fmt='%.5f')  
        
#creer fenetre
if __name__ == '__main__':
    # app mainloop
    app = TkProg()
    app.mainloop()