from django import forms

from jobapp.models import DailyJobTick, DailyJob

class DateForm(forms.Form):
    date = forms.DateField()

class DailyJobTickForm(forms.ModelForm):

    class Meta:
        exclude = ['job']
        model = DailyJobTick

    def save(self, job=None, *kw):
        if self.instance.pk:
            i = self.instance
            i.done = self.cleaned_data.get('done')
            i.date = self.cleaned_data.get('date')
            i.save()
        else:
            d = {
                 'job'     : job,
                 'done'    : self.cleaned_data.get('done'),
                 'date'     : self.cleaned_data.get('date'),
            }
            try:
                i = DailyJobTick.objects.get(job=job, date=self.cleaned_data.get('date'))
                i.done = self.cleaned_data.get('done')
            except DailyJobTick.DoesNotExist:
                i = DailyJobTick(**d)
            i.save()
        return i

class DailyJobForm(forms.ModelForm):
    
    class Meta:
        exclude = ['user', 'is_on', 'importance']
        model = DailyJob
        
    def save(self, user=None, *kw):
        if self.instance.pk:
            i = self.instance
            i.title = self.cleaned_data.get('title','no title')
            i.text = self.cleaned_data.get('text','no text')
            i.n = self.cleaned_data.get('n',1)
            i.save()
        else:
            d = {
                 'user'     : user,
                 'title'    : self.cleaned_data.get('title','no title'),
                 'text'     : self.cleaned_data.get('text','no text'),
                 'n'        : self.cleaned_data.get('n',1),
            }             
            i = DailyJob(**d)
            i.save()
        return i
            