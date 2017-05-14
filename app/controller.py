from app.state import APP_STATE as state
from app.mqtt_publish import message_satellite
import app.system_interface as system_interface

# the threshold for the difference in the set temp
# and the current temp needed to change the status
# TODO: line up with config.py
TOLERANCE = 1

# TODO: import
def create_action(type, payload):
  action = {
    'type': type,
    'payload': payload
  }
  return action

def add_satellite(id):
  satellite = {
    'id': id,
    # initialize satellite set temp to system temp
    'set_temperature': state['set_temperature'],
    # initialize satellite curr temp to system temp,
    # update after connecting
    # TODO: or include as param?
    'current_temperature': state['set_temperature'],
    'status': False,
    'virtual_temperature': state['set_temperature']
  }
  state['satellites'].append(satellite)
  # TODO: call update_satellites_status() here or in app code?
  update_satellites_status()

def update_satellites_status():
  for satellite in state['satellites']:
    temp_diff = satellite['virtual_temperature'] - satellite['set_temperature']

    if state['type'] == 'HEAT':
      temp_diff = temp_diff * -1

    if temp_diff > TOLERANCE:
      if not satellite['status']:
        satellite['status'] = True
        signal_satellite_status(satellite['id'])
    else:
      if satellite['status']:
        satellite['status'] = False
        signal_satellite_status(satellite['id'])

def signal_satellite_status(id):
  satellite = [s for s in state['satellites'] if s['id'] == id][0]
  payload = {
    'id': id,
    'status': satellite['status']
  }
  action = create_action('SATELLITE_MESSAGE', payload)
  message_satellite(action)

def update_system_status():
  satellite_statuses = [s['status'] for s in state['satellites']]
  if any(satellite_statuses):
    if not state['status']:
      state['status'] = True
      system_interface.system_resume()
  else:
    if state['status']:
      state['status'] = False
      system_interface.system_standby()
