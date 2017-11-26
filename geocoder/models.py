import googlemaps
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class GeocodeCache(models.Model):
    key = models.CharField(max_length=500)
    hash = models.CharField(max_length=100, blank=True)
    is_zero_results = models.NullBooleanField(help_text='Indicates whether google has returned ZERO_RESULTS'
                                                        'for this address.')
    lat = models.FloatField()
    lng = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    accessed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.key


class GeocodeCacheAdmin(admin.ModelAdmin):
    list_display = ('key', 'lat', 'lng', 'created')


def init_gmaps():
    gmaps = googlemaps.Client(key='AIzaSyB4yHzhZQwIBtNf3RUMlkOsMmRjMqbAM60')
    return gmaps


def geocode_from_google(address):
    gmaps = init_gmaps()
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return lat, lng
    else:
        return None


def is_geocode_in_db(address):
    try:
        g = GeocodeCache.objects.get(key=address)
        return g.lat, g.lng
    except ObjectDoesNotExist:
        return None


def save_to_db(latlng, address):
    if latlng:
        try:
            g = GeocodeCache.objects.get(key=address).delete()
        except ObjectDoesNotExist:
            pass
        GeocodeCache.objects.create(key=address, lat=latlng[0], lng=latlng[1])


def geocode(address):
    address = address.strip()
    latlng = is_geocode_in_db(address)
    if not latlng:
        latlng = geocode_from_google(address)
        save_to_db(latlng, address)
    return latlng
