import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import app_config
from app.actions import create_action

topic = 'autostat/control_board'

mqttc = mqtt.Client()
mqttc.connect(app_config.MQTT_HOSTNAME, port=app_config.MQTT_PORT)
mqttc.loop_start()

def send_control_message(message):
  mqttc.publish(topic, str(message), qos=1)

def set_room_temp(id, temp):
  """
  """
  payload = {
    'id': id,
    'temperature': temp
  }
  action = create_action('SET_ROOM_TEMP', payload)
  send_control_message(action)

def set_weather(temp):
  """
  """
  payload = {
    'temp': temp,
    'temp_min': temp,
    'temp_max': temp
  }
  action = create_action('SET_TEMP_WEATHER', payload)
  send_control_message(action)
