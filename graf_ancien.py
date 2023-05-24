from tkinter import *
from tkinter.filedialog import askopenfile,askdirectory
import os
import glob  
from Code_Python_Acier_P20.Function_ExtractData_txt import *
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
        file = askopenfile(mode ='r', filetypes =[('All files', '*.txt')]) #stocker le fichier en tant que variable
        file = file.name
        print(type(file))
        print(file)
        self.storage_input.append(file) #add data to storage for next computing
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
        

    def function_calcultemperature(self) :  
        #print(len(self.storage_input))
        for i in range(len(self.storage_input)) :
            print(self.storage_input[i])
            temperature = np.loadtxt( self.storage_input[i] , skiprows=1, max_rows=self.t_fin_filtre,  usecols=self.colonne_extraire )
            print(np.shape(temperature))
            print(temperature)
            [self.vt,self.T_vf]   = CalculTemperature(temperature,self.f,self.t_fin_filtre,self.fact,
                                            self.n_sortie,self.f_sortie,self.Avec_Offset_AxeY)
            self.storage_output.append([self.vt, self.T_vf])
            #print(T_vf)

    
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