# purpose of dispatcher is to take actions and update the application state
# the controller will then take the state and decide what to do with the updated state

import json
import autostat.app_config as app_config
from state import APP_STATE as state
import controller as controller
from autostat.modules.weather import weather_action_dispatch as weather_update, add_weather_module_dispatch as add_weather_module

# the threshold for the difference in the set temp
# and the current temp needed to change the status
# TODO: line up with config.py
TOLERANCE = 1

print('app_config.DEBUG: ' + str(app_config.DEBUG))

def dispatch(action):
  type = action['type']
  payload = action['payload']
  action_mapper[type](payload)

  if app_config.DEBUG:
    print('--------- DISPATCH ---------')
    print(json.dumps(action, indent=2, sort_keys=True))
    print('---------- STATE -----------')
    print(json.dumps(state, indent=2, sort_keys=True))
    print('----------------------------')

  controller.trigger_update()

def set_system_temperature(temp):
  state['set_temperature'] = temp

  # setting system temp will also set all satellites
  for s in state['satellites']:
    s['set_temperature'] = temp
    s['virtual_temperature'] = temp

def register_satellite(payload):
  id = payload['id']
  temperature = payload['temperature']

  if any([s for s in state['satellites'] if s['id'] == id]):
    temp_update(payload)
    return

  new_satellite = {
    'id': id,
    'set_temperature': state['set_temperature'],
    'current_temperature': temperature,
    'status': False,
    'virtual_temperature': temperature
  }
  state['satellites'].append(new_satellite)

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

  ct = satellite['current_temperature']
  vt = satellite['virtual_temperature']
  st = satellite['set_temperature']
  ac = state['type'] == 'AC'
  heat = state['type'] == 'HEAT'

  scale = 10

  if ac:
    if ct > vt > st:
      # decrease rate of decreasing vt
      if (ct - vt) > (vt - st):
        dt = (ct - vt) - (vt - st)
        satellite['virtual_temperature'] -= dt / scale
      else:
        dt = (vt - st) - (ct - vt)
        satellite['virtual_temperature'] -= dt / scale
    if vt > ct > st:
      # increase rate of decreasing vt
      dt = (vt - ct) + (ct - st)
      satellite['virtual_temperature'] -= dt / scale
    if ct > st > vt:
      # (gets really hot): increase vt
      dt = (ct - vt)
      satellite['virtual_temperature'] += dt / scale
  if heat:
    if ct < vt < st:
      # decrease rate of increasing vt
      if (vt - ct) > (st - vt):
        dt = (vt - ct) - (st - vt)
        satellite['virtual_temperature'] += dt / scale
      else:
        dt = (st - vt) - (vt - ct)
        satellite['virtual_temperature'] += dt / scale
    if vt < ct < st:
      # increase rate of increasing vt
      dt = (ct - vt) + (st - ct)
      satellite['virtual_temperature'] += dt / scale
    if ct < st < vt:
      # (gets really cold): decrease vt
      dt = (vt - ct)
      satellite['virtual_temperature'] -= dt / scale


action_mapper = {
  'REGISTER_SATELLITE': register_satellite,
  'USER_ADJUST_UP': user_adjust_up,
  'USER_ADJUST_DOWN': user_adjust_down,
  'TEMP_UPDATE': temp_update,
  # modules
  'ADD_WEATHER_MODULE': lambda payload: add_weather_module(payload, state),
  'WEATHER_UPDATE': lambda payload: weather_update(payload, state),
  # simulation
  'SET_ROOM_TEMP': temp_update,
  'SET_TEMP_WEATHER': lambda payload: weather_update(payload, state)
}
