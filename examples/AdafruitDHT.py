#!/usr/bin/env python3
import sys
import time
import http.client as http
import urllib
import json
import Adafruit_DHT
deviceId = "D7cVIIr2"
deviceKey = "C60DFhhj1ZHtr1aD"
def post_to_mcs(payload):
   headers = {"Content-type": "application/json", "deviceKey": deviceKey}
   not_connected = 1
   while (not_connected):
      try:
         conn = http.HTTPConnection("api.mediatek.com:80")
         conn.connect()
         not_connected = 0
      except (http.HTTPException, socket.error) as ex:
         print ("Error: %s" % ex)
         time.sleep(10)
   conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
   response = conn.getresponse()
   print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
   data = response.read()
   conn.close()

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

while True:
   if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
       sensor = sensor_args[sys.argv[1]]
       pin = sys.argv[2]
   else:
       print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
       print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connect')
       sys.exit(1)
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

   if humidity is not None and temperature is not None:
       print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
       payload = {"datapoints":[{"dataChnId":"Hum","values":{"value":humidity}},
                {"dataChnId":"Temp","values":{"value":temperature}}]}
       post_to_mcs(payload)
       time.sleep(1)
   else:
       print('Failed to get reading. Try again!')
       sys.exit(1)
