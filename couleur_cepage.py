import re
import requests
from bs4 import BeautifulSoup
import html5lib


f=str(open("/home/fitec/Bureau/links.txt","r").read())
liste=f.split("\n")

"""url="https://www.vins-bourgogne.fr/nos-vins-nos-terroirs/la-bourgogne-et-ses-appellations/aloxe-corton,2377,9170.html?&args=Y29tcF9pZD0yMjA1JmFjdGlvbj12aWV3RmljaGUmaWQ9MjExJnw%3D"
"""
with open("couleur", "w") as cl:
    cl.write("")
    cl.close()

for url in liste:
    requete=requests.get(url)
    page_html=requete.content
    page_BS=BeautifulSoup(page_html, "html5lib")
    couleur_text=page_BS.find_all('div', class_='portlet3')[0]

    couleur1=str(couleur_text.find_all('div', class_='col-md-offset-1')[0]).split('<br/>')[1].split(" ")[1]


    try:
        cepage1=str(couleur_text.find_all('div', class_='col-md-offset-1')[0]).split('<br/>')[1].split(" ")[-1]
    except:
        print (url)
        print ("cepage1")
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

