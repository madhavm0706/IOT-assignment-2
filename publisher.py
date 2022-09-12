import paho.mqtt.client as mqtt
import time

import Adafruit_DHT  
DHT11=Adafruit_DHT.DHT11  # Adafruit_DHT.DHT22 for DHT22 sensor.

temp=0
humid=0
while True:

    temp,humid=Adafruit_DHT.read_retry(DHT11,4) # 4 is ithe GPIO number you can change this to your required need  
    if(temp):
        break 
 

i=1
def senddata(a):
    global i
    client.publish('raspberry/value', payload=i, qos=0, retain=False)
    print(f"{a}send data to Subscriber via topic raspberry/value")
    i =i+1




def on_connect(client,userdata,flags,rc):
    print("connected with code :" + str(rc))
    client.subscribe("raspberry/value")
    client.subscribe("raspberry/value1")

def on_message(client,userdata,msg):
    global i
    print(f"{msg.payload} received data from Subscriber via topic {msg.topic}")
    senddata(i)
   



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)


# a= ["50.2 88.4","51.2 83.4","60.2 78.4","55.2 68.4","10.2 18.4"]

client.publish('raspberry/value', payload=temp, qos=0, retain=False)
print(f"send data {temp} to Subscriber via topic raspberry/value")
i = i+1

# for i in range(5):
#     # the four parameters are topic, sending content, QoS and whether retaining the message respectively
#     client.publish('raspberry/value', payload=a[i], qos=0, retain=False)
#     print(f"send {i} to raspberry/value")
#     time.sleep(1)
client.loop_forever()

