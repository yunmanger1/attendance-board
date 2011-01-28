# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Student.info'
        db.alter_column('eplace_student', 'info', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Student.email'
        db.alter_column('eplace_student', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))


    def backwards(self, orm):
        
        # Changing field 'Student.info'
        db.alter_column('eplace_student', 'info', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Student.email'
        db.alter_column('eplace_student', 'email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eplace.copypastestudents': {
            'Meta': {'object_name': 'CopyPasteStudents'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'eplace.dean': {
            'Meta': {'unique_together': "(('user', 'faculty'),)", 'object_name': 'Dean'},
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Faculty']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'eplace.faculty': {
            'Meta': {'object_name': 'Faculty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'eplace.generatelessonday': {
            'Meta': {'object_name': 'GenerateLessonDay'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Lesson']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'weak_days': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'eplace.group': {
            'Meta': {'ordering': "('faculty', '-start_year', 'title')", 'object_name': 'Group'},
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Faculty']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_year': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'eplace.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eplace.Group']", 'symmetrical': 'False'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Subject']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Teacher']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
            'week_days': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        'eplace.lessonday': {
            'Meta': {'ordering': "('date',)", 'unique_together': "(('date', 'lesson'),)", 'object_name': 'LessonDay'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Lesson']"})
        },
        'eplace.student': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'group'),)", 'object_name': 'Student'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'eplace.subject': {
            'Meta': {'object_name': 'Subject'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'eplace.superviser': {
            'Meta': {'object_name': 'Superviser'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['eplace.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'eplace.teacher': {
            'Meta': {'object_name': 'Teacher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'eplace.tick': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Tick'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ld': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.LessonDay']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Student']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['eplace']
