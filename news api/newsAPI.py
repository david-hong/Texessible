import feedparser

d = feedparser.parse('http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&output=rss')

def getSites():
    x = ""
    for i in range (0, 10):
        x += (str(i+1)+": " + d.entries[i]['title']+"\n")
    return x

def getLinks(n = 0):
    x = (str(n+1)+": "+ d.entries[n]['link']+"\n")
    return x
