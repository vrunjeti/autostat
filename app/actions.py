def create_action(type, payload):
  action = {
    "type": type,
    "payload": payload
  }
  return action

# actions defined in app
#
# USER_ADJUST_UP
# payload = {
#   "id": id
# }
#
# USER_ADJUST_DOWN
# payload = {
#   "id": id
# }
#
# TEMP_UPDATE
# payload = {
#   "id": id,
#   "temperature": get_temperature()
# }
