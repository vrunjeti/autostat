from app.state import APP_STATE as state

# the threshold for the difference in the set temp
# and the current temp needed to change the status
TOLERANCE = 1

def set_system_temperature(temp):
  state['set_temperature'] = temp

  # setting system temp will also set all satellites
  for s in state['satellites']:
    s['set_temperature'] = temp

  update_satellites_status()

def set_satellite_temperature(name, temp):
  satellite = [s for s in state['satellites'] if s['name'] == name][0]
  satellite['set_temperature'] = temp
  update_satellites_status()

def add_satellite(name):
  satellite = {
    "name": name,
    # initialize satellite set temp to system temp
    "set_temperature": state['set_temperature'],
    # initialize satellite curr temp to system temp,
    # update after connecting
    # TODO: or include as param?
    "current_temperature": state['set_temperature'],
    "status": False
  }
  state['satellites'].append(satellite)
  # TODO: call update_satellites_status() here or in app code?
  update_satellites_status()

def update_satellites_status():
  for satellite in state['satellites']:
    temp_diff = satellite['current_temperature'] - satellite['set_temperature']

    if state['type'] == "HEAT":
      temp_diff = temp_diff * -1

    if temp_diff > TOLERANCE:
      satellite['status'] = True
    else:
      satellite['status'] = False
