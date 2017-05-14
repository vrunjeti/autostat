import paho.mqtt.client as mqtt
import time
from config import id
from interfaces import process_action

# TODO: import from app config
hostname = 'iot.eclipse.org'
port = 1883

topic = 'autostat/to_satellite'

def on_connect(client, userdata, rc):
  # Successful connection is '0'
  print('Connection result: ' + str(rc))
  if rc == 0:
    client.subscribe(topic)

def on_message(client, userdata, message):
  print('Received message on %s: %s (QoS = %s)' % (message.topic, message.payload.decode('utf-8'), str(message.qos)))
  action = eval(message.payload.decode('utf-8'))
  if action['payload']['id'] == id:
    process_action(action)

def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Disconnected unexpectedly')

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(hostname, port=port)
client.loop_forever()
