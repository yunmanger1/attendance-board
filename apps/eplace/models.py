from django.db import models
from django.contrib.auth.models import User, Group as UserGroup
from django.conf import settings

import datetime, logging

log = logging.getLogger('eplace')

class Subject(models.Model):
    short_name      = models.CharField(max_length=10)
    full_name       = models.CharField(max_length=100)
    
    def __unicode__(self):
        return u'{0}'.format(self.full_name)

class Faculty(models.Model):
    title           = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'faculty'
        verbose_name_plural = 'faculties'
    
    def __unicode__(self):
        return self.title
    
class Group(models.Model):
    faculty         = models.ForeignKey(Faculty)
    title           = models.CharField(max_length=10)
    start_year      = models.IntegerField()
#    faculty         = models.CharField(max_length=50)

    class Meta:
        ordering = ('faculty', '-start_year', 'title')

#    @property
    def course(self):
        date = datetime.datetime.today().date()
        year = date.year
        if (date.month < 9):
            year-=1
        return year - self.start_year+ 1
        

    def __unicode__(self):
        return '{0} {1} course'.format(self.title, self.course())

class Student(models.Model):
    group           = models.ForeignKey(Group, blank=True, null=True)
    name            = models.CharField(max_length=50, blank=True)
    email           = models.EmailField(null=True, blank=True)
    info            = models.TextField(null=True, blank=True)
    
    @property
    def start_year(self):
        return self.group.start_year
    
    def __unicode__(self):
        return '{0}'.format(self.name)
    
    def fromString(self, line):
        t = line.split(';')
        n = len(t)
        if n > 0:
            self.name = t[0].strip()
        if n > 1:
            self.email = t[1].strip()
        if n > 2:
            self.info = t[2].strip()
#        if n > 3:
#            self.info = t[3].strip()
            
    
    @models.permalink
    def link(self):
        return ('eplace_students_student',None, {'id': self.pk})
    
    def subjects(self):
        return self.lessonday_set.only('subject').distinct('subject')
    
    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'group',)      

#====================================================

class Dean(models.Model):
    user            = models.OneToOneField(User)
    faculty         = models.ForeignKey(Faculty)
    
    class Meta:
        unique_together = ('user','faculty')
        
    def get_name(self):
        return self.user.username

        
    def __unicode__(self):
        return '{0}'.format(self.get_name())
    
class Teacher(models.Model):
    user            = models.OneToOneField(User)
    
    def get_name(self):
        return self.user.username

    def __unicode__(self):
        return '{0}'.format(self.get_name())
    
class Superviser(models.Model):
    user            = models.OneToOneField(User)
    groups          = models.ManyToManyField(Group, null=True, blank=True)
    
    def get_name(self):
        return self.user.username

    def __unicode__(self):
        return '{0}'.format(self.get_name())

#===========================================================    

class Lesson(models.Model):
    teacher         = models.ForeignKey(Teacher)
    subject         = models.ForeignKey(Subject)
    groups          = models.ManyToManyField(Group)
    hours           = models.IntegerField(default=1)
    week_days       = models.CharField(max_length=30, default='')
    type            = models.CharField(max_length=15, default='')
    
    def short_name(self):
        return self.subject.short_name
    
    @models.permalink
    def link(self):
        return ('eplace_students_lesson', None, {'id': self.pk})
    
    
    def __unicode__(self):
        if self.type != '':
            return u'{0} {1} {2}'.format(self.teacher, self.subject, self.type)
        else:
            return u'{0} {1}'.format(self.teacher, self.subject)
        

class LessonDay(models.Model):
    lesson          = models.ForeignKey(Lesson)
    date            = models.DateField()
    
    class Meta:
        unique_together = ('date', 'lesson')
        ordering = ('date',)
        
    
    def is_absent(self, student):
        ticks = Tick.objects.filter(ld=self, student=student)
        n = ticks.count()
        if n > 0:
            tick = ticks[0]
            if tick.value == 0:
                return True
        return False
                    

    @models.permalink
    def del_link(self):
        return ('eplace_teacher_ld_delete', None, {'lid' : self.pk})
    
    def __unicode__(self):
        return '{0} {1} {2}'.format(self.teacher, self.subject, self.group)
    
class Tick(models.Model):
    ld              = models.ForeignKey(LessonDay)
    student         = models.ForeignKey(Student)
    value           = models.IntegerField()
    pub_date        = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-pub_date',)
    
class GenerateLessonDay(models.Model):
    lesson          = models.ForeignKey(Lesson)
    start_date      = models.DateField()
    end_date        = models.DateField()
    weak_days       = models.CharField(max_length=50, help_text="Separate lesson-days using comma (,). <br>Ex: mon, wed<br>Weekdays are defined by: mon, tue, wed, thu, fri, sat, sun")
    
    def save(self, *a, **kw):
        super(GenerateLessonDay, self).save(*a,**kw)
        #TODO: generate here
        t = self.weak_days.replace(' ','').split(',')
        d = {}
        for x in t:
            k = ['mon','tue','wed','thu','fri','sat','sun'].index(x)
            d.update({k:self.lesson.hours})
        
        cur = self.start_date
        while cur < self.end_date:
            w = cur.weekday()
            if d.has_key(w):
                o, c = LessonDay.objects.get_or_create(
                     lesson=self.lesson,
                     date=cur
                )
                o.save()
            cur = cur.fromtimestamp(int(cur.strftime("%s"))+24*60*60)
        super(GenerateLessonDay, self).delete(*a,**kw)



class EplaceUser(User):
    
    class Meta:
        proxy = True

    def is_teacher(self):
        try:
            Teacher.objects.get(user=self)
            return True
        except Teacher.DoesNotExist:
            return False
        
    def is_superviser(self):
        try:
            Superviser.objects.get(user=self)
            return True
        except Superviser.DoesNotExist:
            return False
        
    def make_teacher(self):
        Teacher.objects.get_or_create(user=self)

    def make_superviser(self):
        Superviser.objects.get_or_create(user=self)
        
        
class CopyPasteStudents(models.Model):
    group           = models.ForeignKey(Group)
    text            = models.TextField()
    
    def save(self, *a, **kw):
        super(CopyPasteStudents, self).save(*a,**kw)
        list = self.text.split('\n')
        for line in list:
            if line == '':
                continue
            s = Student(group=self.group)
            s.fromString(line)
            try:
                ns = Student.objects.get(name=s.name)
            except Student.DoesNotExist:
                s.save()                
        super(CopyPasteStudents, self).delete(*a,**kw)
