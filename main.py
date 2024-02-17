import Jeu
import Interface
import multiprocessing
 
if __name__ == "__main__":

    queuePourInterface = multiprocessing.Queue()
    queuePourJeu = multiprocessing.Queue()

    
    #Mets les arguments en connexion (il faut avoir une , a la fin)
    arguments = (queuePourInterface, queuePourJeu)

    #Cree les process 
    ProcesInterface = multiprocessing.Process(target=Interface.Interface, args=arguments)
    ProcesJeu = multiprocessing.Process(target=Jeu.Jeu, args=arguments)

    ProcesInterface.start()
    ProcesJeu.start()

    while True:
        if not ProcesInterface.is_alive() or not ProcesJeu.is_alive():
            ProcesJeu.kill()
            ProcesInterface.kill()
            exit(1)