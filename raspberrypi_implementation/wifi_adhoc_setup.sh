if [ $# != 1 ] ; then
 echo "$0 <SSID>"
 exit
fi
$rmt iwconfig wlan0 mode ad-hoc 
$rmt iwconfig wlan0 essid $1
