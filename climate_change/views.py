# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from random import random

# http://open-flash-chart-python.googlecode.com/files/Python%202.10.zip
from OpenFlashChart import Chart

from django.db import models
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode

Location = models.get_model("climate_change", "Location")
WeatherLog = models.get_model("climate_change", "WeatherLog")

def display_charts(request, slug):
    location = get_object_or_404(Location, slug=slug)
    return render_to_response(
        "climate_change/charts.html",
        {'location': location},
        context_instance=RequestContext(request),
        )

def rgb_to_html_color(r, g, b):
    """ convert an R, G, B to #RRGGBB """
    return '#%02x%02x%02x' % (r, g, b)

def json_get_statistics(request, slug, field):
    location = get_object_or_404(Location, slug=slug)
    extreme_values = location.weatherlog_set.aggregate(
        models.Min(field),
        models.Max(field),
        models.Min("timestamp"),
        models.Max("timestamp"),
        )
    elements = []

    for year in range(
        extreme_values['timestamp__min'].year,
        extreme_values['timestamp__max'].year + 1,
        ):
        element = Chart()
        monthly_values = []
        for month in range (1, 13):
            monthly = location.weatherlog_set.filter(
                timestamp__year=year,
                timestamp__month=month,
                ).aggregate(models.Avg(field))
            monthly_values.append(monthly['%s__avg' % field])
        element.values = monthly_values
        element.type = "line"
        element.dot_style.type = "dot"
        element.dot_style.dot_size = 5
        random_html_color = rgb_to_html_color(
            r=63+int(random() * 128),
            g=63+int(random() * 128),
            b=63+int(random() * 128),
            )
        element.dot_style.colour = random_html_color
        element.width = 4
        element.colour = random_html_color
        element.text = str(year)
        element.font_size = 10
        elements.append(element)
    
    # Create chart
    chart = Chart()
    chart.y_axis.min = float(str(extreme_values['%s__min' % field]))
    chart.y_axis.max = float(str(extreme_values['%s__max' % field]))
    chart.y_axis.font_size = 10
    chart.title.text = force_unicode(WeatherLog._meta.get_field(field).verbose_name)
    chart.x_axis.labels.labels = [
        _("Jan"), _("Feb"), _("Mar"), _("Apr"),
        _("May"), _("Jun"), _("Jul"), _("Aug"),
        _("Sep"), _("Oct"), _("Nov"), _("Dec"),
        ]

    #
    # here we add our data sets to the chart:
    #
    chart.elements = elements
    
    return HttpResponse(chart.create())

