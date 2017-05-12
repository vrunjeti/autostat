def dispatch(action):
  type = action['type']
  payload = action['payload']
  return action_mapper[type](payload)

def user_adjust_up(payload):
  pass

def user_adjust_down(payload):
  pass

def temp_update(payload):
  pass

action_mapper = {
  'USER_ADJUST_UP': user_adjust_up
  'USER_ADJUST_DOWN': user_adjust_down
  'TEMP_UPDATE': temp_update
}
