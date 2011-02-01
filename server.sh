#!/bin/bash

workon atboard
uwsgi_cmd="$uwsgi_bin/uwsgi -s $socket --env PYTHONPATH=$PYTHONPATH -p 4 -M -t 20 -r -C -L -d $log_dir/atboard.uwsgi.log -w wsgi"

case $2 in
"start")
if [ $1 != "workday" ]
then
$uwsgi_cmd
fi
;;
"stop")
if [ $1 != "workday" ]
then
ps aux | grep "$uwsgi_cmd" | grep -v grep | awk '{system("kill -9 " $2)}'
fi
;;
"restart")
bash $0 $1 stop
sleep 1
bash $0 $1 start
;;
*) echo "Usage: ./server.sh <config> {start|stop|restart}"
esac
