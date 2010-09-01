# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Teacher'
        db.delete_table('eplace_teacher')

        # Removing M2M table for field subjects on 'Teacher'
        db.delete_table('eplace_teacher_subjects')

        # Removing M2M table for field groups on 'Teacher'
        db.delete_table('eplace_teacher_groups')

        # Deleting model 'Superviser'
        db.delete_table('eplace_superviser')

        # Removing M2M table for field groups on 'Superviser'
        db.delete_table('eplace_superviser_groups')

        # Adding field 'Group.start_year'
        db.add_column('eplace_group', 'start_year', self.gf('django.db.models.fields.IntegerField')(default=2010), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Teacher'
        db.create_table('eplace_teacher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('eplace', ['Teacher'])

        # Adding M2M table for field subjects on 'Teacher'
        db.create_table('eplace_teacher_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('teacher', models.ForeignKey(orm['eplace.teacher'], null=False)),
            ('subject', models.ForeignKey(orm['eplace.subject'], null=False))
        ))
        db.create_unique('eplace_teacher_subjects', ['teacher_id', 'subject_id'])

        # Adding M2M table for field groups on 'Teacher'
        db.create_table('eplace_teacher_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('teacher', models.ForeignKey(orm['eplace.teacher'], null=False)),
            ('group', models.ForeignKey(orm['eplace.group'], null=False))
        ))
        db.create_unique('eplace_teacher_groups', ['teacher_id', 'group_id'])

        # Adding model 'Superviser'
        db.create_table('eplace_superviser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('eplace', ['Superviser'])

        # Adding M2M table for field groups on 'Superviser'
        db.create_table('eplace_superviser_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('superviser', models.ForeignKey(orm['eplace.superviser'], null=False)),
            ('group', models.ForeignKey(orm['eplace.group'], null=False))
        ))
        db.create_unique('eplace_superviser_groups', ['superviser_id', 'group_id'])

        # Deleting field 'Group.start_year'
        db.delete_column('eplace_group', 'start_year')


    models = {
        'eplace.faculty': {
            'Meta': {'object_name': 'Faculty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'eplace.group': {
            'Meta': {'object_name': 'Group'},
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Faculty']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_year': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'eplace.student': {
            'Meta': {'object_name': 'Student'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'eplace.subject': {
            'Meta': {'object_name': 'Subject'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['eplace']
