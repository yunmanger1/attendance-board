from django import forms
from django.conf import settings

from eplace.models import Group, Subject, LessonDay, GenerateLessonDay
from common.models import UserField 

class TickForm(forms.Form):
    teacher = None 
    
    def __init__(self, teacher, *a, **kw):
        super(TickForm, self).__init__(*a, **kw)
        self.teacher = teacher
        self.fields['group'].queryset = teacher.groups.all()
        self.fields['subject'].queryset = teacher.subjects.all()
        
    group   = forms.ModelChoiceField(queryset=Group.objects.none())
    subject = forms.ModelChoiceField(queryset=Subject.objects.none())
    tick    = forms.CharField()

class LessonDayForm(forms.ModelForm):
    
    class Meta:
        model = LessonDay
        exclude = ['teacher', 'subject', 'group']
        
    def save(self, teacher, subject, group): 
        o,c = LessonDay.objects.get_or_create(teacher=teacher, subject=subject, group=group, date=self.cleaned_data.get("date"))
        o.hours = self.cleaned_data.get("hours")
        o.save()
        return o
    
class GenerateLessonDayForm(forms.ModelForm):

    class Meta:
        model = GenerateLessonDay
        exclude = ['teacher', 'subject', 'group']
        
    def clean_weak_days(self):
        weak_days = self.cleaned_data.get('weak_days')
        t = weak_days.replace(' ','').split(',')
        for x in t:
            y = x.split(':')
            if y[0] not in ('mon','tue','wed','thu','fri','sat','sun'):
                raise forms.ValidationError("weak-day wrongly specified")
            try:
                k = int(y[1])
            except:
                raise forms.ValidationError("number of hours must be Integer")
        return weak_days

    def save(self, teacher, subject, group): 
        o = GenerateLessonDay(
            teacher=teacher, subject=subject, 
            group=group, 
            start_date=self.cleaned_data.get("start_date"),
            end_date=self.cleaned_data.get("end_date"),
            weak_days=self.cleaned_data.get("weak_days"),
        )
        o.save()
        
        
class SettingsForm(forms.Form):
    absence_percentage_limit = forms.IntegerField()
    
    def save(self, user, *a, **kw):
        o,c = UserField.objects.get_or_create(user=user, key="absence_percentage_limit")
        o.value = self.cleaned_data.get('absence_percentage_limit', settings.ABSENCE_PERCENTAGE_LIMIT)
        o.save()
        
def get_default_settings(request):
    try:
        o = UserField.objects.get(user=request.user, key="absence_percentage_limit")
        return {'absence_percentage_limit': o.value}
    except UserField.DoesNotExist:
        return {'absence_percentage_limit':settings.ABSENCE_PERCENTAGE_LIMIT}