import paho.mqtt.client as mqtt
import time

import RPi.GPIO as GPIO
import time
 

import Adafruit_DHT  
DHT11=Adafruit_DHT.DHT11  # Adafruit_DHT.DHT22 for DHT22 sensor.

# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15
 
# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
  # Main program block
 
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable
 
  # Initialise display
  lcd_init()
 
  # Toggle backlight on-off-on
  lcd_backlight(True)
  time.sleep(0.5)
  lcd_backlight(False)
  time.sleep(0.5)
  lcd_backlight(True)
  time.sleep(0.5)
 
  while True:
 
    # Send some centred test
    lcd_string("--------------------",LCD_LINE_1,2)
    lcd_string("Rasbperry Pi",LCD_LINE_2,2)
    lcd_string("Model B",LCD_LINE_3,2)
    lcd_string("--------------------",LCD_LINE_4,2)
 
    time.sleep(3) # 3 second delay
 
    lcd_string("Raspberrypi-spy",LCD_LINE_1,3)
    lcd_string(".co.uk",LCD_LINE_2,3)
    lcd_string("",LCD_LINE_3,2)
    lcd_string("20x4 LCD Module Test",LCD_LINE_4,2)
 
    time.sleep(3) # 20 second delay
 
    # Blank display
    lcd_byte(0x01, LCD_CMD)
 
    time.sleep(3) # 3 second delay

    temp=0
    humid=0
    our_payload = None
    def sendtemp():
        global our_payload
        while True:
            temp,humid=Adafruit_DHT.read_retry(DHT11,4) # 4 is ithe GPIO number you can change this to your required need  
            our_payload = str(humid)+" "+str(temp)
            if(temp):

                client.publish('raspberry/value', payload=i, qos=0, retain=False)
                print("temp value send")
                break



    
 
    




    def on_connect(client,userdata,flags,rc):
        print("connected with code :" + str(rc))
        client.subscribe("raspberry/value")
        client.subscribe("raspberry/value1")

    def on_message(client,userdata,msg):
        if(msg.topic =="raspberry/value1"):
            water_flow = msg.payload
            print(f"{water_flow} received data from Subscriber via topic {msg.topic}")
            lcd_string("{msg.payload}",LCD_LINE_1,2)
            sendtemp()
        time.sleep(10)



    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost",1883,60)


    # a= ["50.2 88.4","51.2 83.4","60.2 78.4","55.2 68.4","10.2 18.4"]

    client.publish('raspberry/value', payload=temp, qos=0, retain=False)
    print(f"send data {temp} to Subscriber via topic raspberry/value")
    

    # for i in range(5):
    #     # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    #     client.publish('raspberry/value', payload=a[i], qos=0, retain=False)
    #     print(f"send {i} to raspberry/value")
    #     time.sleep(1)
    client.loop_forever()
    
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified
 
  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
def lcd_backlight(flag):
  # Toggle backlight on-off-on
  GPIO.output(LED_ON, flag)
 



if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()