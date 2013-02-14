# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Area'
        db.create_table('invdb_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=50, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('invdb', ['Area'])

        # Adding model 'Rack'
        db.create_table('invdb_rack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invdb.Area'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('numu', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('invdb', ['Rack'])

        # Adding model 'PhysicalStatusCode'
        db.create_table('invdb_physicalstatuscode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('invdb', ['PhysicalStatusCode'])

        # Adding model 'LogicalStatusCode'
        db.create_table('invdb_logicalstatuscode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('invdb', ['LogicalStatusCode'])

        # Adding model 'Role'
        db.create_table('invdb_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('invdb', ['Role'])

        # Adding model 'Interface'
        db.create_table('invdb_interface', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True)),
            ('ip4', self.gf('django.db.models.fields.IPAddressField')(default=None, max_length=15, unique=True, null=True, blank=True)),
            ('vlan', self.gf('django.db.models.fields.IntegerField')(default='0', max_length=4, null=True, blank=True)),
            ('mac', self.gf('django.db.models.fields.CharField')(default=None, max_length=12, unique=True, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['invdb.Asset'], null=True, blank=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invdb.Interface'], null=True)),
        ))
        db.send_create_signal('invdb', ['Interface'])

        # Adding model 'AssetType'
        db.create_table('invdb_assettype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('invdb', ['AssetType'])

        # Adding model 'Asset'
        db.create_table('invdb_asset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset_type', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['invdb.AssetType'])),
            ('alt_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('asset_tag', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('purchase_date', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('primary_interface', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['invdb.Interface'], unique=True, null=True, blank=True)),
            ('console', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, unique=True, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('physical_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invdb.PhysicalStatusCode'])),
            ('logical_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invdb.LogicalStatusCode'])),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['invdb.Rack'], null=True, blank=True)),
            ('rack_u', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('rack_u_size', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('pdu0_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['invdb.Asset'], null=True, blank=True)),
        ))
        db.send_create_signal('invdb', ['Asset'])


    def backwards(self, orm):
        # Deleting model 'Area'
        db.delete_table('invdb_area')

        # Deleting model 'Rack'
        db.delete_table('invdb_rack')

        # Deleting model 'PhysicalStatusCode'
        db.delete_table('invdb_physicalstatuscode')

        # Deleting model 'LogicalStatusCode'
        db.delete_table('invdb_logicalstatuscode')

        # Deleting model 'Role'
        db.delete_table('invdb_role')

        # Deleting model 'Interface'
        db.delete_table('invdb_interface')

        # Deleting model 'AssetType'
        db.delete_table('invdb_assettype')

        # Deleting model 'Asset'
        db.delete_table('invdb_asset')


    models = {
        'invdb.area': {
            'Meta': {'object_name': 'Area'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'invdb.asset': {
            'Meta': {'object_name': 'Asset'},
            'alt_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'asset_tag': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'asset_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['invdb.AssetType']"}),
            'console': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logical_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invdb.LogicalStatusCode']"}),
            'model': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pdu0_id': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['invdb.Asset']", 'null': 'True', 'blank': 'True'}),
            'physical_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invdb.PhysicalStatusCode']"}),
            'primary_interface': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invdb.Interface']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'purchase_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['invdb.Rack']", 'null': 'True', 'blank': 'True'}),
            'rack_u': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'rack_u_size': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'invdb.assettype': {
            'Meta': {'object_name': 'AssetType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'invdb.interface': {
            'Meta': {'object_name': 'Interface'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip4': ('django.db.models.fields.IPAddressField', [], {'default': 'None', 'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['invdb.Asset']", 'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invdb.Interface']", 'null': 'True'}),
            'vlan': ('django.db.models.fields.IntegerField', [], {'default': "'0'", 'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'invdb.logicalstatuscode': {
            'Meta': {'object_name': 'LogicalStatusCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'invdb.physicalstatuscode': {
            'Meta': {'object_name': 'PhysicalStatusCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'invdb.rack': {
            'Meta': {'object_name': 'Rack'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invdb.Area']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'numu': ('django.db.models.fields.IntegerField', [], {})
        },
        'invdb.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['invdb']