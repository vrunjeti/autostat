import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import autostat.app_config as app_config

topic = 'autostat/modules'

def message_app(message):
  mqttc.publish(topic, str(message), qos=1)

mqttc = mqtt.Client()
mqttc.connect(app_config.MQTT_HOSTNAME, app_config.MQTT_PORT)
mqttc.loop_start()
