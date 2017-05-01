from sense_hat import SenseHat

sense = SenseHat()

def get_temperature():
  temp = sense.get_temperature()
  return temp
