# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table(u'safewater_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('source_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('date_taken', self.gf('django.db.models.fields.DateField')(null=True)),
            ('log', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('entity', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('action_subtype', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['safewater.Report'])),
        ))
        db.send_create_signal(u'safewater', ['Action'])

        # Adding field 'Report.date_created'
        db.add_column(u'safewater_report', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 19, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Report.last_updated'
        db.add_column(u'safewater_report', 'last_updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 10, 19, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Report.contaminant_name'
        db.alter_column(u'safewater_report', 'contaminant_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))
        # Adding field 'PublicWaterSource.date_created'
        db.add_column(u'safewater_publicwatersource', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 19, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'PublicWaterSource.last_updated'
        db.alter_column(u'safewater_publicwatersource', 'last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):
        # Deleting model 'Action'
        db.delete_table(u'safewater_action')

        # Deleting field 'Report.date_created'
        db.delete_column(u'safewater_report', 'date_created')

        # Deleting field 'Report.last_updated'
        db.delete_column(u'safewater_report', 'last_updated')


        # Changing field 'Report.contaminant_name'
        db.alter_column(u'safewater_report', 'contaminant_name', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))
        # Deleting field 'PublicWaterSource.date_created'
        db.delete_column(u'safewater_publicwatersource', 'date_created')


        # Changing field 'PublicWaterSource.last_updated'
        db.alter_column(u'safewater_publicwatersource', 'last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    models = {
        u'safewater.action': {
            'Meta': {'object_name': 'Action'},
            'action_subtype': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'log': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['safewater.Report']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'source_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'safewater.publicwatersource': {
            'Meta': {'object_name': 'PublicWaterSource'},
            'contact_addr1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'contact_addr2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'contact_city': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'contact_org_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'contact_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'contact_zip': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'date_closed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'epa_region': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'fips_county': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'geography_type': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'owner_type': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True'}),
            'population_served': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'primary_source': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'primary_source_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'pwsid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'pwstype': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True'}),
            'regulating_agency_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'})
        },
        u'safewater.report': {
            'Meta': {'object_name': 'Report'},
            'contaminant_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'contaminant_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_reported': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_resolved': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_url1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'info_url2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'info_url3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'info_url4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pws_affected': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['safewater.PublicWaterSource']"}),
            'report_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'severity': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'source_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'verification': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'violation_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        }
    }

    complete_apps = ['safewater']