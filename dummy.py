import paho.mqtt.client as mqtt
import time

data = None
def send_tem_humid():
    global data
    temp = float(input("Enter temperature value"))
    humid = float(input("Enter humidity value"))
    
    data = str(temp)+" "+str(humid)
    


def subscribe_to_broker(client,userdata,flags,rc):
    print(f"connection sucessfully established {rc}")
    client.subscribe("raspberry/temp_humid")
    client.subscribe("raspberry/get_temp_humid")
    send_tem_humid()


def message_from_topic(client,userdata, msg):
    
    if(msg.topic == "raspberry/get_temp_humid"):
        global data
        print({msg.payload})
        send_tem_humid()
        
        client.publish("raspberry/temp_humid", payload=data, qos=0, retain=False)
       


client = mqtt.Client() 
client.on_connect = subscribe_to_broker 
client.on_message = message_from_topic 

client.connect("broker.hivemq.com",1883,60) #connecting the subscriber to the Broker.

# send_tem_humid()

client.loop_forever()

