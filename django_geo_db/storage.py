from django.contrib.staticfiles.templatetags.staticfiles import static
import urllib.request


class DataStorage:

    def __init__(self, domain):
        self.domain = domain
        self.star = None

    def get_static_or_media_data(self, url):
        if 'static' not in url:
            url = static(url)
        if 'http' not in url:
            url = self.domain + url
        response = urllib.request.urlopen(url)
        data = response.read()
        return data

    def get_star(self):
        if not self.star:
            self.star = self.get_static_or_media_data('img/django_geo_db/star.png')
        return self.star

