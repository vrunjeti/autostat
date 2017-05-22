import autostat.app_config as app_config
from actions import create_action
from state import APP_STATE as state
from mqtt_publish import message_satellite
import system_interface

def trigger_update():
  update_satellites_status()
  update_system_status()

def update_satellites_status():
  for satellite in state['satellites']:
    temp_diff = satellite['virtual_temperature'] - satellite['set_temperature']

    if state['type'] == 'HEAT':
      temp_diff = temp_diff * -1

    if temp_diff > app_config.TOLERANCE:
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
