# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Action', fields ['report', 'action_subtype', 'action_type', 'entity']
        db.create_unique(u'safewater_action', ['report_id', 'action_subtype', 'action_type', 'entity'])


    def backwards(self, orm):
        # Removing unique constraint on 'Action', fields ['report', 'action_subtype', 'action_type', 'entity']
        db.delete_unique(u'safewater_action', ['report_id', 'action_subtype', 'action_type', 'entity'])


    models = {
        u'safewater.action': {
            'Meta': {'unique_together': "(('entity', 'action_type', 'action_subtype', 'report'),)", 'object_name': 'Action'},
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