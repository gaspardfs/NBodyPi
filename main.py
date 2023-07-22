import Jeu
import Interface
import multiprocessing


if __name__ == "__main__":
    #Cree les varaibles valeur
    variable1 = multiprocessing.Value("i", 0)
    
    #Mets les arguments en connexion (il faut avoir une , a la fin)
    arguments = (variable1,)

    #Cree les process 
    ProcessInterface = multiprocessing.Process(target=Interface.Interface, args=arguments)
    ProcessJeu = multiprocessing.Process(target=Jeu.Jeu, args=arguments)

    ProcessInterface.start()
    ProcessJeu.start()