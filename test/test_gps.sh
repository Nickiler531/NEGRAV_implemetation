stty -F /dev/ttyMFD1 4800

echo "46" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio46/direction

echo 1 > /sys/class/gpio/gpio46/value
sleep 1
echo 0 > /sys/class/gpio/gpio46/value
cat /dev/ttyMFD1 
