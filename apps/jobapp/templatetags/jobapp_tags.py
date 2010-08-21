import re
from django import template
from django.db import models
from django.utils import text

#Post = models.get_model('jobapp','post')
register = template.Library()

@register.filter
def get_tick_for(job, date):
    try:
        return job.dailyjobtick_set.filter(date=date)[0]
    except:
        return None
get_tick_for.is_safe = True

@register.filter
def get_latest_ticks(job):
    try:
        return job.dailyjobtick_set.published().order_by("-date")[:3]
    except:
        return ()
get_tick_for.is_safe = True

