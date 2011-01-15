PATH=/usr/bin:/bin
DJANGO_HOME="/home/german/distr/django-trunk"
PROJECT_HOME="/home/german/work"
EXTRA_DIRS="$PROJECT_HOME/djangoejudge:$PROJECT_HOME/djangoejudge/apps:$PROJECT_HOME/djangoejudge/apps/zlibs"
EJUDGE_HOME="/home/ejudge/ejudge-2.3.16"
LOG_DIR=/home/german/tmp

pwd=$( readlink -f "$( dirname "$BASH_SOURCE" )" )
local_env=$pwd/env_local.sh
# echo $local_env

if [ -r $local_env ]
then
	. $local_env
fi

PYTHONPATH=$DJANGO_HOME:$PROJECT_HOME:$EXTRA_DIRS

export PYTHONPATH
