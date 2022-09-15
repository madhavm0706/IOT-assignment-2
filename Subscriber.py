
#importing all the packages required in our project
import paho.mqtt.client as mqtt
import joblib
import time
from model import waterflow_prediction

module  = joblib.load("waterflowrate.pk1") #importing our ML Module

#function to send water flow rate To Publisher
def send_waterflow_predict(humidity,temp):
    waterflow_rate = module.prediction(humidity,temp)
    print(f"sending predicted waterflow")
    client.publish('raspberry/waterflow_rate', payload=float(waterflow_rate), qos=0, retain=False)

#function to subscribe the topics    
def subscribe_to_broker(client,userdata,flags,rc):
    print(f"connection sucessfully established {rc}")
    client.subscribe("raspberry/temp_humid")
    client.subscribe("raspberry/waterflow_rate")


#function to check messages from the Topic
def message_from_topic(client,userdata, msg):
    if(msg.topic == "raspberry/temp_humid"):
        x = msg.payload.decode()
        our_payload = x.split(" ")
        print(f" temperature -- {our_payload[1]},humidity -- {our_payload[0]} ")
        send_waterflow_predict(float(our_payload[0]),float(our_payload[1]))
    time.sleep(10)    
        
    

   

client = mqtt.Client() 
client.on_connect = subscribe_to_broker 
client.on_message = message_from_topic 

client.connect("192.168.43.143",1883,60) #connecting the subscriber to the Broker.

client.loop_forever() #will check the topics value by running client module regularly.



