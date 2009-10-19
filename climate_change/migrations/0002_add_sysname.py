# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from climate_change.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Location.sysname'
        db.add_column('climate_change_location', 'sysname', orm['climate_change.location:sysname'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Location.sysname'
        db.delete_column('climate_change_location', 'sysname')
        
    
    
    models = {
        'climate_change.location': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '200', 'unique': 'True', 'db_index': 'True', 'blank': 'True'})
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
