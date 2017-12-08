from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict


INDEX_KEY = ('chocolate', 'vanilla', 'mint',
             'cake', 'cookies', 'nut/almond/pecan',
             'lemon', 'berry/cherries', 'sherbet',
             'other')
INDEX_KEY = sorted(INDEX_KEY, key=str.lower)
# quickly sort our index for clean output

quote_page = 'https://www.baskinrobbins.com/content/baskinrobbins/en/products/icecream/flavors.html'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
flavor = soup.find_all('h5', attrs={'class':'title'})

flavors_arr = []

for tag in flavor:
    flavors_arr.append(tag.string)
flavors_arr = [element.lower() for element in flavors_arr]

d  = defaultdict()
d= {key:[] for key in INDEX_KEY}
for flavor in flavors_arr:
    find = False
    for word in flavor.split(" "):
        for key in d:
            for x in key.split('/'):
                if x in word:
                    d[key].append(flavor)
                    find = True
                    break
        if find:
            break
    if not find:
        d['other'].append(flavor)

# Quickly sort the output arrys in the dict
for key in d:
    sorted(d[key])
try:
    f = open('flavors.txt', 'w')
    f.write('Notation Key: \n')
    for note in INDEX_KEY:
        f.write(''.join(list(note)[:3]))
        f.write('\n')
    f.write('\n************* Ice Cream!!! *************\n')
    for list in INDEX_KEY:
    # because we use the INDEX_KEY it preserves the order
        output = list + '\n'
        f.write(output.title())
        for value in d[list]:
            output = '\t'+value + '\n'
            f.write(output.title())
        f.write('\n')
except:
    print ("Unexpected error:")
    # none of this code should actually throw an error so
    # there is no need for a fancy catch
finally:
    f.close()
    # ensures the file gets closed
