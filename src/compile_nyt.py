from bs4 import BeautifulSoup as Soup

paths = []

with open('dat/corpora/nyt/great.txt', 'r') as fle:
    for line in fle:
        p = line.strip().replace('_', '/')
        paths.append(p)

with open('dat/corpora/nyt/verygood.txt', 'r') as fle:
    for line in fle:
        p = line.strip().replace('_', '/')
        paths.append(p)

with open('dat/corpora/nyt/typical.txt', 'r') as fle:
    for line in fle:
        p = line.strip().replace('_', '/')
        paths.append(p)

base = 'dat/corpora/nyt/nyt_corpus/data/'
out = 'dat/corpora/nyt-science/'
for p in paths:
    handler = open(base + p).read()
    soup = Soup(handler, "xml")
    for message in soup.findAll("block", {"class": "full_text"}):
        with open(out + p.replace('/', '_'), 'w') as fle:
            fle.write(message.text)
