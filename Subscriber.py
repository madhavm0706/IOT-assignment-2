
#subscriber file
import paho.mqtt.client as mqtt
import joblib
import time
from struct import *
module  = joblib.load("mlmodule.pk1")

i=1

def send_waterflow(humidity,temp):
    waterflow = module.predict([[humidity,temp]])[0][0]
    print(waterflow)
    print(f"sending  predicted to publisher via topic raspberry/value1")
    client.publish('raspberry/value1', payload=float(waterflow), qos=0, retain=False)
    



def on_connect(client,userdata,flags,rc):
    print(f"connected with status code {rc}")
    client.subscribe("raspberry/value")
    client.subscribe("raspberry/value1")


def on_message(client,userdata, msg):
    
    print(f"{msg.payload}")
    
    
    if(msg.topic == "raspberry/value"):


        x = msg.payload.decode()
        our_payload = x.split(" ")

        print(f" temperature is {our_payload[1]}, and humidity is {our_payload[0]} ")
            
        send_waterflow(float(our_payload[0]),float(our_payload[1]))
        
    time.sleep(10)    
        
    

   

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.43.143",1883,60)

client.loop_forever()



