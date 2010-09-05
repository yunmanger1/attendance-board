from django import forms
from django.conf import settings

from eplace.models import Group, Subject, LessonDay, GenerateLessonDay, Lesson
from common.models import UserField 

class TickForm(forms.Form):
    teacher = None 
    
    def __init__(self, teacher, *a, **kw):
        super(TickForm, self).__init__(*a, **kw)
        self.teacher = teacher
        self.fields['lesson'].queryset = teacher.lesson_set.all()
        
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.none())
    tick    = forms.CharField()

class LessonDayForm(forms.ModelForm):
    
    class Meta:
        model = LessonDay
        exclude = ['lesson']
        
    def save(self, lesson): 
        o,c = LessonDay.objects.get_or_create(lesson=lesson, date=self.cleaned_data.get("date"))
        o.save()
        return o
    
class GenerateLessonDayForm(forms.ModelForm):

    class Meta:
        model = GenerateLessonDay
        exclude = ['lesson']
        
    def clean_weak_days(self):
        weak_days = self.cleaned_data.get('weak_days')
        t = weak_days.replace(' ','').split(',')
        for x in t:
            if x not in ('mon','tue','wed','thu','fri','sat','sun'):
                raise forms.ValidationError("weak-day wrongly specified")
        return weak_days

    def save(self, lesson): 
        o = GenerateLessonDay(
            lesson = lesson,
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