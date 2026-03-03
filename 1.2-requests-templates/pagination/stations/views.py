from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

import csv

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    bus_stations = []
    with open(BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bus_stations.append({'Name': row['Name'],
                                 'Street': row['Street'],
                                 'District': row['District']
                                 })
    paginator = Paginator(bus_stations, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page.object_list,
        'page': page
    }
    return render(request, 'stations/index.html', context)
