import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
from sense import temp_update
from config import id

interval = 5
topic = 'autostat/satellite'

hostname = "iot.eclipse.org" # Sandbox broker
port = 1883 # Default port for unencrypted MQTT

mqttc = mqtt.Client()
mqttc.connect(hostname, port=port)
mqttc.loop_start()
while True:
  temp_action = temp_update(id)
  print temp_action
  mqttc.publish(topic, str(temp_action), qos=1)
  time.sleep(interval)
