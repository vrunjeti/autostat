import paho.mqtt.client as mqtt
import time

hostname = "iot.eclipse.org" # Sandbox broker
port = 1883 # Default port for unencrypted MQTT

topic = "autostat/satellite"

def on_connect(client, userdata, rc):
  # Successful connection is '0'
  print("Connection result: " + str(rc))
  if rc == 0:
    # Subscribe to topics
    client.subscribe(topic)

def on_message(client, userdata, message):
  print("Received message on %s: %s (QoS = %s)" % (message.topic, message.payload.decode("utf-8"), str(message.qos)))
  print "temp is " + str(eval(message.payload.decode("utf-8"))['payload']['temperature'])

def on_disconnect(client, userdata, rc):
  if rc != 0:
    print("Disconnected unexpectedly")

# Initialize client instance
client = mqtt.Client()

# Bind events to functions
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to the specified broker
client.connect(hostname, port=port)

# Network loop runs in the background to listen to the events
client.loop_forever()
