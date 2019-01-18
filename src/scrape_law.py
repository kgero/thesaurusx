import urllib.request
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Referer': 'https://cssspritegenerator.com',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def get_article_urls(url):
    """Return list of url strings with articles on page of url."""
    core = "https://www.mdpi.com"

    req = urllib.request.Request(url, None, hdr) #The assembled request
    resp = urllib.request.urlopen(req)
    page = resp.read() # The data u need
    soup = BeautifulSoup(page, 'html.parser')

    links = soup.find_all('a', string="HTML Full-text")
    res = []
    for a in links:
        res.append(core + a['href'])
    return res


def get_doc(url):
    """Return string of full contents of law article at url."""
    req = urllib.request.Request(url, None, hdr) #The assembled request
    resp = urllib.request.urlopen(req)
    page = resp.read() # The data u need
    soup = BeautifulSoup(page, 'html.parser')

    doc = ''

    if soup.find('section', id='html-abstract') is None:
        return ''

    abstract = soup.find('section', id='html-abstract').get_text()
    doc += abstract + '\n'

    sections = soup.find("div", class_="html-body").find_all('section')
    for sec in sections:
        try:
            title = sec.h2.get_text()
        except:
            try:
                title = sec.h4.get_text()
            except:
                print(sec)
                raise AttributeError
        doc += '\n' + title + '\n'

        content = sec.find_all('p')
        if not content:
            content = sec.find_all('div')
        for text in content:
            doc += text.get_text() +'\n'

    return doc


core = "https://www.mdpi.com"
for vol in range(1, 9):
    for issue in range(1, 5):
        url = "https://www.mdpi.com/2075-471X/{}/{}".format(vol, issue)
        print('looking at', url)
        articles = get_article_urls(url)
        for art in articles:
            doc = get_doc(art)
            flnm = "2075-471X.{}.{}.{}".format(vol, issue, art.split('/')[6])
            with open('dat/law/' + flnm, 'w') as fle:
                fle.write(doc)
            print('wrote', flnm)
