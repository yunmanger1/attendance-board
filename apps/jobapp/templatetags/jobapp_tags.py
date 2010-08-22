import re
from django import template
from django.db import models
from django.utils import text

import datetime 

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
def get_latest_ticks(job, date=None):
    if date is None:
        date = datetime.datetime.today().date()
    try:
        return job.dailyjobtick_set.published().filter(date__lte=date).order_by("-date")[:3]
    except:
        return ()
get_tick_for.is_safe = True

