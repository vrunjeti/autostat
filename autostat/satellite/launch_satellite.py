import config
import time
import sense
from mqtt_publish import message_system
import autostat.app_config as app_config
from app.actions import create_action

payload = {
  'id': config.id,
  'temperature': sense.get_temperature()
}
register_satellite_action = create_action('REGISTER_SATELLITE', payload)
message_system(register_satellite_action)

while True:
  temp_action = sense.temp_update(config.id)
  message_system(temp_action)
  time.sleep(app_config.INTERVAL)
