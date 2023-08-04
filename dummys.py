import paho.mqtt.client as mqtt


def send_request():
    client.publish("raspberry/get_temp_humid",payload="request for temp", qos=0,retain= False)


def subscribe_to_broker(client,userdata,flags,rc):
    print(f"connection sucessfully established {rc}")
    client.subscribe("raspberry/temp_humid")
    client.subscribe("raspberry/get_temp_humid")


def message_from_topic(client,userdata, msg):
    if(msg.topic == "raspberry/temp_humid"):
        print({msg.payload})



client = mqtt.Client() 
client.on_connect = subscribe_to_broker 
client.on_message = message_from_topic 
# client.username_pw_set("madhavm0706", password="@1Dec97")
client.connect("broker.hivemq.com",1883,60) #connecting the subscriber to the Broker.
send_request()
client.loop_forever()

