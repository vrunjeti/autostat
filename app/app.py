import time
import app.controller as controller

# minutes that the update of the system occurs
# TODO: line up with config.py
INTERVAL = 30 * 60

# TODO: set up app

# keep app running
while True:
  controller.update_satellites_status()
  controller.update_system_status()
  sleep(INTERVAL)
