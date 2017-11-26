from django.contrib import admin

from .models import Data
from geocoder.models import GeocodeCache, GeocodeCacheAdmin

admin.site.register(Data)
admin.site.register(GeocodeCache, GeocodeCacheAdmin)
