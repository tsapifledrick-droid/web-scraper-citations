"""
Web Scraper - Extraction et traduction de citations
Extrait des citations d'un site web, les traduit en français,
et sauvegarde le resultat dans un fichier CSV.
"""

import requests
from bs4 import BeautifulSoup
import csv

def traduire(texte, langue_cible="fr"):
    """Traduit un texte via l'API Google Translate (gratuite, sans cle)"""
    url = "https://translate.googleapis.com/translate_a/single"
    parametres = {
        "client": "gtx",
        "sl": "en",
        "tl": langue_cible,
        "dt": "t",
        "q": texte
    }
    reponse = requests.get(url, params=parametres)
    resultat = reponse.json()
    return resultat[0][0][0]

def scraper_et_traduire(url, nom_fichier_csv):
    """Scrape une page de citations, traduit, et sauvegarde en CSV"""
    reponse = requests.get(url)
    soupe = BeautifulSoup(reponse.text, "html.parser")
    blocs_citation = soupe.find_all("div", class_="quote")

    with open(nom_fichier_csv, "w", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.writer(fichier)
        ecrivain.writerow(["Citation (EN)", "Citation (FR)", "Auteur"])

        for bloc in blocs_citation:
            texte_en = bloc.find("span", class_="text").text
            auteur = bloc.find("small", class_="author").text
            texte_fr = traduire(texte_en)
            ecrivain.writerow([texte_en, texte_fr, auteur])

    print("Termine. Donnees sauvegardees dans", nom_fichier_csv)


scraper_et_traduire("https://quotes.toscrape.com", "citations.csv")
