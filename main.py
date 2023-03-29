import network
import time
from machine import Pin
import netman
from umqttsimple import MQTTClient

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

def callback(topic, msg): 
    print((topic, msg))
    msg = msg.decode('UTF-8')

        
country = 'SG'
ssid = ''
password = ''
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = ''
client_id = ''
user_t = ''
password_t = ''
topic_pub = ''

ldr = machine.ADC(27)

while True:   
    try:
        client = mqtt_connect()
    except OSError as e:
        reconnect()
        
    while True:
        try:
            reading = ldr.read_u16()
            print(reading)
            client.publish(topic_pub, msg=str(round(reading)))
            print('published')
            time.sleep(2)
        except:
            reconnect()
            pass
    client.disconnect()
    



