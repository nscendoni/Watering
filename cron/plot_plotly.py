#!/usr/bin/python

import plotly.plotly as py
import credentials
from plotly.graph_objs import *


py.sign_in(credentials.username, credentials.api_key)
from datetime import datetime
import sys
import MySQLdb

db = MySQLdb.connect(sys.argv[1], sys.argv[2], sys.argv[3],
                    sys.argv[4])

file_name=sys.argv[6]


cursor = db.cursor()

query = sys.argv[5]
cursor.execute(query)

result = cursor.fetchall()

t = []
s = []

for record in result:
  t.append(record[0])
  s.append(record[1])


data = Data([
    Scatter(
        x=t,
        y=s
    )
])

layout = Layout(
    title=file_name,
    xaxis=XAxis(
        title='Date',
        titlefont=Font(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=YAxis(
        title='Value',
        titlefont=Font(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = Figure(data=data, layout=layout)


print "saving file: " + file_name
#plot_url = py.plot(data, filename=file_name)
plot_url = py.plot(fig, filename=file_name)

#py.image.save_as({'data': data}, "/home/pi/Watering/static/images/"+file_name+".png")
py.image.save_as(fig, "/home/pi/Watering/static/images/"+file_name+".png")

