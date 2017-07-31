from django import forms
from django.conf import settings
from django.template.loader import render_to_string

class GeocoordinateWidget(forms.TextInput):
    template_name = 'geocoordinate.html'
    css = {
            'all': ('styles.css',)
        }

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'value': value,
            'GM_SETTINGS': settings.GM_SETTINGS,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
        }
        return render_to_string(self.template_name, context)
