import re

with open('Glavna_stran.html') as f:
    vsebina = f.read()

# kategorije 
vzorec = (
    r'<a href="../books/(?P<ktegorija>.*_\d+)/.*>'
)

count = 0
for zadetek in re.finditer(vzorec, vsebina):
    print(zadetek.groupdict())
    count += 1
print(count)

