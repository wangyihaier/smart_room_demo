from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from Adafruit_BME280 import *
import RPi.GPIO as GPIO
import time
import sqlite3



#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

e = create_engine('sqlite:///salaries.db')
d = create_engine('sqlite:///sensors.db')

app = Flask(__name__)
api = Api(app)

LED = 26


class Led_State(Resource):
    def get(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #GPIO.setup(LED, GPIO.IN)
        return {'LedState': GPIO.input(LED)}

class Led_Switch(Resource):
    def get(self, state):

            action = -1
            state = int(state)

           
            # -1 = do nothing
            # 0 = off the led
            # 1 = on the led
            # 3 = no action needed as the led already on or off
            
            #Find out the sate in DB
            #dbState = state
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()
            c.execute("SELECT state FROM gpios WHERE gpioid ={gpioid}".\
            format(gpioid=LED))
            id_exists = c.fetchone()
            print id_exists
            if id_exists:
                dbState = id_exists[0]
                print 'DBState:{}'.format(dbState)
            else:
                dbState = state
                print 'insert record'
                c.execute("INSERT INTO gpios (gpioid, state) VALUES({gpioid}, {s})"\
             .format(gpioid=LED, s=state))

            
            #Find out current led state
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(LED, GPIO.OUT)
            currentState = GPIO.input(LED)
            print 'currentState:{}'.format(currentState)

            
            if state == currentState:
                    action = 3
            else:
                    action = state
                    GPIO.output(LED, state)
                    c.execute("UPDATE gpios SET state = ({sv}) WHERE gpioid=({gpioid})".\
                        format(sv=state, gpioid=LED))
            
            conn.commit()
            conn.close()

            if action>3:
                action = 3
        
            return {'Action': action}



class RME280_Data(Resource):
    def get(self):
        #Connect to databse
        #conn = e.connect()
        #Perform query and return JSON data
        #query = conn.execute("select distinct DEPARTMENT from salaries")
        #return {'departments': [i[0] for i in query.cursor.fetchall()]}
        
        sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
        return {'sensor': {'Temp': '{0:0.3f} deg C'.format(sensor.read_temperature()), 'Pressure': '{0:0.2f} hPa'.format(sensor.read_pressure()), 'Humidity': '{0:0.2f} %'.format(sensor.read_humidity())}}

class Departments_Meta(Resource):
    def get(self):
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select distinct DEPARTMENT from salaries")
        return {'departments': [i[0] for i in query.cursor.fetchall()]}
        #return {'sensor': {'Temp': '{0:0.3f} deg C'.format(sensor.read_temperature()), 'Pressure': '{0:0.2f} hPa'.format(sensor.read_pressure()), 'Humidity': '{0:0.2f} %'.format(sensor.read_humidity())}}

class Departmental_Salary(Resource):
    def get(self, department_name):
        conn = e.connect()
        query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
    
 
api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/departments')
api.add_resource(RME280_Data, '/rme280')
api.add_resource(Led_State, '/ledstate')
api.add_resource(Led_Switch, '/action/<state>')

if __name__ == '__main__':
     app.run(host='0.0.0.0')
