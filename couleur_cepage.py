import re
import requests
from bs4 import BeautifulSoup
import html5lib


"""Resecement des liens"""
lien = []
url="https://www.vins-bourgogne.fr/nos-vins-nos-terroirs/la-bourgogne-et-ses-appellations/la-bourgogne-une-localisation-privilegiee,2377,9170.html?&args=Y29tcF9pZD0yMjA1JmFjdGlvbj12aWV3RnVsbExpc3RlQ2xpbWF0JmlkPSZ8"
requete=requests.get(url)
page_html=requete.content
page_BS=BeautifulSoup(page_html, "html5lib")

count=len(page_BS.find_all('li',class_="{appellation_class}"))


for i in range(count):
    lien.append(page_BS.find_all('li',class_="{appellation_class}")[i].a.get("href"))


"""transformer list en set pour eliminer les liens doublonnés"""
lien_unique=set(lien)

"""ajouter préfix http://www.vins-bourgogne.fr à tous les liens"""

lien_corrige=[]
prefix="https://www.vins-bourgogne.fr"

lien_corrige=[prefix+i for i in lien_unique]


with open("couleur", "w") as cl:
    cl.write("")
    cl.close()

for url in lien_corrige:
    requete=requests.get(url)
    page_html=requete.content
    page_BS=BeautifulSoup(page_html, "html5lib")
    couleur_text=page_BS.find_all('div', class_='portlet3')[0]

    try:
        couleur1=str(couleur_text.find_all('div', class_='col-md-offset-1')[0]).split('<br/>')[1].split(" ")[1]
    except:
        print("couleur1, page na pas ce contenu")

    try:
        cepage1=str(couleur_text.find_all('div', class_='col-md-offset-1')[0]).split('<br/>')[1].split(" ")[-1]
    except:
        print("cepage2, page na pas ce contenu")

    try:
        couleur2=str(couleur_text.find_all('div', class_='col-md-offset-1')[0]).split('<br/>')[2].split(" ")[1]
    except:
        print (url)
        print ("couleur2")
        pass

    try:
        cepage2=str(couleur_text.find_all('div', class_='col-md-offset-1')[0]).split('<br/>')[2].split(" ")[-1]
    except:
        print (url)
        print("cepage2")
        pass

    try:
        AOP=str(page_BS.h1.getText())
    except:
        print(url)
        print("AOP")


    with open("couleur", "a") as cl:

        cl.write(AOP)
        cl.write(couleur1+'\n')
        cl.write(cepage1+'\n')
        cl.write(couleur2 + '\n')
        cl.write(cepage2+'\n')