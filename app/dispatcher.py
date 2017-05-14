# purpose of dispatcher is to take actions and update the application state
# the controller will then take the state and decide what to do with the updated state

from app.state import APP_STATE as state

# the threshold for the difference in the set temp
# and the current temp needed to change the status
# TODO: line up with config.py
TOLERANCE = 1

def dispatch(action):
  type = action['type']
  payload = action['payload']
  action_mapper[type](payload)

def set_system_temperature(temp):
  state['set_temperature'] = temp

  # setting system temp will also set all satellites
  for s in state['satellites']:
    s['set_temperature'] = temp
    s['virtual_temperature'] = temp

def user_adjust_up(payload):
  id = payload['id']
  satellite = [s for s in state['satellites'] if s['id'] == id][0]
  # change by tolerance because automatic adjust with user adjusting implies
  # adjustments are more related to overall application state than speicific temperatures
  # (like a traditional thermostat)
  satellite['virtual_temperature'] += TOLERANCE

def user_adjust_down(payload):
  id = payload['id']
  satellite = [s for s in state['satellites'] if s['id'] == id][0]
  # change by tolerance because automatic adjust with user adjusting implies
  # adjustments are more related to overall application state than speicific temperatures
  # (like a traditional thermostat)
  satellite['virtual_temperature'] -= TOLERANCE

def temp_update(payload):
  id = payload['id']
  satellite = [s for s in state['satellites'] if s['id'] == id][0]
  satellite['current_temperature'] = payload['temperature']

  temp_diff = satellite['current_temperature'] - satellite['set_temperature']
  if state['type'] == 'HEAT':
    temp_diff = temp_diff * -1

  satellite['virtual_temperature'] += temp_diff

action_mapper = {
  'USER_ADJUST_UP': user_adjust_up
  'USER_ADJUST_DOWN': user_adjust_down
  'TEMP_UPDATE': temp_update
}
