import paho.mqtt.client as mqtt
import time
import Adafruit_DHT  

DHT11=Adafruit_DHT.DHT11  
our_payload = None

def sendtemp():
    global our_payload
    while True:
      humid,temp=Adafruit_DHT.read_retry(DHT11,4) # 4 is ithe GPIO number you can change this to your required need 
      our_payload = str(humid)+" "+str(temp)
      if(temp):
        client.publish('raspberry/temp_humid', payload=our_payload, qos=0, retain=False)
        break

def subscribe_to_broker(client,userdata,flags,rc):
    print("connected with code :" + str(rc))
    client.subscribe("raspberry/get_temp_humid")
    client.subscribe("raspberry/temp_humid")

def message_from_topic(client,userdata,msg):
    if(msg.topic =="raspberry/get_temp_humid"):
        sendtemp()
    time.sleep(10)

client = mqtt.Client()
client.on_connect = subscribe_to_broker
client.on_message = message_from_topic

client.connect("192.168.43.143",1883,60)

client.loop_forever()    