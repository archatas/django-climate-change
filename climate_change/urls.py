# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns("climate_change.views",
    url(
        r"^(?P<slug>[^/]+)/$",
        "display_charts",
        ),
    url(
        r"^(?P<slug>[^/]+)/temperature/",
        "json_get_statistics",
        {'field': "temperature"},
        name="climate_change_temperature",
        ),
    url(
        r"^(?P<slug>[^/]+)/humidity/",
        "json_get_statistics",
        {'field': "humidity"},
        name="climate_change_humidity",
        ),
    url(
        r"^(?P<slug>[^/]+)/wind-speed/",
        "json_get_statistics",
        {'field': "wind_speed"},
        name="climate_change_wind_speed",
        ),
    url(
        r"^(?P<slug>[^/]+)/visibility/",
        "json_get_statistics",
        {'field': "visibility"},
        name="climate_change_visibility",
        ),
    )
