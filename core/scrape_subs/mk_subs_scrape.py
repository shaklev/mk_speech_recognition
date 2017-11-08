from lxml import html
import requests
import re
import urllib2
from random import randint

page = requests.get('https://podnapisi.net/subtitles/search/advanced?episodes=&language=mk&year=&keywords=&seasons=&page=2')
tree = html.fromstring(page.content)
all_links_obj = tree.xpath("//a[contains(@href,'subtitles/mk')]")
all_links = [ "https://podnapisi.net"+obj.attrib["href"] for obj in all_links_obj ]

all_links_fixed = []
for link in all_links:
    if "/download" not in link:
        all_links_fixed.append(link+"/download")

for link in all_links_fixed:
    try:
        f = urllib2.urlopen(link)
        with open(str(randint(10, 222222)), "wb") as code:
            code.write(f.read())
    except:
        pass

# data = r.text

# soup = BeautifulSoup(data)
#
# for link in soup.findAll('a', href=re.compile("subtitles/mk")):
#     print(link.get('href'))
