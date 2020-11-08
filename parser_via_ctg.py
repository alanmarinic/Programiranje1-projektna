import requests
import re
import json
import orodja

'''Shranni spletne strani'''
url_1 = 'http://books.toscrape.com/index.html'
orodja.shrani_spletno_stran(url_1, 'zajeti-podatki/glavna_stran.html')

#for stran in range(2, 51):
#    url_2 = f'http://books.toscrape.com/catalogue/page-{stran}.html'
#    ime_datoteke = f'zajeti-podatki/knjige_od_{(stran - 1) * 20 + 1}_do_{(stran * 20)}.html'
#    orodja.shrani_spletno_stran(url_2, ime_datoteke)

vsebina = orodja.vsebina_datoteke('zajeti-podatki/glavna_stran.html')

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

for i in range(2,9):
    index_sez.append(f'page-{i}')

slovar_strani = {linki_ctg[i]: ktg_imena_datotek[i] for i in range(len(linki_ctg))}

for i in index_sez:
    for item in slovar_strani:
        url_2 = f'http://books.toscrape.com/catalogue/category/books/{item}/{i}.html'
        ime_datoteke = (
            f'zajeti-podatki/'
            f'{slovar_strani.get(item).replace(" ", "_")}_od_{index_sez.index(i) * 20 + 1}_do_{(index_sez.index(i) + 1 ) * 20}.html'
        )
        orodja.shrani_spletno_stran(url_2, ime_datoteke)
'''Poišči vse knjige in jih dodaj v slovar'''

# 1 probam shrant vse strani po kategorijah
# 2 tak regular expresion da bo shranu kategorijo zraven za usak film


#vzorec_knjige = (
#    r'class="star-rating (?P<ocena>.*?)".*?'  #OCENA
#    r'title="(?P<naslov>.*?)".*?'  #NASLOV
#    r'class="price_color">..(?P<cena>.*?)<'  #CENA
#)

#for zadetek in re.finditer(vzorec_knjige, vsebina, flags=re.DOTALL):
#    knjige.append(zadetek.groupdict())


#knjigam dodaj id
i = 1
for slovar in knjige:
    slovar['id'] = i
    i += 1
