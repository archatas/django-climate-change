# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from climate_change.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'WeatherLog'
        db.create_table('climate_change_weatherlog', (
            ('id', orm['climate_change.WeatherLog:id']),
            ('location', orm['climate_change.WeatherLog:location']),
            ('timestamp', orm['climate_change.WeatherLog:timestamp']),
            ('temperature', orm['climate_change.WeatherLog:temperature']),
            ('humidity', orm['climate_change.WeatherLog:humidity']),
            ('wind_speed', orm['climate_change.WeatherLog:wind_speed']),
            ('visibility', orm['climate_change.WeatherLog:visibility']),
        ))
        db.send_create_signal('climate_change', ['WeatherLog'])
        
        # Adding model 'Location'
        db.create_table('climate_change_location', (
            ('id', orm['climate_change.Location:id']),
            ('name', orm['climate_change.Location:name']),
            ('location_id', orm['climate_change.Location:location_id']),
        ))
        db.send_create_signal('climate_change', ['Location'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'WeatherLog'
        db.delete_table('climate_change_weatherlog')
        
        # Deleting model 'Location'
        db.delete_table('climate_change_location')
        
    
    
    models = {
        'climate_change.location': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'climate_change.weatherlog': {
            'humidity': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['climate_change.Location']"}),
            'temperature': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'visibility': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'wind_speed': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }
    
    complete_apps = ['climate_change']
