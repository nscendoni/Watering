#!/bin/bash

python /home/pi/Watering/plot_plotly.py localhost root password arduino "select created,value from sensors where sensor=1 and created like '$(date +%Y-%m-%d%)'" today
