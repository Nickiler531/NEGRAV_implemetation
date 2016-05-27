import time
import pyupm_grove as grove

	 
# Create the button object using GPIO pin 0
button = grove.GroveButton(0)
# Read the input and print, waiting one second between readings
while 1:
    print button.name(), ' value is ', button.value()
    time.sleep(1)
# Delete the button object
del button