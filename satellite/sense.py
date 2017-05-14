from sense_hat import SenseHat
# from autostat.app.actions import create_action

sense = SenseHat()

# TODO: figure out import
def create_action(type, payload):
  action = {
    'type': type,
    'payload': payload
  }
  return action

def get_temperature():
  temp = sense.get_temperature()
  return temp

def temp_update(id):
  payload = {
    'id': id,
    'temperature': get_temperature()
  }
  action = create_action('TEMP_UPDATE', payload)
  return action

def set_led_green():
  green = (0, 255, 0)
  sense.clear(green)

def set_led_red():
  red = (255, 0, 0)
  sense.clear(red)
