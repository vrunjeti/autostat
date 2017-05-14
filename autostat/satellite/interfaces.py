from config import id
import sense

def process_action(action):
  if action['payload']['status']:
    open_vent()
    sense.set_led_green()
  else:
    close_vent()
    sense.set_led_red()

def close_vent():
  print(id + ': closing vent')

def open_vent():
  print(id + ': opening vent')
