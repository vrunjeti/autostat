import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
from sense import temp_update
from config import id

# TODO: import from app config
interval = 5
topic = 'autostat/from_satellite'

hostname = 'iot.eclipse.org'
port = 1883

def message_system(message):
  mqttc.publish(topic, str(message), qos=1)

mqttc = mqtt.Client()
mqttc.connect(hostname, port=port)
mqttc.loop_start()
# while True:
#   temp_action = temp_update(id)
#   mqttc.publish(topic, str(temp_action), qos=1)
#   time.sleep(interval)
