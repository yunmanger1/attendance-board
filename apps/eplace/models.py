from django.db import models
from django.contrib.auth.models import User, Group as UserGroup
from django.conf import settings

import datetime

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
        return u'{0}'.format(self.title)
    
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
        return u'{0} {1} course'.format(self.title, self.course())

class Student(models.Model):
    group           = models.ForeignKey(Group, blank=True, null=True)
    name            = models.CharField(max_length=50, blank=True)
    email           = models.EmailField(blank=True)
    info            = models.TextField(blank=True)
    
    @property
    def start_year(self):
        return self.group.start_year
    
    def __unicode__(self):
        return u'{0}'.format(self.name)
    
    @models.permalink
    def link(self):
        return ('eplace_students_student',None, {'id': self.pk})
    
    def subjects(self):
        return self.lessonday_set.only('subject').distinct('subject')
    
    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'group',)      


class Dean(models.Model):
    user            = models.OneToOneField(User)
    faculty         = models.ForeignKey(Faculty)
    
    class Meta:
        unique_together = ('user','faculty')
        
    def get_name(self):
        return self.user.username

    def save(self, *a, **kw):
        super(Dean, self).save(*a,**kw)
        group = UserGroup.objects.get(name=settings.DEANS_GROUP)
        self.user.groups.add(group)
        self.user.is_staff = True
        self.user.save()
        
    def delete(self, *a, **kw):
        group = UserGroup.objects.get(name=settings.DEANS_GROUP)
        self.user.groups.remove(group)
        self.user.save()
        super(Dean, self).delete(*a,**kw)
        
    def __unicode__(self):
        return '{0}'.format(self.get_name())
        
    
class Teacher(models.Model):
    user            = models.OneToOneField(User)
    subjects        = models.ManyToManyField(Subject, null=True, blank=True)
    groups          = models.ManyToManyField(Group, null=True, blank=True)
    
    def get_name(self):
        return self.user.username

    def save(self, *a, **kw):
        super(Teacher, self).save(*a,**kw)
        group = UserGroup.objects.get(name=settings.TEACHERS_GROUP)
        self.user.groups.add(group)
        self.user.is_staff = True
        self.user.save()
        
    def delete(self, *a, **kw):
        group = UserGroup.objects.get(name=settings.TEACHERS_GROUP)
        self.user.groups.remove(group)
        self.user.save()
        super(Teacher, self).delete(*a,**kw)

    def __unicode__(self):
        return u'{0}'.format(self.get_name())
    
class SubjectGroup(models.Model):
    subject = models.ForeignKey(Subject)
    group   = models.ForeignKey(Group)
    
class Superviser(models.Model):
    user            = models.OneToOneField(User)
    groups          = models.ManyToManyField(Group, null=True, blank=True)

    def get_name(self):
        return self.user.username

    def save(self, *a, **kw):
        super(Superviser, self).save(*a,**kw)
        group = UserGroup.objects.get(name=settings.SUPERVISERS_GROUP)
        self.user.groups.add(group)
        self.user.is_staff = True
        self.user.save()
        
    def delete(self, *a, **kw):
        group = UserGroup.objects.get(name=settings.SUPERVISERS_GROUP)
        self.user.groups.remove(group)
        self.user.save()
        super(Superviser, self).delete(*a,**kw)

    def __unicode__(self):
        return u'{0}'.format(self.get_name())


class LessonDay(models.Model):
    teacher         = models.ForeignKey(Teacher)
    subject         = models.ForeignKey(Subject)
    group           = models.ForeignKey(Group)
    date            = models.DateField()
    hours           = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('date', 'group', 'subject', 'teacher')
        ordering = ('date',)

    @models.permalink
    def del_link(self):
        return ('eplace_teacher_ld_delete', None, {'lid' : self.pk})
    
    def __unicode__(self):
        return u'{0} {1} {2}'.format(self.teacher, self.subject, self.group)
    
class Tick(models.Model):
    ld              = models.ForeignKey(LessonDay)
    student         = models.ForeignKey(Student)
    value           = models.IntegerField()
    pub_date        = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-pub_date',)
    
class GenerateLessonDay(models.Model):
    teacher         = models.ForeignKey(Teacher)
    subject         = models.ForeignKey(Subject)
    group           = models.ForeignKey(Group)
    start_date      = models.DateField()
    end_date        = models.DateField()
    weak_days       = models.CharField(max_length=50, help_text="Separate lesson-hours using comma (,). <br>Each lesson-hour is defined by (weekday):(hours). <br>Ex: mon:4, wed:2<br>Weekdays are defined by: mon, tue, wed, thu, fri, sat, sun")
    
    def save(self, *a, **kw):
        super(GenerateLessonDay, self).save(*a,**kw)
        #TODO: generate here
        t = self.weak_days.replace(' ','').split(',')
        d = {}
        for x in t:
            y = x.split(':')
            k = ['mon','tue','wed','thu','fri','sat','sun'].index(y[0])
            h = int(y[1])
            d.update({k:h})
        
        cur = self.start_date
        while cur < self.end_date:
            w = cur.weekday()
            if d.has_key(w):
                o, c = LessonDay.objects.get_or_create(
                     teacher=self.teacher,
                     subject=self.subject,
                     group=self.group,
                     date=cur
                )
                o.hours = d[w]
                o.save()
            cur = cur.fromtimestamp(int(cur.strftime("%s"))+24*60*60)
        super(GenerateLessonDay, self).delete(*a,**kw)
        
def is_teacher(user):
    if user.is_anonymous():
        return False
    t = Teacher.objects.filter(user=user)
    if (t.count() > 0):
        return True
    return False
    
def is_superviser(user):
    if user.is_anonymous():
        return False
    t = Superviser.objects.filter(user=user)
    if (t.count() > 0):
        return True
    return False

def is_dean(user):
    if user.is_anonymous():
        return False
    t = Dean.objects.filter(user=user)
    if (t.count() > 0):
        return True
    return False    