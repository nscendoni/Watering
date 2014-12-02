#!/usr/bin/python


import web
import serial
import plotly.plotly as py
import sys
import basicauth
from threading import Lock

from plotly.graph_objs import *
from datetime import datetime


urls = (
    '/rest/(.*)/(.*)', 'digital',
    '/rest/(.*)', 'analogRead',
    '/temperature/(.*)', 'temperature',
    '/plot/(.*)/(.*)/(.*)', 'plot',
    '/report/(.*)/(.*)/(.*)/(.*)', 'report'
)

serial_port="/dev/ttyACM0"
try:
	ser = serial.Serial(serial_port, 9600, timeout=100)
except:
	serial_port="/dev/ttyACM1"
	ser = serial.Serial(serial_port, 9600, timeout=100)

def mutex_processor():
    mutex = Lock()

    def processor_func(handle):
        mutex.acquire()
        try:
            return handle()
        finally:
            mutex.release()
    return processor_func

def myVerifier(username, password, realm):
    return (username == "nicola" and password == "peperoncino123") \

app = web.application(urls, globals())
app.add_processor(mutex_processor())
db = web.database(dbn='mysql', user='root', pw='password', db='arduino')
auth = basicauth.auth(verify = myVerifier)


def sql_query(sql_query,name):
	t = []
	s = []

	#SQL Injection!! curdate()- INTERVAL 2 DAY
	results = db.select("sensors", where=sql_query, what="created,value").list()
	for record in results:
		t.append(record['created'])
		s.append(str(record['value']))

	data = Data([
		Scatter(
			x=t,
			y=s
		)
	])
	#print "saving file" + file_name
	plot_url = py.plot(data, filename=name)
	py.image.save_as({'data': data}, "/home/pi/Watering/static/images/"+name+".png")
	return "{\"filename\":\""+name+"\"}"

class digital:
	#value="on"|"off"
    def GET(self, pin,command):
	global ser
	global serial_port
	print("digital on called")
	try:
		ser.write("digital "+command+" "+pin+"/")
		line = ser.readline()
	except:
		if (serial_port=="/dev/ttyACM0"):
			serial_port="/dev/ttyACM1"
		else:
			serial_port="/dev/ttyACM0"
		ser = serial.Serial(serial_port, 9600, timeout=100)
		ser.write("digital "+value+" "+pin+"\n")
		line = ser.readline()
	return line

class analogRead:
    def GET(self, pin):
	global ser
	try:
		ser.write("analog read "+pin+"/")
		value = ser.readline()
	except:
		if (serial_port=="/dev/ttyACM0"):
			serial_port="/dev/ttyACM1"
		else:
			serial_port="/dev/ttyACM0"
		ser = serial.Serial(serial_port, 9600, timeout=100)
		value = ser.readline()

	print "analog value2="+value
	db.insert("sensors",value=int(value),sensor=pin)
	return "{\n \"pin\": "+pin+",\n \"value\": "+value+"\n}"


class temperature:
    
    def GET(self,pin):
	global ser
	global serial_port

	try:
		ser.write("temperature "+pin+"/")
		value = ser.readline()
	except:
		if (serial_port=="/dev/ttyACM0"):
			serial_port="/dev/ttyACM1"
		else:
			serial_port="/dev/ttyACM0"
		ser = serial.Serial(serial_port, 9600, timeout=100)
		ser.write("temperature\n")
		value = ser.readline()
	print "analog temp2="+value
	db.insert("sensors",value=int(value),sensor=pin)
	return "{\n \"temperature\": "+value+"}"

class plot:
	#value="on"|"off"

    def GET(self, interval,pin,name):
	py.sign_in("nscendoni", "jp1g307jcq")
	return sql_query("sensor="+pin+" and  date(created)=curdate() - INTERVAL "+interval+" DAY",name)

class report:
    def GET(self, start_date,end_date,pin,name):
	py.sign_in("nscendoni", "jp1g307jcq")
	return sql_query("sensor="+pin+" AND date(created)>=date('"+start_date+"') AND  date(created)<=date('"+end_date+"')",name)

if __name__ == "__main__":
    app.run()

