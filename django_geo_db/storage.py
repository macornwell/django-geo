from django.contrib.staticfiles.templatetags.staticfiles import static
import urllib.request
from django.core.files.storage import default_storage

class DataStorage:

    def __init__(self, domain):
        self.domain = domain
        self.star = None

    def _get_static_url(self, url):
        if 'static' not in url:
            url = static(url)
        if 'http' not in url:
            url = self.domain + url
        return url

    def _get_media_url(self, url):
        return url

    def get_static_or_media_data(self, url):
        url = self._get_static_url(url)
        response = urllib.request.urlopen(url)
        data = response.read()
        return data

    def get_star(self):
        if not self.star:
            self.star = self.get_static_or_media_data('img/django_geo_db/star.png')
        return self.star

    def delete_file(self, url):
        default_storage.delete(url)

    def save_file_get_url(self, image, directory, filename):
        url = '{0}/{1}'.format(directory, filename)
        url = self._get_media_url(url)
        url = default_storage.save(url, image)
        return url
