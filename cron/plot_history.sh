#!/bin/bash

#Plot weekley reports for all the sensors

cd /home/pi/Watering/cron/

python plot_plotly.py localhost root password arduino "select created,value from sensors where sensor=0 and date(created)>=curdate() - INTERVAL 7 DAY" week_temperature

python plot_plotly.py localhost root password arduino "select created,value from sensors where sensor=1 and date(created)>=curdate() - INTERVAL 7 DAY" week_moisture

python plot_plotly.py localhost root password arduino "select created,value from sensors where sensor=2 and date(created)>=curdate() - INTERVAL 7 DAY" week_light


#curl http://localhost:8080/plot/1/1/yesterday
#curl http://localhost:8080/plot/1/2/yesterday_light

#curl http://localhost:8080/plot/2/1/two_days_ago
#curl http://localhost:8080/plot/2/2/two_days_ago_light

