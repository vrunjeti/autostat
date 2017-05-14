from config import id

def process_action(action):
  if action['payload']['status']:
    open_vent()
  else
    close_vent()

def close_vent():
  print(id + ': closing vent')

def open_vent():
  print(id + ': opening vent')
