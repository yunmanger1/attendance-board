#!/bin/bash
name=atboard
pwd=$( readlink -f "$( dirname "$BASH_SOURCE" )" )

PYTHONPATH=$PYTHONPATH:$pwd/apps:/opt/envs/$name/lib/python2.5/site-packages
echo $PYTHONPATH

nginx=/opt/nginx
uwsgi_bin=$nginx/sbin
socket=$nginx/sock/$name.$1.sock
nginx_vhosts=$nginx/vhosts
log_dir=$nginx/logs

uwsgi_cmd="$uwsgi_bin/uwsgi -s  --env PYTHONPATH=$PYTHONPATH -p 4 -M -t 20 -r -C -L -d $log_dir/wsgi_$name.log -w wsgi"

procid=$(ps -ef|grep "nginx: master process" | grep -v grep | awk '{print $2}')

case $2 in
"start")
bash $0 $1 deploy
if [ $1 != "workday" ]
then
$uwsgi_cmd
fi
kill -HUP $procid
;;
"stop")
bash $0 $1 undeploy
if [ $1 != "workday" ]
then
ps aux | grep "$uwsgi_cmd" | grep -v grep | awk '{system("kill -9 " $2)}'
fi
kill -HUP $procid
;;
"restart")
bash $0 $1 stop
sleep 1
bash $0 $1 start
;;
"deploy")
cp $pwd/deploy/$1/nginx.conf $nginx_vhosts/$name.kz.conf
;;
"undeploy")
rm $nginx_vhosts/$name.kz.conf
;;
*) echo "Usage: ./server.sh <config> {start|stop|restart}"
esac