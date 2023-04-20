#!/usr/bin/env python

import re,os

ssid = ""
with open('ap_info.txt', 'r') as out_file:
    ap_info = out_file.read()
    ap_info = ap_info.strip()
    info_list = ap_info.split("=")
    ssid = info_list[2]
    # print("Reading ap_info.txt")
    # print(info_list)
hostapd_content = ""
with open("hostapd.conf", "r") as out_file:
	hostapd_content =out_file.read()
with open("hostapd.conf", 'w') as out_file:
	ap_name = re.search("(?:ssid=)(.*)(?:[\\n\\r])", hostapd_content).group(1)
	hostapd_content = hostapd_content.replace(ap_name, ssid)

	# hostapd_content = re.sub("(?:ssid=)(.*)(?:[\\n\\r])", ssid, hostapd_content)
	out_file.write(hostapd_content)
