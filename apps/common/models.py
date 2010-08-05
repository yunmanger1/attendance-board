from django.db import models
from django.contrib.auth.models import User

class UserField(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s:%s=%s' % (self.user.username, self.key, self.value)    