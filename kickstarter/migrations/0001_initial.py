# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceCheck'
        db.create_table('kickstarter_servicecheck', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('command', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('result', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('kickstarter', ['ServiceCheck'])

        # Adding model 'kssettings'
        db.create_table('kickstarter_kssettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('setting', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('permanent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('kickstarter', ['kssettings'])

        # Adding model 'BootOption'
        db.create_table('kickstarter_bootoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('label', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('kernel', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('append', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('kickstarter', ['BootOption'])


    def backwards(self, orm):
        # Deleting model 'ServiceCheck'
        db.delete_table('kickstarter_servicecheck')

        # Deleting model 'kssettings'
        db.delete_table('kickstarter_kssettings')

        # Deleting model 'BootOption'
        db.delete_table('kickstarter_bootoption')


    models = {
        'kickstarter.bootoption': {
            'Meta': {'object_name': 'BootOption'},
            'append': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kernel': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'kickstarter.kssettings': {
            'Meta': {'object_name': 'kssettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'permanent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'setting': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'kickstarter.servicecheck': {
            'Meta': {'object_name': 'ServiceCheck'},
            'command': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['kickstarter']