# -*- coding: UTF-8 -*-
import urllib
from xml.dom import minidom
from pprint import pprint
from datetime import datetime

from django.db import models
from django.core.management.base import NoArgsCommand

Location = models.get_model("climate_change", "Location")
WeatherLog = models.get_model("climate_change", "WeatherLog")

SILENT, NORMAL, VERBOSE = 0, 1, 2

WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s&u=c'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

def weather_for_location(location_id):
    # taken from http://developer.yahoo.com/python/python-xml.html
    # and modified a little
    url = WEATHER_URL % location_id
    dom = minidom.parse(urllib.urlopen(url))
    forecasts = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'forecast'):
        forecasts.append({
            'date': node.getAttribute('date'),
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition': node.getAttribute('text')
        })
    ycondition = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
    ywind = dom.getElementsByTagNameNS(WEATHER_NS, 'wind')[0]
    yatmosphere = dom.getElementsByTagNameNS(WEATHER_NS, 'atmosphere')[0]
    return {
        'current_condition': ycondition.getAttribute('text'),
        'current_temp': ycondition.getAttribute('temp'),
        'current_humidity': yatmosphere.getAttribute('humidity'),
        'current_visibility': yatmosphere.getAttribute('visibility'),
        'current_wind_speed': ywind.getAttribute('speed'),
        'forecasts': forecasts,
        'title': dom.getElementsByTagName('title')[0].firstChild.data,
        'guid': dom.getElementsByTagName('guid')[0].firstChild.data,
    }            

class Command(NoArgsCommand):
    help = "Aggregates data from weather feed"
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        
        created_count = 0
        for l in Location.objects.all():
            weather = weather_for_location(l.location_id)
            if verbosity > SILENT:
                pprint(weather)
            timestamp_parts = map(int, weather['guid'].split("_")[1:-1])
            timestamp = datetime(*timestamp_parts)
            log, created = WeatherLog.objects.get_or_create(
                 location=l,
                 timestamp=timestamp,
                 defaults={
                    'temperature': weather['current_temp'],
                    'humidity': weather['current_humidity'],
                    'wind_speed': weather['current_wind_speed'],
                    'visibility': weather['current_visibility'],
                    }
                 )
            if created:
                created_count += 1
        if verbosity > SILENT:
            print "New weather logs: %d" % created_count
                

