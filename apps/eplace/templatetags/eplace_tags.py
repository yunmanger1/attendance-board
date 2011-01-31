import re
from django import template
from django.db import models
from django.db import connection
from django.utils import text
from django.conf import settings
from eplace.utils import is_dean as isdean, is_superviser as issuperviser, is_teacher as isteacher

import datetime 

#Post = models.get_model('jobapp','post')
register = template.Library()

def get_t(lesson, student):
    tick = None
    try:
        tick = lesson.tick_set.filter(student=student)[0]
    except IndexError:
        pass
    return tick

def ctv(val):
    for v, k, kk in settings.TICK_VALUES:
        if v == val:
            return k
        if v > 0:
            return '+'
    
def get_tick_d(lesson, student):
    tick = get_t(lesson, student)
    if tick is None:
        return '?'
    else:
        return ctv(tick.value)

@register.filter
def get_tick(lesson, student):
    return get_t(lesson, student)
get_tick.is_safe = True

@register.filter
def get_tick_display(lesson, student):
    return get_tick_d(lesson, student)
get_tick_display.is_safe = True

@register.filter
def is_teacher(user):
    return isteacher(user)
    
@register.filter    
def is_superviser(user):
    return issuperviser(user)

@register.filter
def is_dean(user):
    return isdean(user)

@register.filter
def get_absence_count(student, lesson):
    lessons = lesson.lessonday_set.all()
    count= 0
    for lessonday in lessons:
        if lessonday.is_absent(student):
            count += 1
    return count