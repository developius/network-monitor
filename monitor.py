#-----------------------------------------------#
#		Network Monitor			#
# http://github.com/developius/network-monitor  #
#-----------------------------------------------#

import subprocess, time, datetime, csv, os, pysftp,sys, json

configFile = json.load(open("config.json")) # load the config file

try: sftp = pysftp.Connection(configFile['host'], username=configFile['username']) # try to connect to the server
except: print("ssh error!"); sys.exit() # exit if we can't

while True: # loop forever
	with open("data/%s.csv" % datetime.datetime.now().strftime("%d-%m-%Y"),"a") as fp: # open the file in append mode with data/format d-m-y.csv
		commands = ["ping -c 1 192.168.1.254","ping -c 1 google.com"] # the commands to run (192.168.1.254 needs to be changed to your router)
		json = {"data":[{},{}]} # dictionary to store our data
		json["data"][0]["time"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") # put the current time into our data storage dictionary
		processes = [subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE) for cmd in commands] # start running the commands
		ok = True
		for p in processes: # for each command
			p.wait() # wait for it to finish
			try:
				out = p.communicate()[0].split() # get the output of the command
				if out[1] == commands[0].split()[3]: # if the command is the internal one
					json['data'][0]['ip']    = out[1] # get host ip
					json['data'][0]['taken'] = out[33].split("/")[1] # get round trip time (ms)
					json['data'][0]['loss']  = out[25] # get loss of trip (%)
				if out[1] == commands[1].split()[3]: # if the command is the external one
					json['data'][1]['ip']    = out[1]; # get host ip
					json['data'][1]['taken'] = out[34].split("/")[1] # get round trip time (ms)
					json['data'][1]['loss']  = out[26] # get loss of trip (%)
			except: ok = False # something went wrong
		if ok: # if we are ok
			print("Time: %s" % json['data'][0]['time']) # print current time
			print("	[INTERNAL] IP: %s Time taken: %s Loss: %s" % (json['data'][0]['ip'],json['data'][0]['taken'],json['data'][0]['loss'])) # print internal pings stats
			print("	[EXTERNAL] IP: %s Time taken: %s Loss: %s" % (json['data'][1]['ip'],json['data'][1]['taken'],json['data'][1]['loss'])) # print external ping stats
			data = [json['data'][0]['time'], # make nice list of data
				json['data'][0]['ip'],
				json['data'][0]['taken'],
				json['data'][0]['loss'],
		                json['data'][1]['ip'],
		                json['data'][1]['taken'],
		                json['data'][1]['loss']]
			fp.write("%s,%s,%s,%s\r\n%s,%s,%s,%s\r\n" %(data[0],data[1],data[2],data[3],data[0],data[4],data[5],data[6])) # write the stats to the csv file
			json_out = '{"data":[{"time":"%s","ip":"%s","taken":"%s","loss":"%s"},{"ip":"%s","taken":"%s","loss":"%s"}]}' % (json['data'][0]['time'],json['data'][0]['ip'],json['data'][0]['taken'],json['data'][0]['loss'],json['data'][1]['ip'],json['data'][1]['taken'],json['data'][1]['loss']) # make nice json array for upload to server
			with open("/home/pi/coding/current.txt","w") as current_file: # open the current stats file
				current_file.write(json_out) # write the current stats
				current_file.close() # close the file
				try:
					with sftp.cd('www/home'): # move to correct diretory on server
						sftp.put('current.txt') # upload current stats to server file
				except: print("SFTP upload error") # something went wrong
		else: print("Not ok!") # not ok!
