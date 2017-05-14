import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

topic = 'autostat/modules'

# TODO: import from app config
hostname = 'iot.eclipse.org'
port = 1883

def message_app(message):
  mqttc.publish(topic, str(message), qos=1)

mqttc = mqtt.Client()
mqttc.connect(hostname, port=port)
mqttc.loop_start()
