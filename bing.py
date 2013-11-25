import requests
from config import IMG_FORMATS
from local_settings import MS_KEY
from urllib import quote_plus
from utils import xweb


BASE_QUERY = r'https://api.datamarket.azure.com/Bing/Search/v1/Composite?Sources=%%27image%%27&Query=%%27%s%%27&$format=json&$skip=%i'
STEP = 50


def get(query, skip=0):
    query = BASE_QUERY % (quote_plus(query), skip)
    jdct = requests.get(query, auth=(MS_KEY, MS_KEY)).json()
    return jdct['d']['results'][0]['Image']


def xbinglinks(search, limit=100):
    while limit > 0:
        skip = 0
        results = get(search, skip=skip)
        for res in results[:limit - skip * STEP]:
            if any([fmt in res['ContentType'].lower() for fmt in IMG_FORMATS]):
                yield res['MediaUrl']
                limit -= 1
        skip += STEP


xbing = lambda x: xweb(xbinglinks(x))
