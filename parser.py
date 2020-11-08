import requests
import re
import json
import orodja

'''Shranni sletne strani'''
#url_1 = 'http://books.toscrape.com/index.html'
#orodja.shrani_spletno_stran(url_1, 'zajeti-podatki/glavna_stran.html')
#
#for stran in range(2, 51):
#    url_2 = f'http://books.toscrape.com/catalogue/page-{stran}.html'
#    ime_datoteke = f'zajeti-podatki/knjige_od_{(stran - 1) * 20 + 1}_do_{(stran * 20)}.html'
#    orodja.shrani_spletno_stran(url_2, ime_datoteke)

vsebina = orodja.vsebina_datoteke('zajeti-podatki/glavna_stran.html')


knjige, kategorije, id = [], [], [x for x in range(21)]

'''Vzorci in funkcije iskanja podatkov'''
vzorec_knjige = (
    r'class="star-rating (?P<ocena>.*?)".*?'  #OCENA
    r'title="(?P<naslov>.*?)".*?'  #NASLOV
    r'class="price_color">..(?P<cena>.*?)<'  #CENA
)
vzorec_kategorije = (
    r'<a href=".*?/books/(?P<kategorija>.*)_\d+/.*>'
)

for zadetek in re.finditer(vzorec_knjige, vsebina, flags=re.DOTALL):
    knjige.append(zadetek.groupdict())

for zadetek in re.finditer(vzorec_kategorije, vsebina):
    kategorije.append(zadetek.groupdict())





#print(knjige)



#           shrani v json slovar
#           with open('knjige.json', 'w') as f:
#               json.dump(knjige, f)