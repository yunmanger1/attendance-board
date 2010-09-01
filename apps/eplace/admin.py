from django.contrib import admin
from django import forms
from django.forms.formsets import formset_factory
from eplace.models import Faculty, Group, Student, Subject, Superviser, Teacher
from eplace.models import Dean, GenerateLessonDay, LessonDay

#class PostAdmin(admin.ModelAdmin):
#    list_display  = ('title', 'pub_date')
#    list_filter   = ('pub_date', 'category')
#    search_fields = ('title', 'text')
#    prepopulated_fields = {'slug': ('title',)}

class GroupInline(admin.TabularInline):
    model = Group
    extra = 3
    
class StudentInline(admin.TabularInline):
    model = Student
    extra = 3

class FacultyAdmin(admin.ModelAdmin):
    inlines = [GroupInline]
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_year','course')
    list_filter = ('start_year', 'title',)
    search_fields = ('title','start_year',)
    inlines = [StudentInline]    

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'start_year')
    list_filter = ( 'name', 'group')
    search_fields = ('name','group__start_year', 'group__title', 'group__faculty__title')
    
#class SubjectForm(forms.ModelForm):
#    
#    class Meta: 
#        model = Subject
#        
#SubjectsForm = formset_factory(SubjectForm, extra=4, can_delete=True) 
#        
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name',)
    list_filter = ('full_name', 'short_name',)
    search_fields = ('full_name', 'short_name',)

class DeanAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'user', 'faculty',)
    list_filter = ('user', 'faculty',)
    
class GenerateLessonDayAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button
    
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Superviser)
admin.site.register(Teacher)
admin.site.register(Dean, DeanAdmin)
admin.site.register(GenerateLessonDay, GenerateLessonDayAdmin)
admin.site.register(LessonDay)
