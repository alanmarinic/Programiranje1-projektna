import os
import re
import json
import orodja
import requests

'''Shranni spletne strani'''
url_1 = 'http://books.toscrape.com/index.html'
orodja.shrani_spletno_stran(url_1, 'glavna_stran.html')
vsebina = orodja.vsebina_datoteke('glavna_stran.html')

knjige, kategorije_linki, kategorije_obdelava, linki_ctg, index_sez = [], [], [], [], ["index"]


'''Priprava linkov za iskanje po kategorijah'''
vzorec_kategorije_linki = (
    r'<a href=".*?/books/(?P<kategorija>.*_\d+)/.*>'
)
for zadetek in re.finditer(vzorec_kategorije_linki, vsebina):
    kategorije_linki.append(zadetek.groupdict())

for item in kategorije_linki:
    for ctg in item.values():
        linki_ctg.append(ctg)


'''Lepši zapis kategorij za shranjevanje datotek in obdelavo podatkov'''
vzorec_kategorije_obdelava= (
    r'<a href="catalogue/category/books/.*?/index.html">\W*(?P<kategorija>.*)\W*</a>'
)
for zadetek in re.finditer(vzorec_kategorije_obdelava, vsebina):
    kategorije_obdelava.append(zadetek.groupdict())

ktg_imena_datotek = []
for item in kategorije_obdelava:
    for ctg in item.values():
        ktg_imena_datotek.append(ctg)

#range(2, 9)
for i in range(2, 3):
    index_sez.append(f'page-{i}')

slovar_strani = {linki_ctg[i]: ktg_imena_datotek[i] for i in range(len(linki_ctg))}


'''Shranjevanje strani po kategorijah'''
# Spremembo sem naredil, ker je za iskanje po kategorijah potrebno 
# preleteti približno 900 strani manj kot pri iskanju po izdelkih, kar prihrani na času.
#for i in index_sez:
#    for item in slovar_strani:
#        url_2 = f'http://books.toscrape.com/catalogue/category/books/{item}/{i}.html'
#        ime_datoteke = (
#            f'zajeti-podatki/'
#            f'{slovar_strani.get(item).replace(" ", "_")}_od_'
#            f'{index_sez.index(i) * 20 + 1}_do_{(index_sez.index(i) + 1 ) * 20}.html'
#        )
#        orodja.shrani_spletno_stran(url_2, ime_datoteke)


'''Poišči vse knjige in jih dodaj v slovar z vsemi atributi'''
vzorec_ktg = (
    r'<h1>(?P<kategorija>.+?)</h1>' #KATEGORIJA
)
vzorec_knjige = (
    r'class="star-rating (?P<ocena>.*?)".*?'  #OCENA
    r'title="(?P<naslov>.*?)".*?'  #NASLOV
    r'class="price_color">..(?P<cena>.*?)<'  #CENA
)

milijon_strani = 'zajeti-podatki'
zacasni_seznam = []

for datoteka in os.listdir(milijon_strani):
    vsebina = orodja.vsebina_datoteke(f'zajeti-podatki/{datoteka}')
    for kategorija in re.finditer(vzorec_ktg, vsebina, flags=re.DOTALL):
        trenutna_ktg = kategorija.group()
        for zadetek in re.finditer(vzorec_knjige, vsebina, flags=re.DOTALL):
            zacasni_seznam.append(zadetek.groupdict())
            for slovar in zacasni_seznam:
                for li in zacasni_seznam:
                    li['kategorija'] = trenutna_ktg[4:-5:]
                knjige += zacasni_seznam
                zacasni_seznam.clear()

#knjigam dodaj id
i = 1
for slovar in knjige:
    slovar['id'] = i
    i += 1

print(knjige)
