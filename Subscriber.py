
#subscriber file
import paho.mqtt.client as mqtt
import joblib
import time
module  = joblib.load("mlmodule.pk1")

i=1

def on_connect(client,userdata,flags,rc):
    print(f"connected with status code {rc}")
    client.subscribe("raspberry/value")
    client.subscribe("raspberry/value1")


def on_message(client,userdata, msg):
    global i
    print(f" received data {msg.payload} from publisher via topic {msg.topic} ")
    
    
    print(f"sending  data {i} to publisher via topic raspberry/value1")
    client.publish('raspberry/value1', payload=i, qos=0, retain=False)
    i = i+1
    time.sleep(30)

   

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.17.75.42",1883,60)

client.loop_forever()



