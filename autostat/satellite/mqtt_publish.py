import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

topic = 'autostat/from_satellite'

def message_system(message):
  mqttc.publish(topic, str(message), qos=1)

mqttc = mqtt.Client()
mqttc.connect(app_config.MQTT_HOSTNAME, app_config.MQTT_PORT)
mqttc.loop_start()
