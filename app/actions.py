def create_action(type, payload):
  action = {
    'type': type,
    'payload': payload
  }
  return action

# actions defined in app
#
# ---- FROM SATELLITE TO APP ----
# USER_ADJUST_UP
# - id
#
# USER_ADJUST_DOWN
# - id
#
# TEMP_UPDATE
# - id
# - temperature
#
# ---- FROM APP TO SATELLITE ----
# SATELLITE_MESSAGE
# - id
# - status
#

