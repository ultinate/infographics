# GENERAL VIEWS
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages

from .models import Data


def index(request):
    locations = ''
    data_list = Data.objects.order_by('key')
    try:
        locations = Data.objects.get(key='location').data
        locations = locations.splitlines()
        messages.debug(request, 'Locations is: %s' % locations)
    except ObjectDoesNotExist:
        messages.warning(request, 'Data `key=location` does not exist.')
    context = {'data_list': data_list, 'locations': locations}
    return render(request, 'index.html', context)


def about(request):
    context = {}
    return render(request, 'about.html', context)
