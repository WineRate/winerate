"""Projet WineRate : Programme de scraping des pages du vignoble"""

# Operating System - recherche de fichiers
import os

# Importation de la bibliothèque de scraping BeautifulSoup
import requests
from bs4 import BeautifulSoup

def collecte_tableau(nom_vignoble,couleur_vin,rang_couleur_tableau,annee_millesime) :
    """Scraping d'un tableau de données déterminé par le rang_couleur_tableau"""

    # création de l'URL à scraper
    url = 'http://www.vin-vigne.com/millesimes/annee-'+str(annee_millesime)+'-vin-'+nom_vignoble+'.html'

    # se connecter à la page et obtenir le code source
    requete = requests.get(url)
    page_html = requete.content

    # initialisation de la chaine qui contiendra toutes les données de la page web
    chaine = ""

    # transformer la page HTML en beautifulSoup pour pouvoir la manipuler
    soupe = BeautifulSoup(page_html, "html5lib")
    
    #Vérification des variables en entrée, on ne traite pas au delà de 4ième tableaux 
    
    # stocker les donnees des vins obtenues par scraping
    data = []
    table = soupe.find_all('table', attrs={'class': 'points'})[rang_couleur_tableau]
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if cols :   # on élmine les premières lignes non utiles et vides du tableau
            data.append(cols)

    # accumulation des données de chaque ligne et colonne dans une chaîne de caractère
    max_rows=len(data)
    max_cols=5
    #print(max_rows)
    
    for count_rows in range(max_rows) :
        chaine = chaine + nom_vignoble.capitalize() +';'+str(annee_millesime)+';'+couleur_vin
        for count_cols in range(max_cols) :
            if data[count_rows][count_cols] :
                chaine=chaine+';'+data[count_rows][count_cols]
            else :
                chaine = chaine +';'                
        chaine = chaine +'\n'
    
    return chaine


def collecte_region_millesime(nom_vignoble,annee_millesime) :
    """Scraping de toute la page web d'une région pour un millesime donnée"""
    
    chaine=collecte_tableau(nom_vignoble,'Rouge',2,annee_millesime)
    chaine=chaine+collecte_tableau(nom_vignoble,'Blanc',3,annee_millesime)
    chaine=chaine+collecte_tableau(nom_vignoble,'Rosée',4,annee_millesime)
    return chaine


def collecte_global_region(nom_vignoble,annee_min,annee_max) :
    """Scraping pour une région d'une annee_min à une annee_max"""
        
    #Initialisation de la trame
    chaine_donnees=""
    
    #Initialisation du compteur avec la plage à parcourir
    compteur_annee=annee_max-annee_min+1
    
    for annee_millesime in range(compteur_annee) :        
        chaine_donnees=chaine_donnees+collecte_region_millesime(nom_vignoble,annee_min)
        annee_min+=1
    
    return chaine_donnees


def collecte_france(annee_min, annee_max) :
    """Scraping pour toute les régions viticoles de France"""

    # Liste des régions des vignobles
    region_viticole = ['alsace',
                      'beaujolais',
                      'bordeaux',
                      'bourgogne',
                      'champagne',
                      'cognac',
                      'jura',
                      'languedoc-roussillon',
                      'loire',
                      'lorraine',
                      'provence-corse',
                      'rhone',
                      'savoie-bugey',
                      'sud-ouest']

    #Initialisation des variables de la trame de donnée
    chaine_donnees='Region;Annee;Couleur;Appellation;Note;Label_fr;Label_eu;Nb_vins'+'\n'
 
    # Scraping des éléments sur toutes les régions viticoles de France
    for region in region_viticole :
        # Collecte des données région par région
        chaine_donnees=chaine_donnees + collecte_global_region(region,annee_min,annee_max)

        #print("Données de la region viticole : {}\n\n".format(region))

    return chaine_donnees


def sauvegarde_fichier_donnees(nom_fichier, chaine) :
    # Librairie pour déterminer le système d'exploitation de la plateforme
    import platform

    # Détermination du système d'exploitation sous lequel on exécute le programme de scraping
    if platform.uname()[0] == 'Windows' :
        path_file = os.getcwd() + '\\'+ nom_fichier
    else :
        path_file = os.getcwd() + '//'+ nom_fichier

    # sauvegarde des données dans un fichier    
    with open(path_file,'a') as file :
        file.write(chaine)
        file.close()

    return None


def collecte_region_viticole() :
    """Scraping des communes des régions viticoles"""
    
    # Liste des régions des vignobles
    region_viticole = ['Alsace',
                      'Beaujolais',
                      'Bordeaux',
                      'Bourgogne',
                      'Champagne'
                      'Cognac',
                      'Jura',
                      'Languedoc-roussillon',
                      'Loire',
                      'Lorraine',
                      'Provence-corse',
                      'Rhône',
                      'Savoie bugey',
                      'Sud-ouest']
    
    # Initialisation des variables
    compteur=0
    chaine_region_viticole='Region;Communes;CP;Population;Altitude_min;Altitude_moy;Altitude_max;Superficie'+'\n'
    
    # Scraping des éléments
    for region in region_viticole :
        chaine_region_viticole=chaine_region_viticole + collecte_tableau_commune(region_viticole[compteur],compteur)
        compteur+=1
        
    return chaine_region_viticole
        

def collecte_tableau_commune(nom_region_viticole,rang_region_tableau) :
    """Scraping d'un tableau de données déterminé par le rang_region_tableau"""

    # URL à scraper
    url = 'http://www.vin-vigne.com/commune/'
    
    # se connecter à la page et obtenir le code source
    requete = requests.get(url)
    page_html = requete.content

    # initialisation de la chaine qui contiendra toutes les données de la page web
    chaine = ""

    # transformer la page HTML en beautifulSoup pour pouvoir la manipuler
    soupe = BeautifulSoup(page_html, "html5lib")
    
    #Vérification des variables en entrée, on ne traite pas au delà de 4ième tableaux 
    
    # stocker les donnees des vins obtenues par scraping
    data = []
    table = soupe.find_all('table', attrs={'class': 'points'})[rang_region_tableau]
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if cols :   # on élmine les premières lignes non utiles et vides du tableau
            data.append(cols)
    
    # accumulation des données de chaque ligne et colonne dans une chaîne de caractère
    max_rows=len(data)
    max_cols=7
    for count_rows in range(max_rows) :
        chaine = chaine + nom_region_viticole                
        for count_cols in range(max_cols) :
            if data[count_rows][count_cols] :
                chaine=chaine+';'+data[count_rows][count_cols]
            else :
                chaine = chaine +';'
            ####print("chaine : {}".format(chaine))                
        chaine = chaine +'\n'
        
    return chaine


data_vignoble=collecte_france(1996, 2013)
sauvegarde_fichier_donnees('data_france_viticole.csv', data_vignoble)
print("Fin du traitement de collecte de données")
#print(data_vignoble)
