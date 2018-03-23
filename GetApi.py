#!/usr/bin/python3

#Using info from https://www.digitalocean.com/community/tutorials/how-to-use-web-apis-in-python-3 and https://stackoverflow.com/questions/35120250/python-3-get-and-parse-json-api
#From the robtex API I need 'asname', 'whoisdesc', 'bgproute'

from argparse import ArgumentParser
import sys
import io
import os
import json
import requests
import string

api_url_base = "https://freeapi.robtex.com/ipquery/"
headers = headers = {'Content-Type': 'application/json'}



def get_IP_info(ip):
	#Build URL and request
	api_url = str(api_url_base) + str(ip)
	response = requests.get(api_url, headers=headers)
	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None


def print_ip_info(ip):
	ip_Info = get_IP_info(ip)
	if ip_Info is not None:
		try:
			whois = ip_Info["whoisdesc"]
		except:
			whois = ""
		try:
			asname = ip_Info["asname"]
		except:
			asname = ""
		try:
			bgproute = ip_Info["bgproute"]
		except:
			bgproute = ""
		
		print ("\"" + ip + "\",\"" + whois + "\",\"" + asname + "\",\"" + bgproute)
	else:
		print ("Failed for IP " + ip)
#	print ("IP: " +ip)
#	print ("WhoIs: " + ip_Info["whoisdesc"])
#	print ("ASName: " + ip_Info["asname"])
#	print ("Subnet: " + ip_Info["bgproute"])
#	print ("---------------------")

#	print (ip_Info["asname"])
#	if ip_Info is not None:
#		for item in ip_Info['asname']['whoisdesc']['bgproute']:
#			print ("IP: ", IP, "\nWhois: ", item['whoisdesc'], "\nASName: ", item['asname'], "\nSubnet: ", item['bgproute'])
#			print ("-----------------")
#		else:
#			print ("Error! - Failed")


def main():

	parser = ArgumentParser()
	parser.add_argument("-f", "--file", dest="ipFile", help="Open specified file")
	args = parser.parse_args()
	ipFile = args.ipFile
	assert os.path.exists(ipFile), "The file could not be found at, " +str(ipFile)
	print ("ip,whois,asname,subnet")
	with io.open(ipFile,'r',newline=None) as allips:
		for ip in allips:
			#gotta strip the newline
			print_ip_info(ip.rstrip())
	exit()

if __name__== "__main__":
  main()
