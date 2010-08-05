#!/bin/bash

. ./deploy/$1/dirs.cfg

uwsgi_cmd="$uwsgi_bin/uwsgi -s $socket -p 4 -M -t 20 -r -C -L -d ../wsgi_watchme.log wsgi"

case $2 in
"start")
$uwsgi_cmd
sudo $nginx_bin/nginx -c $nginx_conf
;;
"stop")
ps aux | grep '$uwsgi_cmd' | grep -v grep | awk '{system("kill -9 " $2)}'
sudo $nginx_bin/nginx -s stop -c $nginx_conf
;;
"restart")
bash $0 $1 stop
sleep 1
bash $0 $1 start
;;
*) echo "Usage: ./server.sh <config> {start|stop|restart}"
esac