#!/usr/bin/python


import web
import serial
from threading import Lock


urls = (
    '/rest/(.*)/(.*)', 'digital',
    '/rest/(.*)', 'analogRead',
    '/temperature/(.*)', 'temperature'
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


app = web.application(urls, globals())
app.add_processor(mutex_processor())

db = web.database(dbn='mysql', user='root', pw='password', db='arduino')

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
	return "{\n pin: "+pin+",\n value: "+value+"\n}"

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
	return "{\n temperature: "+value+"}"

if __name__ == "__main__":
    app.run()

