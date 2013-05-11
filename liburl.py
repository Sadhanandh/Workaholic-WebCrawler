import urllib2
def fetchurllib2(url):
    data = ""
    try:
        res = urllib2.urlopen(url)
        data = res.read()
    except Exception:
        pass
        #log Exception
    return data


def fetchrequests(url):
    import requests
    data = ""
    try:
        res = requests.get(url)
        data = res.text
    except Exception:
        pass
        #log Exception
    return data


def fetch(url):
    return fetchurllib2(url)

def fetchwheader(url,uaheader="FakeFireFox/1.0"):
    """Example Use uaheader as -> "Mozilla/5.0 (X11; U; Linux i386) Gecko/20091127 Firefox/2.0.0.12"""
    data = ""
    try:
        req = urllib2.Request(url)
        opener = urllib2.build_opener() 
        req.add_header('User-Agent',uaheader)
        data= opener.open(req).read() 
    except Exception:
        pass
    return data

