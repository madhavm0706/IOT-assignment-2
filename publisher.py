#importing all the required packages
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import Adafruit_DHT  

DHT11=Adafruit_DHT.DHT11  

# GPIO to LCD mapping
RS = 26
E  = 19
D4 = 13
D5 = 6
D6 = 5
D7 = 11
ON = 15
 
#LCD constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LINE_1 = 0x80 #  RAM address of the 1st line
LINE_2 = 0xC0 #  RAM address of the 2nd line
LINE_3 = 0x94 #  RAM address of the 3rd line
LINE_4 = 0xD4 #  RAM address of the 4th line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


def main():
  
 
  GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
  GPIO.setup(E, GPIO.OUT)  # E
  GPIO.setup(RS, GPIO.OUT) # RS
  GPIO.setup(D4, GPIO.OUT) # DB4
  GPIO.setup(D5, GPIO.OUT) # DB5
  GPIO.setup(D6, GPIO.OUT) # DB6
  GPIO.setup(D7, GPIO.OUT) # DB7
  GPIO.setup(ON, GPIO.OUT) #enable backlight
 
  #calling function to initialize lcd
  lcd_init()
  display_message("Farm Irrigation System ",LINE_1,1)
  display_message("By Team Protocols ",LINE_2,2)

  temp=0
  humid=0
  our_payload = None
  def sendtemp():
    global our_payload
    while True:

      humid,temp=Adafruit_DHT.read_retry(DHT11,4) # 4 is ithe GPIO number you can change this to your required need 
      lcd_backlight(True)
      time.sleep(0.5)
      lcd_backlight(False) 
      our_payload = str(humid)+" "+str(temp)
      if(temp):
        display_message("Temperature "+str(temp),LINE_1,1)
        display_message("Humidity "+str(humid),LINE_2,1)
        client.publish('raspberry/temp_humid', payload=our_payload, qos=0, retain=False)
        print("temp value send")
        break

  def subscribe_to_broker(client,userdata,flags,rc):
    print("connected with code :" + str(rc))
    client.subscribe("raspberry/temp_humid")
    client.subscribe("raspberry/waterflow_rate")

  def message_from_topic(client,userdata,msg):

    if(msg.topic =="raspberry/waterflow_rate"):
      
      display_message("Water flow rate "+str(msg.payload.decode()),LINE_3,1)
      sendtemp()
    time.sleep(10)



  client = mqtt.Client()
  client.on_connect = subscribe_to_broker
  client.on_message = message_from_topic

  client.connect("192.168.43.143",1883,60)


   

  sendtemp()
    

  client.loop_forever()
    
def lcd_init():
  # Initialise display
  byte_of_lcd(0x33,LCD_CMD) # 110011 Initialise
  byte_of_lcd(0x32,LCD_CMD) # 110010 Initialise
  byte_of_lcd(0x06,LCD_CMD) # 000110 Cursor move direction
  byte_of_lcd(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  byte_of_lcd(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  byte_of_lcd(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def byte_of_lcd(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(RS, mode) # RS
 
  # High bits
  GPIO.output(D4, False)
  GPIO.output(D5, False)
  GPIO.output(D6, False)
  GPIO.output(D7, False)
  if bits&0x10==0x10:
    GPIO.output(D4, True)
  if bits&0x20==0x20:
    GPIO.output(D5, True)
  if bits&0x40==0x40:
    GPIO.output(D6, True)
  if bits&0x80==0x80:
    GPIO.output(D7, True)
 
  # Toggle 'Enable' pin
  toggle_en()
 
  # Low bits
  GPIO.output(D4, False)
  GPIO.output(D5, False)
  GPIO.output(D6, False)
  GPIO.output(D7, False)
  if bits&0x01==0x01:
    GPIO.output(D4, True)
  if bits&0x02==0x02:
    GPIO.output(D5, True)
  if bits&0x04==0x04:
    GPIO.output(D6, True)
  if bits&0x08==0x08:
    GPIO.output(D7, True)
 
  # Toggle 'Enable' pin
  toggle_en()
 
def toggle_en():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(E, True)
  time.sleep(E_PULSE)
  GPIO.output(E, False)
  time.sleep(E_DELAY)
 
def display_message(message,line,style):
  if style==1:
    message = message.ljust(LCD_WIDTH," ") # style=1 Left justified
  elif style==2:
    message = message.center(LCD_WIDTH," ") # style=2 Centred
  elif style==3:
    message = message.rjust(LCD_WIDTH," ") #style=3 Right justified
 
  byte_of_lcd(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    byte_of_lcd(ord(message[i]),LCD_CHR)
 
def lcd_backlight(flag):
  # Toggle backlight on-off-on
  GPIO.output(ON, flag)
 



if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    byte_of_lcd(0x01, LCD_CMD)
    display_message("Prediction Done",LINE_1,2)
    GPIO.cleanup()