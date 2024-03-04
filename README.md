# GravitSim

![GravitSim_Logo](https://media.discordapp.net/attachments/1118301544765456455/1138277972583927818/logo3.png?ex=65efab78&is=65dd3678&hm=e8141d43844f431bc76fd0c2232187563b7f7cbb7a6bfc186b8fa15d5afcbb4e&=&format=webp&quality=lossless&width=280&height=280)

## Sur GravitSim
GravitSim est une application qui simule des intéractions gravitationelles dans un espace 2D, tout en permettant l'utilisateur d'éditer l'environnement et les grandeurs physiques. L'application permet aussi de visualiser les trajectoires et les futures collisions des corps.

## Fonctionnalités
### Interface d'édition
L'interface d'édition a été faite avec le module Tkinter.

Quand ouverte, l'interface d'édition nous permet de créer des corps et de configurer leurs grandeurs physiques.

Pour créer un corps, suffit appuyer `Ajouter corps`, pour l'enlever appuyer `Enlever corps`

Quand un corps est selectonné dans la boîte combo, ses paramètres comme leur positionm, vitesse (momentum sous forme vectorielle), masse, nom, couleur sont configurables.

Quand le corps est configuré, appuyer le boutton vert actualiser qui sauvegarde les paramètres du corps. 

L'interface edition permet de sauvegarder dans `Sauvegarder preset` la configuration planétaire actuelle dans un preset ou d'ouvrir dans `Charger preset` des presets déjá préparées précédemment qui incluent des situations simples comme des situations très spécifiques.

Les trajectoires des corps peuvent être afichées avec `Montrer/Cacher trajectoires` et manuellement actualisées avec (`Actualiser trajectoires`). Le nombre d'étapes calculées sont configurées dans `Nb. d'étapes`, et le corps selectionné peut être pris comme référence planétaire par le bouton `Utiliser réf`. ATTENTION! Le calcul et affichache des trajectoires peut être très computationellement couteux, attention lors de montrer les trajectoires dans quelques presets comme `DebutSystemeSolaire`

### Simulation
En haut à droite est la languette simulation où la vitesse des pas peut être configurée (Il faut appuyer `Actualiser simulation` pour actualiser la vitesse des pas) et la simulation peut être arrêtée ou reprise.

### Interface graphique
L'interface graphique a été faite avec le module Pygame.

Quand ouverte elle nous permet de visualiser les corps présents dans l'espace crée et de visualiser leurs vecteurs vitesse, trajectoires et collisions (quand la languette édition est selectionnée).

On peut glisser la camera avec les flèches du clavier ou WASD, on peut zoomer avec la roue de la souris.

L'édition de quelques attributs comme la position et la vitesse d'un corps peut être altérée dans la fenêtre de l'interface graphique avec la souris: On peut bouger le corps en le clicant et bougeant la souris, ou modifier sa vitesse en clicant la flèche du corps et la changeant.

![Démonstration édition](https://cdn.discordapp.com/attachments/1193679938461638656/1207426813903765574/Animation2144.gif?ex=65f20fd9&is=65df9ad9&hm=761a51a743a8845c55f3f2ed9ad7bc22ce3def8661d30ec4ec2e8321b872f18b&)
