#!/bin/bash

. ./deploy/$1/dirs.cfg

case $2 in
"start")
$uwsgi_bin/uwsgi -s $socket -p 4 -M -t 20 -r -C -L -d ../wsgi.log wsgi
sudo $nginx_bin/nginx -c $nginx_conf
;;
"stop")
killall -9 uwsgi
sudo $nginx_bin/nginx -s stop -c $nginx_conf
;;
"restart")
bash $0 $1 stop
sleep 1
bash $0 $1 start
;;
*) echo "Usage: ./server.sh <config> {start|stop|restart}"
esac