import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

topic = 'autostat/control_board'

# TODO: import from app config
hostname = 'iot.eclipse.org'
port = 1883

mqttc = mqtt.Client()
mqttc.connect(hostname, port=port)
mqttc.loop_start()

def message_control(message):
  mqttc.publish(topic, str(message), qos=1)

def create_action(type, payload):
  action = {
    'type': type,
    'payload': payload
  }
  return action

