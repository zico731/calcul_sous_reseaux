#!/usr/bin/env python
# coding: utf-8

#--------------------------------------------------------------------------------
# A quoi sert le programme : calcul de sous réseaux suite au tp decoupage.py
# auteur :zico731
# date : 29 /10 /2021
#--------------------------------------------------------------------------------



from math import log,ceil

def cidr2mask(cidr):
    # calcul cidr =23 --> octet1=8bits, octet2=8bits, octet=3=7bits, oct4=0 --> 255.255.254.0
    
    oct=list("0000")
   
    oct_entier = cidr//8
    reste =cidr%8
    mask="8"*oct_entier+str(reste)
    suffixe_zero=4 - len(mask)
    mask=mask+"0"*suffixe_zero
    mask=list(mask)
    for i in range(4):
        oct[i]= str(256 - (2**(8-int(mask[i]))))
        
    return ".".join(oct)

    

adresse_ip_cidr = input("Entre l'adresse réseaux (exemple: 10.0.0.0/8) : ")
nb_SR = int(input ("Entre le nombre de sous-réseaux souhaité : "))
adresse_ip = adresse_ip_cidr.split("/")[0]
masque = int(adresse_ip_cidr.split("/")[1])
1
chaine_ip=""



# calcule de l'ipv4 en binaire
liste_octet= adresse_ip.split(".")
for octet in liste_octet:
    oct=bin(int(octet))[2:]
    oct=str("0")*(8-len(oct))+oct# on complète avec des 0 en préfixe
    chaine_ip += oct
    
print(f"\nL'adresse réseau {adresse_ip} peut s'ecrire : {chaine_ip[0:8]}.{chaine_ip[8:16]}.{chaine_ip[16:24]}.{chaine_ip[24:32]}")

 


# calcul du nombre de bit pour le sous réseaux
nb_bit_SR=ceil(log(nb_SR,2))
print(f"\nPour faire {nb_SR} sous-réseaux il faut donc réserver {nb_bit_SR} bits",end=" ") 

# affichage representative avec R, S et H
print("donc l'adresse réseaux est sous la forme de :",end=" ")

modele_IP="R"*masque+"S"*nb_bit_SR+"H"*(32-masque-nb_bit_SR)

print(f"{modele_IP[0:8]}.{modele_IP[8:16]}.{modele_IP[16:24]}.{modele_IP[24:32]}\n")


# cacul du masque CIDR
print(f"Le nouveau masque au format CIDR est : /{masque + nb_bit_SR}")

# calcul du masque en ecriture décimale pointee
print(f"Soit un masque en écriture décimale pointée : {cidr2mask(masque + nb_bit_SR)} ")



# calcul de l'adresse du pc cherché au nieme rang en binaire
res2bin=chaine_ip[0:masque]

nieme_hote = input("Indique le ième hote souhaité : ")
nieme_SR = input("Indique le ième sous-réseau souhaité : ")

nieme_SR_bin = str("0")*(nb_bit_SR-len(bin(int(nieme_SR)-1)[2:]))+bin(int(nieme_SR)-1)[2:]
nieme_hote_bin = str("0")*((32-masque-nb_bit_SR)-len(bin(int(nieme_hote))[2:])) + bin(int(nieme_hote))[2:]

# affichage du calcul de l'adresse du pc cherché au nieme rang en binaire

adresse_cherchee_bin = res2bin+nieme_SR_bin+nieme_hote_bin
print("")
print(f"Le hote recherché a pour IP binaire :{adresse_cherchee_bin[0:8]}.{adresse_cherchee_bin[8:16]}.{adresse_cherchee_bin[16:24]}.{adresse_cherchee_bin[24:32]}")

#conversion en ipv4
adresse_ip_cherche=str(int(adresse_cherchee_bin[0:8],2))+"."+                    str(int(adresse_cherchee_bin[8:16],2))+"."+                    str(int(adresse_cherchee_bin[16:24],2))+"."+                    str(int(adresse_cherchee_bin[24:32],2))
print("Soit en IPv4: " + adresse_ip_cherche)
input("")
