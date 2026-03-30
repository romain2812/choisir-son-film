import os 
from pathlib import Path
import mimetypes
from rapidfuzz import process

tab_fichier = os.listdir('film')


def est_video(fichier):
    type_mime, _ = mimetypes.guess_type(fichier)
    return type_mime is not None and type_mime.startswith("video") 

IGNORER = ["bonus", "sample","featurettes"]

def parcour_tab(path):
    resultat = []

    for element in Path(path).iterdir():
        if element.is_dir():
            if any(mot in str(element).lower() for mot in IGNORER):
                continue
            resultat += parcour_tab(element)
        elif est_video(element):
            resultat.append((element.name, str(element.parent)))

    return resultat


def unpack(tab,n):
    new_tab = []
    for i in tab:
        x,y = i 
        if n==1:
            new_tab.append(x)
        else:
            new_tab.append(y)
    return new_tab




def metreBonForma(tabFilm):
    for i in range(len(tabFilm)):
        tab = tabFilm[i].split(" ")
        if len(tab)==1:
            tab = tabFilm[i].split(".")
        tabFilm[i]=""
        for elt in tab:
            if '1' in elt or '2' in elt:
                break
            tabFilm[i]=tabFilm[i]+" "+elt
    return tabFilm


def afficher_choix(tab):
    i=0
    for elt in tab:
        i+=1
        print(f"{i}/{elt}")
    print(f"{i+1}/recherche")


def rechercher(films):
    mot = input("rechercher:")
    resultarecherche(process.extract(mot, films, limit=len(films)),films)

def resultarecherche(tab_res,tab_film):
    premier,_,_ = tab_res[0]
    dexieme,_,_ = tab_res[1]
    troisieme,_,_ = tab_res[2]
    print(f"{tab_film.index(premier)+1}/{premier}")
    print(f"{tab_film.index(dexieme)+1}/{dexieme}")
    print(f"{tab_film.index(troisieme)+1}/{troisieme}")



def choisir(tab):
    nb = input("choisiser votre film: ") 
    if int(nb)<=len(tab):
        return int(nb)-1
    if int(nb)==len(tab)+1:
        rechercher(tab)
    print("hors index")
    return choisir(tab)


def lancer(choix,tab):
    x,y = tab[choix]
    chemin = y+"/"+x
    chemin_modifie = chemin.replace("/", "\\")
    os.startfile(chemin_modifie)

tab_film_path = parcour_tab('film')
tab_film= unpack(tab_film_path,1)
tab_path= unpack(tab_film_path,2)
tab = metreBonForma(tab_film)
afficher_choix(tab)
choix = choisir(tab)
print(f"vous aves choisi{tab[choix]}")
lancer(choix,tab_film_path)
