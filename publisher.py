import paho.mqtt.client as mqtt
import time




def on_connect(client,userdata,flags,rc):
    print("connected with code :" + str(rc))
    client.subscribe("raspberry/value")
    client.subscribe("raspberry/value1")

def on_message(client,userdata,msg):
    print(f"{msg.topic}{msg.payload}")
    time.sleep(10)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)


a= ["50.2 88.4","51.2 83.4","60.2 78.4","55.2 68.4","10.2 18.4"]
client.publish('raspberry/value', payload=a[0], qos=0, retain=False)
print(f"send 1 to raspberry/value")


# for i in range(5):
#     # the four parameters are topic, sending content, QoS and whether retaining the message respectively
#     client.publish('raspberry/value', payload=a[i], qos=0, retain=False)
#     print(f"send {i} to raspberry/value")
#     time.sleep(1)
client.loop_forever()

