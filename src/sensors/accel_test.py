import time, sys, signal, atexit

import pyupm_mma7660 as upmMMA7660

# Instantiate an MMA7660 on I2C bus 0
myDigitalAccelerometer = upmMMA7660.MMA7660(
           			upmMMA7660.MMA7660_I2C_BUS,
                    upmMMA7660.MMA7660_DEFAULT_I2C_ADDR);

## Exit handlers ##
# This function stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
    raise SystemExit

# This function lets you run code on exit, including functions from myDigitalAccelerometer
def exitHandler():
    print "Exiting"
    sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

# place device in standby mode so we can write registers
myDigitalAccelerometer.setModeStandby()

# enable 64 samples per second
myDigitalAccelerometer.setSampleRate(upmMMA7660.MMA7660.AUTOSLEEP_64)

# place device into active mode
myDigitalAccelerometer.setModeActive()

x = upmMMA7660.new_intp()
y = upmMMA7660.new_intp()
z = upmMMA7660.new_intp()

ax = upmMMA7660.new_floatp()
ay = upmMMA7660.new_floatp()
az = upmMMA7660.new_floatp()

while (1):
    myDigitalAccelerometer.getRawValues(x, y, z)
    outputStr = ("Raw values: x = {0}"
    " y = {1}"
    " z = {2}").format(upmMMA7660.intp_value(x),
    upmMMA7660.intp_value(y),
    upmMMA7660.intp_value(z))
    print outputStr

    myDigitalAccelerometer.getAcceleration(ax, ay, az)
    outputStr = ("Acceleration: x = {0}"
    "g y = {1}"
    "g z = {2}g").format(upmMMA7660.floatp_value(ax),
    upmMMA7660.floatp_value(ay),
    upmMMA7660.floatp_value(az))
    print outputStr
    time.sleep(.5)