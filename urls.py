# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns("",
    (
        r"^$",
        "django.views.generic.simple.direct_to_template",
        {'template': "index.html"},
        ),
    (
        r"^climate-change/",
        include("climate_change.urls"),
        ),
    (
        r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT},
        ),
    (r"^admin/", include(admin.site.urls)),
    )
