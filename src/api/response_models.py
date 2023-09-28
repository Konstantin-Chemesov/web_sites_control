from urllib.parse import urlparse


class StatusResponse():
    def __init__(self, exception_text: str = None):
        if not exception_text:
            self.status = {'status': 'ok'}
        else:
            self.status = {'status': str(exception_text)}


class LinksResponse():
    def __init__(self, visited_links: list):
        self.links_unique = set([urlparse(link_object.link).netloc for link_object in visited_links])
        self.response = {"domains": self.links_unique, 'status': 'ok'}