import hashlib
import random
import time

from django.conf import settings
#from capi.models import ApiUser

#UserField = models.get_model('common','usermodel')


alfa = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def generate_sso_token(id, timestamp):
#    api_u = ApiUser.objects.get(user__pk=id)
    token = "%s%s%s" % (id, username, password)
    md5 = hashlib.md5()
    md5.update(token)
    return md5.hexdigest()


def gen_random_skey(n=512):
    k = len(alfa)
    return "".join([alfa[random.randint(0,k-1)] for i in xrange(0,n)])

def gen_url(user, url):
    t = time.time()
    token = generate_sso_token(user.pk, t)
    return "%s?id=%s&timestamp=%s&token=%s" %(url,user.pk,t,token)