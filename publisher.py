import paho.mqtt.client as mqtt
import time

def on_connect(client,userdata,flags,rc):
    print("connected with code :" + str(rc))
    client.subscribe("raspberry/topic")

def on_message(client,userdata,msg):
    print(str(msg.payload))




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)

for i in range(5):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('raspberry/topic', payload=i, qos=0, retain=False)
    print(f"send {i} to raspberry/topic")
    time.sleep(1)
client.loop_forever()