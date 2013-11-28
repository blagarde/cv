import requests
from local_settings import MS_KEY
from urllib import quote_plus
from utils import xweb, write_to
from argparse import ArgumentParser
from config import DEFAULT_ROOT, DEFAULT_FMT, IMG_FORMATS

BASE_QUERY = r'https://api.datamarket.azure.com/Bing/Search/v1/Composite?Sources=%%27image%%27&Query=%%27%s%%27&$format=json&$skip=%i'
STEP = 50


def get(query, skip=0):
    query = BASE_QUERY % (quote_plus(query), skip)
    print "Bing!", query
    jdct = requests.get(query, auth=(MS_KEY, MS_KEY)).json()
    return jdct['d']['results'][0]['Image']


def xbinglinks(search, limit=100, forever=False, maxemptyqueries=2):
    skip = 0
    quota = maxemptyqueries
    while (forever or limit > 0) and quota > 0:
        quota -= 1
        results = get(search, skip=skip)
        for res in results:
            if any([fmt in res['ContentType'].lower() for fmt in IMG_FORMATS]):
                yield res['MediaUrl']
                limit -= 1
                quota = maxemptyqueries
                if limit <= 0 and not forever:
                    raise StopIteration("Target number of links reached")
        skip += STEP


xbing = lambda x: xweb(xbinglinks(x, forever=True))
zbing = lambda x: xweb(xbinglinks(x))


if __name__ == "__main__":
    parser = ArgumentParser(description="Capture faces")
    parser.add_argument('-o', '--output', default=DEFAULT_ROOT, type=str, help="Path to destination folder (must be writable)")
    parser.add_argument('-n', '--nfaces', type=int, default=None, help="Number of faces to collect")
    parser.add_argument('-f', '--format', type=str, default=DEFAULT_FMT, choices=IMG_FORMATS, help="Output image file format")
    parser.add_argument('source', type=str, help="Single argument, e.g. folder name, search query, webcam URL, video path.")
    args = parser.parse_args()

    write_to(zbing(args.source), args.output, format=args.format)
