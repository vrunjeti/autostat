import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

topic = 'autostat/control_board'

# TODO: import from app config
hostname = 'iot.eclipse.org'
port = 1883

mqttc = mqtt.Client()
mqttc.connect(hostname, port=port)
mqttc.loop_start()

def send_control_message(message):
  mqttc.publish(topic, str(message), qos=1)

def create_action(type, payload):
  action = {
    'type': type,
    'payload': payload
  }
  return action

def set_room_temp(id, temp):
  payload = {
    'id': id,
    'temperature': temp
  }
  action = create_action('SET_ROOM_TEMP', payload)
  send_control_message(action)

def set_weather(temp):
  payload = {
    'temp': temp,
    'temp_min': temp,
    'temp_max': temp
  }
  action = create_action('SET_TEMP_WEATHER', payload)
  send_control_message(action)
