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
sys.path.append(os.path.dirname(__file__)+'\modules\mp3play-0.1.15')
#import mp3play
import re

dmin=0 #difference in minutes
dsec=1 #difference in seconds
dms=0 #difference in ms
TCminutes = 0 #time code for minutes
TCseconds = 0 #time code for seconds
invalid = True


def main():
#	clip = mp3play.load(r'AAOCGmIRC6.mp3')
#	clip.play()

	print "___ __           __    __      __   ___ __      __ \n | |_  /\ |\/|  (_ \_/|__)/  \|__)   | |__) /\ |__)\n | |__/--\|  |  __) | | \ \__/|      | | \ /--\|   \n *~AUTOMATIC DISCRETE LINEAR CLOSED CAPTIONING DIFFERNCE ENGINE~*\n v.0.1337\n[press enter]"
	raw_input()
	start()

def start():
	
	fp = raw_input("Hello welcome good job please input your file path\n Example: C:\Users\path_to_file\my_file.sbv\n\n")
	dm = raw_input ("To subtract time type a negative number (for example, \"-69\"),\nto add time type a positive number (e.g. \"69\")\n >Input difference in minutes:\n")
	#look for valid input
	if (dm==""): 
		dm = "0"
	isValid(dm)
	while (invalid): 
		dm = raw_input ('NO use an integer like -2, 0, or 69\n')
		isValid(dm)
	

	ds = raw_input("Thank-you.\n >Input difference in seconds:\n")
	if (ds==""):
		ds="0"
		if (int(ds)==0 and int(dm)==0):
			raw_input('wtf why are you even using this if you don\'t want to input anything wow\n\n')
	#look for valid input
	isValid(ds)
	while (invalid):
		ds = raw_input ('NO use an integer like -2, 0, or 69\n')
		isValid(ds)

	
	global dsec
	dsec = int(ds)
	global dmin
	dmin = int(dm)
	
	confirm = raw_input("You\'re doing great!\nIs this correct?\n	>Difference in minutes: "+dm+"\n 	>Difference in seconds: "+ds+"\n(Y) for yes (N) for no.")
	if (confirm.lower() == "y"):
		readFile(fp)
	if (confirm.lower()== "n"):
		start()
	if (confirm==""):
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
		raw_input('it worked!')
	lines = file1.readlines()
	file2 = open(file_name+'_processed.sbv', 'w')
	print "writing new file:"+file_name+'_processed\n'

	#match seconds
	for line in lines:
		line = line.strip()
		if "0:" in line:
			global TCminutes
			global TCseconds
			difference = (dsec+(dmin*60)) #the total amount of seconds we want to subtract
			
			#parses in point
			TCminutes = int(line[2:4])
			TCseconds = int(line[5:7])
			currentTimeS = TCseconds+(TCminutes*60) #current time in seconds
			subtractSeconds(currentTimeS, difference)
			line = line[:2]+str(TCminutes)+line[4:]
			line = line[:5]+str(TCseconds)+line[7:]
			
			
			#parses out point
			TCminutes = int(line[14:16])
			TCseconds = int(line[17:19])
			currentTimeS = TCseconds+(TCminutes*60) #current time in seconds
			subtractSeconds(currentTimeS, difference)
			line = line[:14]+str(TCminutes)+line[16:]
			line = line[:17]+str(TCseconds)+line[19:]
			
			#writes the new line
			file2.write(line+'\n')

		else:
			file2.write(line+'\n')
	file1.close()
	file2.close()
	print "Complete! A new file has been written in the same folder that contained your old file!\nHave a great day!"
	raw_input()

def subtractSeconds(t, s):
	global TCminutes
	global TCseconds
	if ((t+s)<=0): #if we subtract past the start of the video
		TCminutes="00"
		TCseconds="00"
		

	else:
		newTime = t+s #the new time in seconds. Should be a positive int.
		TCminutes = newTime/60 #discerns how many minutes that is
		TCseconds = newTime-(TCminutes*60) #subtracts that
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
		

main()
