import config
import time
import sense
from mqtt_publish import message_system

# minutes that the update of the system occurs
# TODO: line up with config.py
INTERVAL = 30 * 60

# TODO: import
def create_action(type, payload):
  action = {
    'type': type,
    'payload': payload
  }
  return action

# TODO: set up app
payload = {
  'id': config.id,
  'temperature': sense.get_temperature()
}
register_satellite_action = create_action('REGISTER_SATELLITE', payload)
message_system(action)

# keep app running
while True:
  temp_action = temp_update(config.id)
  message_system(temp_action)
  time.sleep(INTERVAL)
