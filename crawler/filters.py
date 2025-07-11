from urllib.parse import urldefrag

def normalize_url(url):
    # Remove fragment and trailing slash
    url, _ = urldefrag(url)
    return url.rstrip('/')

class VisitedSet:
    def __init__(self):
        self._visited = set()
    def add(self, url):
        self._visited.add(url)
    def __contains__(self, url):
        return url in self._visited
