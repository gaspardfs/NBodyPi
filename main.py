import Jeu
import Interface
import multiprocessing
 
if __name__ == "__main__":

    queue = multiprocessing.Queue()
    
    #Mets les arguments en connexion (il faut avoir une , a la fin)
    arguments = (queue,)

    #Cree les process 
    ProcessInterface = multiprocessing.Process(target=Interface.Interface, args=arguments)
    ProcessJeu = multiprocessing.Process(target=Jeu.Jeu, args=arguments)

    ProcessInterface.start()
    ProcessJeu.start()