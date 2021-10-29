#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Date 29/10/2017
Auteur Pol-Quentin Dupont
Version V.3
Thème du script : Exercice de découpage de sous-réseaux IPv4.
'''

from random import randint
from random import choice


def creation():
    """
    Création d'une adresse IP aléatoire

    Entrée: aucune
    Sorties :
        - masque_init : masque de sous réseau initial;
        - nbReseauAleatoire : nombre de sous réseaux choisi pour
          l'exercice.
        - une : premier octet de l'adresse IP
        - deux : deuxième octet de l'adresse IP
        - trois : troisième octet de l'adresse IP

    """

    # Choix aléatoire d'une adresse simple donc le quatrième octet
    # sera toujours 0
    une = randint(5, 240)
    deux = randint(0, 240)
    trois = randint(0, 250)

    # Choix d'un masque de sous réseau masque simplissime de type
    # "classe" pour ne pas rendre
    # l'exercice trop dur.
    masque_init = choice([8, 16, 24])

    # Division du réseau choisi en sous réseaux probablement
    # (et volontairement) inégaux mais relativement simple (<5000)
    if masque_init == 8:
        nbreseauxaleatoire = randint(2, 5000)
        deux = 0
        trois = 0
    elif masque_init == 16:
        nbreseauxaleatoire = randint(2, 2384)
        trois = 0
    else:
        nbreseauxaleatoire = randint(2, 64)

    return masque_init, nbreseauxaleatoire, une, deux, trois


def calculadresse(masque_init, nbreseaux, une, deux, trois):

    """
    Choix d'un hôte et d'un réseau au sein des sous-réseaux.

    Entrées:
        - masque_init: masque de sous réseau initial
        - nbreseaux : nombre de sous-réseaux choisis
        - une : premier octet de l'adresse IP initiale
        - deux : deuxième octet de l'adresse IP initiale
        - trois : troisième octet de l'adresse IP initiale
    Sorties:
        - cidr : nouveau masque de sous-réseau.
        - adresse : adresse IP attendue après découpage.
        - reseaurandom : sous-réseau aléatoire choisi parmi
          la liste des sous-réseaux utilisable.
        - randnet : rang de l'hôte dans la partie hostid

    """

    # Calcul du NetID et hostid
    tempn = 1
    while 2**tempn < nbreseaux:
        tempn += 1
    nbreseaux = int(2**tempn)
    cidr = masque_init+tempn
    hostid = 32-cidr
    # Choix d'un hôte pris au hasard parmi les hôtes possibles du
    # sous-réseau choisi
    randnet = randint(2, (2**hostid)-1)
    reseaurandom = randint(1, 2**(cidr-masque_init))

    # Calcul de l'adresse de l'hote choisi dans le sous-reseau en fonction
    # du nouveau masque
    reseaumoinsun = reseaurandom-1  # La première adresse est 0, pas 1.
    # Si masque initial /8
    if masque_init == 8:
        if tempn <= 8:
            new2 = ((reseaumoinsun*(2**(8-tempn)))+randnet//65536)
            new3 = (randnet % 65536)//256
            new4 = (randnet % 65536) % 256
        elif tempn > 8 and tempn <= 16:
            new2 = (reseaumoinsun//(2**(tempn-8)))
            new3 = ((reseaumoinsun % (2**(tempn-8))) * (2**(16-tempn))) +\
                   (randnet//256)
            new4 = randnet % 256
        else:
            new2 = reseaumoinsun//(2**(tempn-8))
            new3 = (reseaumoinsun % (2**(tempn-8)))//(2**(tempn-16))
            new4 = ((reseaumoinsun % (2**(tempn-16)))*(2**(24-tempn)))+randnet
    # Si masque initial /16
    if masque_init == 16:
        new2 = deux
        if tempn >= 8:
            new3 = ((reseaumoinsun//(2**(tempn-8)))+(randnet//256))
            new4 = (reseaumoinsun % (2**(tempn-8)) * (2**(16-tempn))) +\
                   (randnet % 256)
        else:
            new3 = ((reseaumoinsun*(2**(8-tempn)))+randnet//256)
            new4 = randnet % 256
    # Si masque initial /24
    if masque_init == 24:
        new2 = deux
        new3 = trois
        new4 = ((reseaumoinsun)*(2**(8-tempn)))+randnet

    adresse = str(une)+"."+str(new2)+"."+str(new3)+"."+str(new4)  # enfin!

    return cidr, adresse, reseaurandom, randnet


def transformdecimal(cidr):
    """
    Ecriture d'un masque de sous-réseau de la forme CIDR à la
    forme décimale pointée.

    Entrée
        - cidr : Masque sous la forme CIDR.
    Sortie
        - masque_dec : Masque sous la forme décimale pointée.

    """

    # Transformation du NetID en écriture décimale pointée
    nbmots = cidr
    masque1 = 0
    masque2 = 0
    masque3 = 0
    masque4 = 0
    if nbmots < 8:
        while nbmots > 0:
            masque1 += 2**(8-nbmots)
            nbmots -= 1
    elif nbmots >= 8 and nbmots < 16:
        masque1 = 255
        nbmots -= 8
        while nbmots > 0:
            masque2 += 2**(8-nbmots)
            nbmots -= 1
    elif nbmots >= 16 and nbmots < 24:
        masque1 = 255
        masque2 = 255
        nbmots -= 16
        while nbmots > 0:
            masque3 += 2**(8-nbmots)
            nbmots -= 1
    else:
        masque1 = 255
        masque2 = 255
        masque3 = 255
        nbmots -= 24
    while nbmots > 0:
        masque4 += 2**(8-nbmots)
        nbmots -= 1

    masque_dec = str(masque1) + "." + str(masque2) + "." + str(masque3) +\
        "." + str(masque4)
    return masque_dec


def main():

    """
    Programme principal
    """

    print("Salut!\nJe te propose un exercice pour calculer des adresses d'hôtes \
dans un sous-réseau.\n")

    # Boucle pour rejouer si on le souhaite à la fin du programme
    rejouer = 1
    while rejouer == 1:
        # Le rôle de ces variables est expliqué dans les fonctions.
        initial, nbreseauxaleatoire, une, deux, trois = creation()
        cidr, adresse, reseaurandom, randnet = \
            calculadresse(initial, nbreseauxaleatoire, une, deux, trois)
        masque = transformdecimal(cidr)

        # L'énnoncé de l'exercice:

        print("Tu disposes du réseau", str(une) + "." + str(deux) + "." +
              str(trois) + "." + str('0') + "/" + str(initial) +
              " et tu souhaites le découper en " + str(nbreseauxaleatoire) +
              " sous-réseaux identiques.\n")

        # L'exercice ne s'arrête qu'en cas de réussite :
        encore = 1
        while encore == 1:
            # Les questions qui vont bien
            # (cidr, masque en décimal, adresse réseau demandée)
            reponsecidr = str('')

            # On demande le masque au format CIDR (on exige un entier)
            while not isinstance(reponsecidr, int):
                try:
                    reponsecidr =\
                        int(input(
                            "Quel est le nouveau masque (format CIDR) : /"))
                except ValueError:
                    print("J'attends un entier stp")

            # On demande le masque au format décimal pointé
            reponsemasque = input("Ecris ce masque en écriture décimale " +
                                  "pointée (x.x.x.x): ")

            # On demande l'adresse de l'hôte recherché.
            # Petite variante d'affichage si on 'tombe' sur le premier réseau
            if reseaurandom == 1:
                print("Nous voulons connaître le", str(randnet) +
                      "ème hôte du premier sous-réseau (numéro 0).")
            else:
                # Demande pour n'importe quel autre sous réseau:
                print("Nous voulons connaître le", str(randnet) +
                      "ème hôte du", str(reseaurandom) + "ème sous-réseau " +
                      "(donc le sous-réseau numéro", reseaurandom-1,
                      "en partant de 0).")

            reponseadresse = input("Quelle est son adresse IP " +
                                   "(n'écris pas le masque)? :")

            # Comparaison des réponses avec celles attendues :
            if reponseadresse == adresse and reponsecidr == cidr and \
                    reponsemasque == masque:
                print("Bravo tu as réussis l'exercice, tu maîtrises " +
                      "les calculs de sous-réseaux!! :)")
                encore = 0
            else:
                print("Quelque chose ne va pas ... allez, " +
                      "un peu de concentration on recommence.\n")

        # On pourrait avoir affaire à un joueur maso qui veut rejouer :)
        ask = input("Veux-tu rejouer? (Y/N) : ")
        if ask in ["Y", "y", "o", "O"]:
            print("Cool, c'est reparti! :-)")
            rejouer = 1
        else:
            print("A bientôt!")
            input("Tape ENTRER pour quitter")
            rejouer = 0
        exit(1)


if __name__ == '__main__':
    main()
