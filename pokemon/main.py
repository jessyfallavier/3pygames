class NoeudGraphe:
    """Objet représentant un noeud du graphe."""
    def __init__(self, valeurs):
        """Méthode - Attribue les valeurs d'un noeud -- Ne retourne rien

        Paramètres nommés :
        valeurs -- valeurs du noeud (dictionnaire)
        """

        #Attribution des caractéristiques
        #-Mode, Histoire et Choix
        self.mode = valeurs["mode"]
        self.histoire = valeurs["histoire"]
        self.choix = valeurs["choix"]

        #-Multimédia
        self.image = valeurs["image"]
        self.bruitage = valeurs["bruitage"]
        self.musique = valeurs["musique"]

class MoteurJeu:
    """Objet gérant les fonctionnalitées de la partie."""
    def __init__(self):
        """Méthode - Commande le lancement d'une partie -- Ne retourne rien

        Paramètres nommés :
            Aucun

        """

        self.start()

    def start(self):
        """Méthode - Gère le lancement de la partie -- Ne retourne rien

        Paramètres nommés :
            Aucun

        """

        import json
        
        #Récuperer le jeu de données
        self.adj = []

        #Ouvrir le fichier de données et récupérer celles-ci
        with open('res/data/data.json', encoding='utf8') as fichier:
            data = json.load(fichier)

        #Ajouter une ligne d'adjacence pour chaque noeud
        for noeud in data:
            self.adj.append([NoeudGraphe(noeud)] + noeud["adj"])

        #Définition du numéro de noeud actuel et des phrases à afficher
        self.numero = 0
        self.phrases = ["", ""]

        #Lancement de la boucle principale
        self.mainLoop()
    
    def jouerBruitage(self, nom):
        """Méthode - Joue un bruitage -- Ne retourne rien

        Paramètres nommés :
        nom -- nom du fichier bruitage (string)

        """

        import pygame

        #Jouer le bruitage
        pygame.mixer.Sound("res/music/" + nom).play()
    
    def deplacement(self, choix):
        """Méthode - Permet de se déplacer dnas le graphe -- Ne retourne rien

        Paramètres nommés :
        choix -- réponse du joueur concernant la direction (entier)

        """

        #Se déplacer
        self.numero = self.adj[self.numero][choix]

        #Si le déplacement est de quitter le jeu, le quitter
        if self.numero == -1:
            self.continuer = False
        #Si le jeu recommence, remettre à néant le score
        elif self.numero == 0:
            self.score = None

    def verifChoix(self, choix):
        """Méthode - Vérifie si un déplacement est envisageable -- Retourne l'entier du choix ou False si le choix est impossible

        Paramètres nommés :
        choix -- réponse du joueur concernant la direction (entier)

        """

        #Si le choix est dans compris dans le nombre de choix disponibles
        if choix in range(len(self.adj[self.numero])):
            return choix
        else:
            return False

    def verifSouris(self):
        """Méthode - Vérifie si l'endroit de la souris correspond à un choix -- Retourne l'entier du choix ou False si le choix n'en est pas un ou si le choix est impossible

        Paramètres nommés :
            Aucun

        """

        #Si 1ere colonne
        if self.cursorCoord[0] in range(10,460):
            #Si 1ere ligne
            if self.cursorCoord[1] in range(400, 520):
                return self.verifChoix(1)
            #Si 2eme ligne
            elif self.cursorCoord[1] in range(535, 655):
                return self.verifChoix(3)
        #Si 2eme colonne
        elif self.cursorCoord[0] in range(510, 960):
            #Si 1ere ligne
            if self.cursorCoord[1] in range(400, 520):
                return self.verifChoix(2)
            #Si 2eme ligne
            elif self.cursorCoord[1] in range(535, 655):
                return self.verifChoix(4)
        
        return False

    def jouerFond(self, nom):
        """Méthode - Joue une musique de fond -- Ne retourne rien

        Paramètres nommés :
        nom -- nom du fichier musique (string)

        """

        import pygame

        #Jouer la musique de fond
        pygame.mixer.music.load("res/music/" + nom)

        #Jouer la musique en boucle et mettre le son à 50%
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.5)

    def mainLoop(self):
        """Méthode - Boucle principale du jeu -- Ne retourne rien

        Paramètres nommés :
        Aucun

        """

        import pygame
        from time import time

        #Initialiser pygame et le module mixer de pygame à la fréquence 44100Hz
        pygame.mixer.init(frequency=44100)

        #Définition de la taille de l'écran et du titre de la fenètre
        self.screen = pygame.display.set_mode((1000,700))
        pygame.display.set_caption('Légendes Pokémon : Giratina')

        #Définition de l'icone du programme
        programIcon = pygame.image.load('res/image/pokeballLogo.png')
        pygame.display.set_icon(programIcon)

        #Mettre le curseur classique de la souris en invisible
        pygame.mouse.set_visible(False)
        
        #Initialiser pygame
        pygame.init()
        
        #Import des images
        self.cursorIcon = pygame.image.load('res/image/pokeballCurseur.png')
        self.imgDialogue = pygame.image.load("res/image/dialogue.png")
        self.police = pygame.font.Font("res/font/pkmndp.ttf", 35)
        self.policeBold = pygame.font.Font("res/font/pkmndpb.ttf", 35)

        #Définition du temps de départ et le score néant du début
        self.time = time()
        self.score = None

        #Lancer la boucle principale
        self.continuer = True
        while self.continuer:
            
            #- Jouer les sons
            #S'il y a un bruitage, le jouer
            if self.adj[self.numero][0].bruitage != "":
                self.jouerBruitage(self.adj[self.numero][0].bruitage)
                print("possin")

            #S'il y a une musique, la jouer
            if self.adj[self.numero][0].musique != "":
                self.jouerFond(self.adj[self.numero][0].musique)

            #Afficher l'histoire
            for n in range(len(self.adj[self.numero][0].histoire)):

                #Définer les phrases à afficher par deux et une-à-une
                if self.phrases[0] == "" and self.phrases[1] == "":
                    self.phrases[0] = self.adj[self.numero][0].histoire[n]
                elif self.phrases[0] != "" and self.phrases[1] == "":
                    self.phrases[1] = self.adj[self.numero][0].histoire[n]
                else:
                    self.phrases[0] = self.phrases[1]
                    self.phrases[1] = self.adj[self.numero][0].histoire[n]

                #Attendre le clic du joueur avant de poursuivre
                aClique = False
                while not aClique:
                    #Obtenir les coordonées de la souris
                    self.cursorCoord = pygame.mouse.get_pos()
                    
                    #Actualiser l'écran
                    self.afficher(0)

                    #Vérification des évènements
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            #L'utilisateur veux fermer le programme
                            self.continuer = False
                            aClique = True

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            #L'écran est cliqué
                            aClique = True

                #Jouer le bruitage de bump
                self.jouerBruitage("bump.ogg")

                #Si l'utilisateur veux fermer le programme, casser la boucle
                if self.continuer == False:
                    break
            
            #Si l'utilisateur veux fermer le programme, casser la boucle
            if self.continuer == False:
                break

            #Réanitinalisation des phrases à afficher
            self.phrases = ["", ""]
            
            #Boucle pour attendre que l'utilisateur clique sur un choix valide
            aClique = False
            while not aClique:
                
                #Obtenir les coordonées de la souris
                self.cursorCoord = pygame.mouse.get_pos()
                
                #Actualiser l'écran
                self.afficher(1)

                #Vérification des évènements
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #L'utilisateur veux fermer le programme
                        self.continuer = False
                        aClique = True
                            
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #L'écran est cliqué
                        
                        #Obtenir le numero de choix correspondant ou False s'il y en a pas
                        reponse = self.verifSouris()
                        if reponse:
                            #Le choix est valide, jouer le bruitage exclam
                            self.jouerBruitage("exclam.ogg")
                            aClique = True
                        else:
                            #Le choix est valide, jouer le bruitage bumb
                            self.jouerBruitage("bump.ogg")

            #Si l'utilisateur veux fermer le programme, casser la boucle
            if self.continuer == False:
                break

            #Se déplacer dans le graphe
            self.deplacement(reponse)
        
        #Quitter le programme
        pygame.quit()

    def afficher(self, etape):
        """Méthode - Actualise l'affichage de la fenêtre -- Ne retourne rien

        Paramètres nommés :
        etape -- représente le mode d'affichage à mettre en place (entier)

        """

        import pygame
        from time import time

        #Mettre un écran noir
        self.screen.fill((255,255,255))

        #Afficher l'image de fond du haut
        if self.adj[self.numero][0].image != "":
            self.screen.blit(pygame.image.load("res/image/" + self.adj[self.numero][0].image), (0, 0))

        #Mettre le fond vert du bas
        rectangle = pygame.Surface((1000, 300))
        pygame.draw.rect(rectangle, pygame.Color(223, 228, 234), rectangle.get_rect())
        self.screen.blit(rectangle, (0, 400))

        #Liste des couleurs d'affichage
        couleurs = [(45, 152, 218), (0, 0, 0), (247, 183, 49), (32, 191, 107), (235, 59, 90)]

        #Mode histoire OU mode choix
        if etape == 0:
            #Afficher la bulle histoire
            self.screen.blit(self.imgDialogue, (0, 400))

            #Afficher l'histoire
            for n in range(2):
                self.screen.blit(self.police.render(self.phrases[n],1,couleurs[self.adj[self.numero][0].mode]), (50, 475 + 100 * n))
        else:
            #Afficher les choix et les bulles de choix
            for n in range(2):
                for k in range(2):
                    #Calcul du numero du choix
                    numeroChoix = n * 2 + k

                    #Vérifie si la case est à afficher
                    if self.verifChoix(numeroChoix + 1):

                        #Si la case est survolée, la colorer et changer le curseur en Pokéball ouverte
                        if self.verifSouris() == numeroChoix + 1:
                            self.screen.blit(pygame.image.load("res/image/choixSelec.png"), (25 + 500 * k, 415 + 135 * n))
                            self.cursorIcon = pygame.image.load('res/image/pokeballCurseurOuverte.png')
                        else:
                            #Afficher la bulle colorée
                            self.screen.blit(pygame.image.load("res/image/choix"+ str(numeroChoix) +".png"), (25 + 500 * k, 415 + 135 * n))

                        #Afficher le texte choix
                        self.screen.blit(self.policeBold.render(self.adj[self.numero][0].choix[numeroChoix],1,(255,255,255)), (50 + 500 * k, 455 + 135 * n))

            
            #Vérification de s'il faut faire apparaitre le score
            multiplicateur = {2: 3, 3: 4, 4:1}
            if self.adj[self.numero][0].mode in multiplicateur.keys():
                #Si le score n'existe pas, le calculer
                if not self.score:
                    #Calcul du score : (250 - difference en secondes) * multiplicateur (1-défaire/3-victoire/+1-victoire parfaite)
                    self.score = int((180 - time() + self.time) * multiplicateur[self.adj[self.numero][0].mode])

                    #Mise en texte
                    if self.score <= 0:
                        #Si c'est un score faire mettre un :-(
                        self.score = "très faible ! :-("
                    elif self.score >= 180:
                        #Si est un très bon score mettre un ^_^
                        self.score = f"de : {self.score} ! ^_^"
                    elif self.adj[self.numero][0].mode == 4:
                        #Si c'est une défaite mettre un :/
                        self.score = f"de : {self.score} points ! :/"
                    else:
                        #Sinon mettre un ^^
                        self.score = f"de : {self.score} points ! ^^"

                #Afficher le score
                self.screen.blit(self.police.render(f"Votre score est {self.score}",1,couleurs[self.adj[self.numero][0].mode]), (150, 600))


        #Afficher le cursuer Pokéball et remettre à zero son image
        self.screen.blit(self.cursorIcon, self.cursorCoord)
        self.cursorIcon = pygame.image.load('res/image/pokeballCurseur.png')


        #Mise à jour de l'affichage
        pygame.display.update()

MoteurJeu()