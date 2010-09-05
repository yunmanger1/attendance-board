# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Subject'
        db.create_table('eplace_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('eplace', ['Subject'])

        # Adding model 'Faculty'
        db.create_table('eplace_faculty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('eplace', ['Faculty'])

        # Adding model 'Group'
        db.create_table('eplace_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('faculty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.Faculty'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start_year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('eplace', ['Group'])

        # Adding model 'Student'
        db.create_table('eplace_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.Group'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('eplace', ['Student'])

        # Adding unique constraint on 'Student', fields ['name', 'group']
        db.create_unique('eplace_student', ['name', 'group_id'])

        # Adding model 'Dean'
        db.create_table('eplace_dean', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('faculty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.Faculty'])),
        ))
        db.send_create_signal('eplace', ['Dean'])

        # Adding unique constraint on 'Dean', fields ['user', 'faculty']
        db.create_unique('eplace_dean', ['user_id', 'faculty_id'])

        # Adding model 'Teacher'
        db.create_table('eplace_teacher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('eplace', ['Teacher'])

        # Adding model 'Lesson'
        db.create_table('eplace_lesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.Teacher'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.Subject'])),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('week_days', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(default='', max_length=15)),
        ))
        db.send_create_signal('eplace', ['Lesson'])

        # Adding M2M table for field groups on 'Lesson'
        db.create_table('eplace_lesson_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['eplace.lesson'], null=False)),
            ('group', models.ForeignKey(orm['eplace.group'], null=False))
        ))
        db.create_unique('eplace_lesson_groups', ['lesson_id', 'group_id'])

        # Adding model 'Superviser'
        db.create_table('eplace_superviser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('eplace', ['Superviser'])

        # Adding M2M table for field groups on 'Superviser'
        db.create_table('eplace_superviser_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('superviser', models.ForeignKey(orm['eplace.superviser'], null=False)),
            ('group', models.ForeignKey(orm['eplace.group'], null=False))
        ))
        db.create_unique('eplace_superviser_groups', ['superviser_id', 'group_id'])

        # Adding model 'LessonDay'
        db.create_table('eplace_lessonday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.Lesson'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('eplace', ['LessonDay'])

        # Adding unique constraint on 'LessonDay', fields ['date', 'lesson']
        db.create_unique('eplace_lessonday', ['date', 'lesson_id'])

        # Adding model 'Tick'
        db.create_table('eplace_tick', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ld', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.LessonDay'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.Student'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('eplace', ['Tick'])

        # Adding model 'GenerateLessonDay'
        db.create_table('eplace_generatelessonday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eplace.Lesson'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('weak_days', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('eplace', ['GenerateLessonDay'])


    def backwards(self, orm):
        
        # Deleting model 'Subject'
        db.delete_table('eplace_subject')

        # Deleting model 'Faculty'
        db.delete_table('eplace_faculty')

        # Deleting model 'Group'
        db.delete_table('eplace_group')

        # Deleting model 'Student'
        db.delete_table('eplace_student')

        # Removing unique constraint on 'Student', fields ['name', 'group']
        db.delete_unique('eplace_student', ['name', 'group_id'])

        # Deleting model 'Dean'
        db.delete_table('eplace_dean')

        # Removing unique constraint on 'Dean', fields ['user', 'faculty']
        db.delete_unique('eplace_dean', ['user_id', 'faculty_id'])

        # Deleting model 'Teacher'
        db.delete_table('eplace_teacher')

        # Deleting model 'Lesson'
        db.delete_table('eplace_lesson')

        # Removing M2M table for field groups on 'Lesson'
        db.delete_table('eplace_lesson_groups')

        # Deleting model 'Superviser'
        db.delete_table('eplace_superviser')

        # Removing M2M table for field groups on 'Superviser'
        db.delete_table('eplace_superviser_groups')

        # Deleting model 'LessonDay'
        db.delete_table('eplace_lessonday')

        # Removing unique constraint on 'LessonDay', fields ['date', 'lesson']
        db.delete_unique('eplace_lessonday', ['date', 'lesson_id'])

        # Deleting model 'Tick'
        db.delete_table('eplace_tick')

        # Deleting model 'GenerateLessonDay'
        db.delete_table('eplace_generatelessonday')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'Meta': {'object_name': 'Group'},
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
            'Meta': {'unique_together': "(('date', 'lesson'),)", 'object_name': 'LessonDay'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Lesson']"})
        },
        'eplace.student': {
            'Meta': {'unique_together': "(('name', 'group'),)", 'object_name': 'Student'},
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
            'Meta': {'object_name': 'Tick'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ld': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.LessonDay']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eplace.Student']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['eplace']
