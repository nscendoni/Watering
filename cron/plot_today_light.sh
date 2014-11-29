#!/bin/bash

python /home/nicola/Irrigazione/plot_plotly.py localhost root password arduino "select created,value from sensors where sensor=2 and created like '$(date +%Y-%m-%d%)'" light_today
