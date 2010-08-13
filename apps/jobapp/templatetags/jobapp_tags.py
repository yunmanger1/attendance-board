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