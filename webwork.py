import liburl
from lxml.html import fromstring
from urlparse import urljoin


def process((url,depth)):
    links = []
    raw_html = liburl.fetch(url)
    #raw_html = liburl.fetchwheader(url) for UserAgent header
    try:
        tree = fromstring(raw_html)
        elems = tree.cssselect("a")
        links = [(urljoin(url,x.attrib["href"]).strip("/"),depth+1) for x in elems]
    except  Exception:
        pass
    return links

