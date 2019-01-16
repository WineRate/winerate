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

list_lien=[]
for url in lien_corrige:
    requete=requests.get(url)
    page_html=requete.content
    page_BS1=BeautifulSoup(page_html, "html5lib")
    lien_div=page_BS1.find_all('div', class_='portlet3')[1]
    lien_li=lien_div.find_all('li', class_='lien')[0].a.get("href")
    list_lien.append(lien_li)

prefix1="https://www.vins-bourgogne.fr"

list_lien_corrige=[prefix1+j for j in list_lien]

with open("code_postal", "w") as cd:
    cd.write("")
    cd.close()

for url in list_lien_corrige:
    requete = requests.get(url)
    page_html = requete.content
    page_BS2 = BeautifulSoup(page_html, "html5lib")
    text=page_BS2.find('div', attrs={"id":u"resultatAppellation"}).getText()
    text2=re.findall(r'\d+', text)
    ville=(page_BS2.title.getText().split())[-1]
    with open("code_postal", "a") as cd:
        cd.write(str(ville))
        cd.write(str(text2))

