from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
import django
import os

_ = os.system

PROJECT_ROOT = settings.PROJECT_ROOT
def rel(*x):
    return os.path.join(PROJECT_ROOT, *x)

DJANGO_ROOT = os.path.abspath(os.path.dirname(django.__file__))
ADMIN_MEDIA = os.path.join(DJANGO_ROOT, "contrib","admin","media")
project_name=os.path.basename(PROJECT_ROOT)
MEDIA_ROOT = rel("..","..","media",project_name)
#WORK_ROOT = rel("..","..")
#DEPLOY_ROOT = os.path.join(WORK_ROOT,"projects",project_name)

def deploy_media(conf):
    if not os.path.exists(MEDIA_ROOT):
        os.mkdir(MEDIA_ROOT)
    if os.path.exists(os.path.join(MEDIA_ROOT,"admin")):
        _("rm {0}".format(os.path.join(MEDIA_ROOT,"admin")))
    _("ln -s {0} {1}".format(ADMIN_MEDIA, os.path.join(MEDIA_ROOT,"admin")))
    if os.path.exists(os.path.join(MEDIA_ROOT,"static_media")):
        _("rm {0}".format(os.path.join(MEDIA_ROOT,"static_media")))
    _("ln -s {0} {1}".format(os.path.join(PROJECT_ROOT,"media","static_media"), os.path.join(MEDIA_ROOT,"static_media")))
    

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--conf', '-c', default='prod', dest='conf',
            help='Deploy configuration'),
    )
    help = ""

    def handle(self, *args, **options):
        conf = options.get('conf')
#        _("bash {0}/bin/copy-project.sh {1}".format(WORK_ROOT, project_name))
        if os.path.exists("etc"):
            _("rm etc")
        _("ln -s etcs/{0} etc".format(conf))
        deploy_media(conf)

