import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import autostat.app_config as app_config

topic = 'autostat/to_satellite'

def message_satellite(message):
  mqttc.publish(topic, str(message), qos=1)

mqttc = mqtt.Client()
mqttc.connect(app_config.MQTT_HOSTNAME, port=app_config.MQTT_PORT)
mqttc.loop_start()
