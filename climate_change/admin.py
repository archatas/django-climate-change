# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

Location = models.get_model("climate_change", "Location")
WeatherLog = models.get_model("climate_change", "WeatherLog")

admin.site.register(Location)
admin.site.register(WeatherLog)

