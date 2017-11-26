import re
import logging
import httplib2
import urllib.parse

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

import geocoder.models
from .models import Data


logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def geocode_address(address):
    geocode_result = geocoder.models.geocode(address)
    if not geocode_result:
        raise ValueError('Geocoding {} resulted in error'.format(address))
    return geocode_result


def geocode_locations(locations):
    geocodes = []
    for location in locations:
        try:
            lat_lng = geocode_address(location)
            logger.debug('    {}'.format(lat_lng))
            geocodes.append(lat_lng)
        except ValueError as e:
            logger.warning(e)
    return geocodes


def process_locations(locations):
    logger.info('Processing locations ...')
    parsed_location = []
    for location in locations.splitlines():
        location = location.strip()
        if location:
            m = re.search('(?:[A-Z]{0,2}[ -]?(?P<zip>[\d]{4,5}[\t ]))?(?P<city>[\w. -]+)', location)
            if m:
                city = m['city']
                try:
                    city = '{} {}'.format(m['zip'], city)
                except KeyError:
                    pass
                logger.debug('{}:'.format(city))
                parsed_location.append(city)
    return parsed_location


def get_center_of_gravity(lat_lngs):
    logger.info('Calculating center of gravity ...')
    sum_lat = 0
    sum_lng = 0
    for lat_lng in lat_lngs:
        sum_lat += lat_lng[0]
        sum_lng += lat_lng[1]
    center_of_gravity = (sum_lat / len(lat_lngs), sum_lng / len(lat_lngs))
    logger.info('{}:'.format(center_of_gravity))
    return center_of_gravity


def index(request):
    logger.info('Entering index view ...')
    lat_lngs = []
    center_of_gravity = []
    data_list = Data.objects.order_by('key')
    try:
        locations = Data.objects.get(key='location').data
        locations = process_locations(locations)
        lat_lngs = geocode_locations(locations)
        logger.debug('lat_lngs: {}:'.format(lat_lngs))
        center_of_gravity = get_center_of_gravity(lat_lngs)
        logger.debug('{}:'.format(center_of_gravity))
    except ObjectDoesNotExist:
        logger.warning(request, 'Data `key=location` does not exist.')
        messages.warning(request, 'Data `key=location` does not exist.')
    context = {'data_list': data_list, 'lat_lngs': lat_lngs,
               'center_of_gravity': center_of_gravity}
    return render(request, 'index.html', context)


def about(request):
    context = {}
    return render(request, 'about.html', context)
