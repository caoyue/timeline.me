#!/bin/bash
# use gunicorn

killall gunicorn
sleep 2

cd /home/project/MyTimeline/timeline/
gunicorn -c gunicorn.conf timeline:application -D --error-logfile ./timeline_gunicorn.log
