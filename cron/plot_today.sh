#!/bin/bash

cd /home/pi/Watering/cron/

python plot_plotly.py localhost root password arduino "select created,value from sensors where sensor=1 and created > now() - INTERVAL 24 DAY_HOUR" today_moisture

python plot_plotly.py localhost root password arduino "select created,value from sensors where sensor=0 and created > now() - INTERVAL 24 DAY_HOUR" today_temperature

python plot_plotly.py localhost root password arduino "select created,value from sensors where sensor=2 and created > now() - INTERVAL 24 DAY_HOUR" today_light

#Plot watering
#curl http://localhost:8080/plot/0/1/today

#Plot Light
#curl http://localhost:8080/plot/0/2/light_today

