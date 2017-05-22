from autostat.app.actions import create_action

def user_adjust_up(id):
  payload = {
    'id': id
  }
  action = create_action('USER_ADJUST_UP', payload)
  return action

def user_adjust_down(id):
  payload = {
    'id': id
  }
  action = create_action('USER_ADJUST_DOWN', payload)
  return action
