
#importing all the packages required in our project
import paho.mqtt.client as mqtt
import time
from model import waterflow_prediction

def request_temp_humid():
    client.publish('raspberry/get_temp_humid',payload="generate",qos=0,retain= False) 

def subscribe_to_broker(client,userdata,flags,rc):
    print(f"connection sucessfully established {rc}")
    client.subscribe("raspberry/temp_humid")
    client.subscribe("raspberry/get_temp_humid")
    request_temp_humid()

#function to check messages from the Topic
def message_from_topic(client,userdata, msg):
    if(msg.topic == "raspberry/temp_humid"):
        print(msg.payload)
        
        
    

   

client = mqtt.Client() 
client.on_connect = subscribe_to_broker 
client.on_message = message_from_topic 

client.connect("172.27.19.27",1883,60) #connecting the subscriber to the Broker.

client.loop_forever() #will check the topics value by running client module regularly.



