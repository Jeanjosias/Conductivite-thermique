from tkinter import *
from tkinter.filedialog import askopenfile,askdirectory
import os
import glob  
from Code_Python_Acier_P20.Function_ExtractData_txt import *
import pandas as pd
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
        
        #variables
        self.storage_input = []   
        self.storage_output = [] 
        
        #commandes
        mon_menu = Menu(self)
        self.config(menu=mon_menu)
        
        
        aide = Menu(mon_menu, tearoff=0)
        aide.add_command(label="aide", command= self.aide)
        
        sortir = Menu(mon_menu, tearoff=0)
        sortir.add_command(label="sortir", command= self.destroy)
        
        
        mon_menu.add_cascade(label="aide", menu=aide)
        mon_menu.add_cascade(label="sortir", menu=sortir)
        
        label_title = Label(self.frame, text="bienvenue sur l'application", font=("Courrier", 40), bg='#41B77F', fg="white")
        label_title.pack()
        

        #ajouter fichier
        #ajout = StringVar()
        #entree = Entry(self.frame, textvariable=ajout)
        #entree.pack()
        
        
        #ajout bouton
        #valide_entree = Button(frame, text='validez', command=get_file)
        #valide_entree.pack()

        btn = Button(self.frame, text ='Open', command = self.open_file)
        btn.pack()

        valide_calcul = Button(self.frame, text='calcul', command= self.function_calcultemperature)
        valide_calcul.pack()
        
        graph = Button(self.frame, text='afficher les graphs', command= self.plot)
        graph.pack()
        
        reset = Button(self.frame, text='nettoyer', command= self.clean)
        reset.pack()

        #nom du fichier a sauvegarder
        self.ajout_save = StringVar()
        entree = Entry(self.frame, textvariable=self.ajout_save)
        entree.pack()
        
        #ajout bouton
        label_1 = Label(self.frame, text="entrez le nom du fichier à save", font=("Courrier", 20), bg='#41B77F', fg="white")
        label_1.pack()
        valide_entree = Button(self.frame, text='validez', command= self.save_filetxt)
        valide_entree.pack()
        
        self.frame.pack(expand=YES)
        
        
    #Fonctions
    
    def aide(self) : 
        file = open('help.txt', 'r')
        print("ok")
        file.read()
        
    def open_file(self):
        file = askopenfile(mode ='r', filetypes =[('All files', '*.xlsx')]) #stocker le chzmin du fichier en tant que variable
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
            df = pd.read_excel(self.storage_input[j])
            list_temperature = np.array(df)
            shape = np.shape(list_temperature)
            #print(type(list_temperature))
            #print(shape)
            data_output = []
            data_len = []
            time = list_temperature[:,0]
            #shape = np.shape(list_temperature)
            #print(type(list_temperature))
            #print(shape)
            k = 5
            for i in range(1 , shape[1]) :
                
                temperature = list_temperature[:,i]
                temperature_liss = self.moving_average(temperature, k)
                time_liss = time[:len(temperature_liss)]
                derive_temp_liss = self.derive_second(time_liss, temperature_liss)
                
                indice_inflexion = derive_temp_liss.index(min(derive_temp_liss))
                #point_inflexion = time[indice_inflexion]
                
                output = temperature[indice_inflexion-6*self.f : indice_inflexion+15*self.f]
                time_output = np.ones(len(output))
                #time_output[indice_inflexion] = 0
                time_output[indice_inflexion : ] = np.linspace(0, len(time_output[indice_inflexion : ]), 1/self.f)
                time_output[: indice_inflexion] = np.linspace(-len(time_output[ : indice_inflexion], 0), 1/self.f)

                print(np.shape(output))
                data_output.append(output)
                data_len.append(len(output))
            
                
            min_len = min(data_len)    
            print(min_len)
            for i in range(len(data_output)) :
                data_output[i] = data_output[i][:min_len]
                    
            data_output = np.array(data_output) 
            #print(np.shape(data_output))
            data_output = data_output.T   
            print(np.shape(data_output))
            np.savetxt('post_'+ str(j) +'.txt',data_output,fmt='%.5f')
            #self.storage_input[j] = data_output
            
    """       

    def function_calcultemperature(self) :
        #print(len(self.storage_input))
        self.normalise()
        for i in range(len(self.storage_input)) :
<<<<<<< HEAD
            path = 'post_'+ str(i) +'txt'
            file = open(path, mode ='r') #stocker le chzmin du fichier en tant que variable
            temperature = np.loadtxt( file , skiprows=1, max_rows=self.t_fin_filtre,  usecols=self.colonne_extraire )
            #temperature = self.storage_input[i][0]
=======
            temperature = np.loadtxt( self.storage_input[i] , skiprows=1, max_rows=self.t_fin_filtre,  usecols=self.colonne_extraire )
            print(np.shape(temperature))
>>>>>>> af5fa3bd96009070612d0df8e78057aee8219307
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
        colour = ['b-', 'r-', 'g-', 'o-', 'w-']
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


    def save_filetxt(self) :
        
        mat = []
        for i in range(len(self.storage_output)) :
            for j in range(len(self.storage_output[0])) :
                mat.append(self.storage_output[i][j])
        
        mat = np.array(mat)
        mat= mat.T
        
        np.savetxt(self.ajout_save.get() +'.txt',mat,fmt='%.5f')      
      

#creer fenetre
if __name__ == '__main__':
    # app mainloop
    app = TkProg()
    app.mainloop()
