#adds or subtracts time to all closed captioning in a .sbv file
#NOTE: currently only shifts time on the order of minutes/seconds.
#This is untested for differences greater than an hour
#-----------------------------------------------------------------
#.sbv files are formatted as:
#<start time>,<end time> 
#	where:
#	<start time> = 0:00:00.000
#	               |  \   \   \
#	               hr mim sec ms
#
#TO-DO: implement support for miliseconds, hours.


import sys
import os
sys.path.append(os.path.dirname(__file__)+'\modules')
import mp3play
import re

dmin=0 #difference in minutes
dsec=1 #difference in seconds
dmsec=0 #difference in ms
TCminutes = 0 #time code for minutes
TCseconds = 0 #time code for seconds
TCmilliseconds = 0 #time code for milliseconds
invalid = True
secondsAcc = 0 #an accumulator for how many seconds to add/subtract

def main():
	clip = mp3play.load(r'AAOCGmIRC6.mp3')
	clip.play()

	print "___ __           __    __      __   ___ __      __ \n | |_  /\ |\/|  (_ \_/|__)/  \|__)   | |__) /\ |__)\n | |__/--\|  |  __) | | \ \__/|      | | \ /--\|   \n *~AUTOMATIC DISCRETE LINEAR CLOSED CAPTIONING DIFFERNCE ENGINE~*\n v.0.1337\n[press enter]"
	raw_input()
	start()

def start():
	
	fp = raw_input("Hello welcome good job please input your .sbv file path or drag your .sbv file here.\n\n")
	
	#add/remove minutes
	dm = raw_input ("To subtract time type a negative number (for example, \"-69\"),\nto add time type a positive number (e.g. \"69\")\n >Input difference in minutes:\n")
	#look for valid input
	if (dm==""): 
		dm = "0"
	isValid(dm)
	while (invalid): 
		dm = raw_input ('NO use an integer like -2, 0, or 69\n')
		isValid(dm)
	
	#add/remove seconds
	ds = raw_input("Thank-you.\n >Input difference in seconds:\n")
	if (ds==""):
		ds="0"
	#look for valid input
	isValid(ds)
	while (invalid):
		ds = raw_input ('NO use an integer like -2, 0, or 69\n')
		isValid(ds)

	#add/remove ms
	dms = raw_input("Thank-you.\n >Input difference in milliseconds:\n(pro-tip: there are 1000ms in a second)\n")
	#if(abs(int(dms))>9999999):
	#	confirm=raw_input("ms is very large, this may take a while. Continue? (Y/N)\n")
        #       if(confirm=="N".lower()):
        #                      start()
	if (dms==""):
		dms="0"
		if (int(ds)==0 and int(dm)==0):
			raw_input('wtf why are you even using this if you don\'t want to input anything wow\n\n')
	#look for valid input
	isValid(dms)
	while (invalid):
		dms = raw_input ('NO use an integer like -2, 0, or 69\n')
		isValid(dms)

	#sets inputted differences to global vars.
	global dsec
	dsec = int(ds)
	global dmin
	dmin = int(dm)
	global dmsec
	dmsec = int(dms)
	
	confirm(dm,ds,dms,fp)
	# confirm = raw_input("You\'re doing great!\nIs this correct?\n	>Difference in minutes: "+dm+"\n 	>Difference in seconds: "+ds+"\n	>Difference in milliseconds: "+dms+"\n(Y) for yes (N) for no.")
	# if (confirm.lower() == "y"):
	# 	readFile(fp)
	# if (confirm.lower()== "n"):
	# 	start()
	# if (confirm==""):
	# 	readFile(fp)
	# else

def confirm(dm,ds,dms,fp):
	confirm = raw_input("You\'re doing great!\nIs this correct?\n	>Difference in minutes: "+dm+"\n 	>Difference in seconds: "+ds+"\n	>Difference in milliseconds: "+dms+"\n(Y) for yes (N) for no.")
	userCompetentce=False
	if (confirm.lower() == "y"):
		readFile(fp)
	if (confirm.lower()== "n"):
		start()
	if (confirm==""):
		readFile(fp)
	while (userCompetentce == False):
		confirm = raw_input("What? I don't understand.\n")
		if (confirm.lower() == "y"):
			userCompetentce = True
			readFile(fp)
		if (confirm.lower()== "n"):
			userCompetentce = True
			start()
		if (confirm==""):
			userCompetentce = True
			readFile(fp)


def isValid(s):
	global invalid
	if (re.match('[a-zA-Z]',s) or '.' in s):
		invalid = True
	else:
		invalid = False
	
def readFile(file_name):
	print "opening"+file_name+"!\n"
	try:
		file1 = open(file_name)
	except IOError:
		fp = raw_input('Invalid file path, try again. (Make sure you include the .sbv extension!):\n')
		readFile(fp)
	else:
		print "file opened!"
	lines = file1.readlines()
	file2 = open(file_name+'_processed.sbv', 'w')
	print "writing new file:"+file_name+'_processed\n'

	#match seconds
	for line in lines:
		line = line.strip()
		if "0:" in line:
			global TCminutes
			global TCseconds
			global TCmilliseconds
			global secondsAcc

			difference = (dsec+(dmin*60)) #the total amount of seconds we want to subtract

		
			#parses in point
			
			TCminutes = int(line[2:4])
			TCseconds = int(line[5:7])
			TCmilliseconds = int(line[8:11])
			calculateMs(dmsec) #calculates the diff in ms
			currentTimeS = TCseconds+(TCminutes*60) #current time in seconds
			subtractSeconds(currentTimeS, difference)
			line = line[:2]+str(TCminutes)+line[4:]
			line = line[:5]+str(TCseconds)+line[7:]
			print "Computed TCmilliseconds: "+str(TCmilliseconds)
			line = line[:8]+str(TCmilliseconds)+line[11:]
			secondsAcc=0 #resets secondsAcc for next timecode
			
			#parses out point
			TCminutes = int(line[14:16]) #!!!This is where it blows up
			TCseconds = int(line[17:19])
			TCmilliseconds = int(line[20:23])
			calculateMs(dmsec) #calculates the diff in ms
			currentTimeS = TCseconds+(TCminutes*60) #current time in seconds
			subtractSeconds(currentTimeS, difference)
			line = line[:14]+str(TCminutes)+line[16:]
			line = line[:17]+str(TCseconds)+line[19:]
			line = line[:20]+str(TCmilliseconds)+line[23:]
			secondsAcc=0 #resets secondsAcc for next timecode
			
			#writes the new line
			file2.write(line+'\n')

		else:
			file2.write(line+'\n')
	file1.close()
	file2.close()
	print "Complete!\n A new file has been written in the same folder that contained your old file!\n\nHave a great day!"
	raw_input()
	exit()

def subtractSeconds(t, s):
	global TCminutes
	global TCseconds
	if ((t+s)<=0): #if we subtract past the start of the video we want our TC to read: 00:00:000
		TCminutes="00"
		TCseconds="00"
		TCmilliseconds="000"
		

	else:
		newTime = t+s #the new time in seconds. Should be a positive int.
		TCminutes = newTime/60 #discerns how many minutes that is
		TCseconds = newTime-(TCminutes*60) #subtracts that
		TCseconds = TCseconds+secondsAcc #the carry from ms
		if (TCseconds<10):
			if(TCseconds<=0):
				TCseconds = '00'
			else:
				TCseconds = '0'+str(TCseconds)
		if (TCminutes<10):
			if (TCminutes<=0):
				TCminutes = '00'
			else:
				TCminutes = '0'+str(TCminutes)
		
def calculateMs(n):
	newMs = TCmilliseconds+n
	print "newMs printout: "+str(newMs)
	#do we need to add or subtract seconds?
	if(newMs<0):
		subtractMs(newMs)
	if(newMs>999):
		addMs(newMs)
	elif (n<0):
		subtractMs(newMs)
	elif (n>=0):
		addMs(newMs)
	elif (newMs==0):
		TCmilliseconds == '000'

def subtractMs(msInput):
	global secondsAcc
	global TCmilliseconds

	while (msInput<0):
		print "in while loop"
		msInput = 1000 + msInput #we're adding because msInput is negative.
		secondsAcc -= 1

	
	if(msInput==0):
		TCmilliseconds = "000"
	if(msInput>-10):
		TCmilliseconds = "00"+str(msInput)
	if(msInput>-100):
		TCmilliseconds = "0"+str(msInput)
	else:
		TCmilliseconds = msInput

def addMs(msInput):
	global secondsAcc
	global TCmilliseconds
	print "TCmilliseconds in addms!: "+str(TCmilliseconds)
	
	while (msInput>999):
		print "in while loop"
		msInput = msInput-1000
		secondsAcc += 1

	if(msInput==0):
		TCmilliseconds = "000"
	if(msInput<10):
		TCmilliseconds = "00"+str(msInput)
	if(msInput<100):
		TCmilliseconds = "0"+str(msInput)
	else:
		TCmilliseconds = str(msInput)


main()
