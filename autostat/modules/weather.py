import requests
import autostat.app_config as app_config
from app.actions import create_action
from mqtt_publish import message_app
from weather_module_config import API_KEY, API_URL
import threading

MODULE_NAME = 'weather'

def get_weather(lat, lon):
  params = {
    'appid': API_KEY,
    'lat': str(lat),
    'lon': str(lon)
  }
  r = requests.get(API_URL, params=params)
  response = r.json()
  temperature_data = {
    'temp': kelvin_to_celsius(response['main']['temp']),
    'temp_min': kelvin_to_celsius(response['main']['temp_min']),
    'temp_max': kelvin_to_celsius(response['main']['temp_max'])
  }
  return temperature_data

def kelvin_to_celsius(kelvin):
  return kelvin - 273.15

def create_weather_action(lat, lon):
  temperature_data = get_weather(lat, lon)
  weather_action = create_action('WEATHER_UPDATE', temperature_data)
  return weather_action

def send_action(action):
  message_app(action)

def add_weather_module():
  payload = {
    'type': MODULE_NAME
  }
  add_module_action = create_action('ADD_WEATHER_MODULE', payload)
  send_action(add_module_action)

  weather_action = create_weather_action(app_config.LOCATION['lat'], app_config.LOCATION['lon'])
  send_action(weather_action)

def add_weather_module_dispatch(payload, app_state):
  if MODULE_NAME not in [m['type'] for m in app_state['module_data']]:
    app_state['module_data'].append(payload)

def weather_action_dispatch(payload, app_state):
  # update app state
  weather_module_data = [m for m in app_state['module_data'] if m['type'] == MODULE_NAME][0]
  weather_module_data['temperature_data'] = payload

  # describe how weather should affect virtual temp
  current_temp = payload['temp']
  for satellite in app_state['satellites']:
    virtual_temp = satellite['virtual_temperature']

    # if set to AC and it's colder outside, reduce virtual temp so AC runs less
    if app_state['type'] == 'AC' and current_temp < virtual_temp:
      dt = virtual_temp - current_temp
      magnitude = scale_virtual_temp(dt)
      satellite['virtual_temperature'] -= magnitude

    # if set to AC, it's hot outside, and AC is currently off,
    # increase virtual temp so AC runs more
    # this would typically happen when weather is hovering around room temp
    if app_state['type'] == 'AC' and current_temp > virtual_temp and not app_state['status']:
      dt = current_temp - virtual_temp
      magnitude = scale_virtual_temp(dt)
      satellite['virtual_temperature'] += magnitude

    # if set to HEAT and it's warmer outside, increase virtual temp so HEAT runs less
    if app_state['type'] == 'HEAT' and current_temp > virtual_temp:
      dt = current_temp - virtual_temp
      magnitude = scale_virtual_temp(dt)
      satellite['virtual_temperature'] += magnitude

    # if set to HEAT, it's cold outside, and HEAT is currently off,
    # decrease virtual temp so HEAT runs more
    # this would typically happen when weather is hovering around room temp
    if app_state['type'] == 'HEAT' and current_temp < virtual_temp and not app_state['status']:
      dt = virtual_temp - current_temp
      magnitude = scale_virtual_temp(dt)
      satellite['virtual_temperature'] -= magnitude

  # TODO: do something with min and max temp of the day
  #       maybe this isn't enough - might need hourly weather forecast
  temp_min = payload['temp_min']
  temp_max = payload['temp_max']

# the formula to determine the effect of the
# current temperature with the virtual temperature setting
# can use fine tuning
def scale_virtual_temp(dt):
  return (dt + (dt ** 2)) / 200

# run module
print('running module: ' + MODULE_NAME)

# HACK!
add_weather_thread = threading.Timer(app_config.WEATHER_INTERVAL/4, add_weather_module)
add_weather_thread.daemon = True
add_weather_thread.start()

def update_weather():
  update_weather_thread = threading.Timer(app_config.WEATHER_INTERVAL, update_weather)
  update_weather_thread.start()
  weather_action = create_weather_action(app_config.LOCATION['lat'], app_config.LOCATION['lon'])
  send_action(weather_action)

update_weather_thread = threading.Timer(app_config.WEATHER_INTERVAL, update_weather)
update_weather_thread.daemon = True
update_weather_thread.start()
