APP_STATE = {
  'set_temperature': 23,
  'type': 'AC',                   # 'AC' or 'HEAT'
  'status': True                  # True means turned on, False means turned off
  'virtual_weight_multiplier': {
    'user_adjust': 1.0
    'weather': 1.0
    'calendar': 1.0
  },
  'satellites': []
}

# structure for satellite:
# {
#   'id': 'Living Room',          # serves as display name
#   'current_temperature': 25.1,
#   'set_temperature': 24,
#   'status': True,               # True means turned on, False means turned off
#   'virtual_temperature': 24.5,  # used for determining status
# }
