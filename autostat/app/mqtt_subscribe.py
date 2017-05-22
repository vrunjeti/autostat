import paho.mqtt.client as mqtt
import json
from state import APP_STATE as state
import autostat.app_config as app_config
from dispatcher import dispatch

topics = [
  ('autostat/from_satellite', 1),
  ('autostat/modules', 1),
  ('autostat/control_board', 1)
]

def on_connect(client, userdata, rc):
  # Successful connection is '0'
  print('Connection result: ' + str(rc))
  if rc == 0:
    client.subscribe(topics)
    if app_config.DEBUG:
      print('---------- STATE -----------')
      print(json.dumps(state, indent=2, sort_keys=True))
      print('----------------------------')

def on_message(client, userdata, message):
  action = eval(message.payload.decode('utf-8'))
  dispatch(action)

def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Disconnected unexpectedly')

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(app_config.MQTT_HOSTNAME, app_config.MQTT_PORT)
client.loop_forever()
