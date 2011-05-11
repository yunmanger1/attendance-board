from django.contrib import admin
from django import forms
from django.forms.formsets import formset_factory
from eplace.models import Faculty, Group, Student, Subject, Superviser, Teacher,\
    CopyPasteStudents, EplaceUser
from eplace.models import Dean, GenerateLessonDay, LessonDay, Lesson
from eplace.forms import CopyPasteStudentsForm
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

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
    extra = 0
    
class CopyPasteStudentsInline(admin.TabularInline):
    model = CopyPasteStudents
    form = CopyPasteStudentsForm
    extra = 1

class FacultyAdmin(admin.ModelAdmin):
    inlines = [GroupInline]
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_year','course')
    list_filter = ('start_year', 'title',)
    search_fields = ('title','start_year',)
    inlines = [CopyPasteStudentsInline, StudentInline]    

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'start_year')
    list_filter = ( 'name', 'group')
    search_fields = ('name','group__start_year', 'group__title', 'group__faculty__title')
    
def make_teacher(self, request, queryset):
    for user in queryset:
        user.make_teacher()
make_teacher.short_description = "Make selected users - teacher"

def make_superviser(self, request, queryset):
    for user in queryset:
        user.make_superviser()
make_superviser.short_description = "Make selected users - superviser"

#add_view = UserAdmin.add_view
#change_view = UserAdmin.change_view
#delete_view = UserAdmin.delete_view

class EplaceUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_teacher','is_superviser')
    #list_filter = ('username', 'title',)
    search_fields = ('username','first_name','last_name')
    inlines = [CopyPasteStudentsInline, StudentInline]
    actions = [make_teacher, make_superviser]
    
    def has_add_permission(self, *args, **kwargs):
        return False
    
    def has_delete_permission(self, *args, **kwargs):
        return False
    
    def change_view(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    
    
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
    

class CopyPasteStudentsAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Superviser)
admin.site.register(EplaceUser, EplaceUserAdmin)
#admin.site.register(Teacher)
admin.site.register(Dean, DeanAdmin)
#admin.site.register(LessonDay)
admin.site.register(Lesson)

admin.site.register(CopyPasteStudents, CopyPasteStudentsAdmin)    
admin.site.register(GenerateLessonDay, GenerateLessonDayAdmin)


