import re
import requests
from bs4 import BeautifulSoup
import html5lib


"""Resecement des liens"""
lien = []
url="https://www.vins-bourgogne.fr/nos-vins-nos-terroirs/la-bourgogne-et-ses-appellations/la-bourgogne-une-localisation-privilegiee,2377,9170.html?&args=Y29tcF9pZD0yMjA1JmFjdGlvbj12aWV3RmljaGVXaXRoVmlnbmVyb24maWQ9MjExJmFwcGVsbGF0aW9uX2FwcGVsbGF0aW9uPUFsb3hlLUNvcnRvbiZhcHBlbGxhdGlvbl9kZXNjcmlwdGlvbj0mYXBwZWxsYXRpb25faWRfYWNjZXNzPTM1fA%3D%3D"
requete=requests.get(url)
page_html=requete.content
page_BS=BeautifulSoup(page_html, "html5lib")

vinRouge=page_BS.find('table', class_="points").getText()
print(vinRouge)