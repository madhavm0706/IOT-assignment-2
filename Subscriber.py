
#subscriber file
import paho.mqtt.client as mqtt
import joblib
import time
module  = joblib.load("mlmodule.pk1")

def on_connect(client,userdata,flags,rc):
    print(f"connected with status code {rc}")
    client.subscribe("raspberry/value")
    client.subscribe("raspberry/value1")


def on_message(client,userdata, msg):
    print(f"{msg.topic} {len(msg.payload)}")
    time.sleep(10)
    if(len(msg.payload)):
        print("hello")
        client.publish('raspberry/value1', payload="data from subscriber", qos=0, retain=False)


   

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.17.75.42",1883,60)

client.loop_forever()



