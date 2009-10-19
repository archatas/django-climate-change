# -*- coding: UTF-8 -*-
from django.db import models
from django import template
from django.template import loader

register = template.Library()

### TAGS ###

def do_get_current_weather(parser, token):
    """
    Returns the latest known weather information.

    Usage::

        {% get_current_weather in <location_sysname> [using <template_path>] [as <var_name>] %}
    
    Examples::

        {% get_current_weather in "berlin" using "climate_change/custom_weather.html" %}

        {% get_current_weather in "london" as current_weather %}
        var sCurrentWeather = "{{ current_weather|escapejs }}";

    """    
    bits = token.split_contents()
    tag_name = bits.pop(0)
    template_path = ""
    var_name = ""
    location_sysname = ""
    try:
        while bits:
            first_word = bits.pop(0)
            second_word = bits.pop(0)
            if first_word == "in":
                location_sysname = second_word
            elif first_word == "using":
                template_path = second_word
            elif first_word == "as":
                var_name = second_word
                    
    except ValueError:
        raise template.TemplateSyntaxError, "get_current_weather tag requires a following syntax: {% get_current_weather [using <template_path>] [as <var_name>] %}"
    return CurrentWeatherNode(tag_name, location_sysname, template_path, var_name)

class CurrentWeatherNode(template.Node):
    def __init__(self, tag_name, location_sysname, template_path, var_name):
        self.tag_name = tag_name
        self.location_sysname = location_sysname
        self.template_path = template_path
        self.var_name = var_name
    def render(self, context):
        location_sysname = template.resolve_variable(
            self.location_sysname,
            context,
            )
        template_path = ""
        if self.template_path:
            template_path = template.resolve_variable(
                self.template_path,
                context,
                )
        context.push()
        WeatherLog = models.get_model("climate_change", "WeatherLog")
        logs = WeatherLog.objects.filter(
            location__sysname=location_sysname,
            ).order_by("-timestamp")
        if logs:
            context['weather'] = logs[0]
        output = loader.render_to_string(
            [template_path, "climate_change/current_weather.html"],
            context,
            )
        context.pop()
        if self.var_name:
            context[self.var_name] = output
            return ""
        else:
            return output


register.tag("get_current_weather", do_get_current_weather)

### FILTERS ###

# none at the moment
