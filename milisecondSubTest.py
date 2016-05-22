#adds or subtracts ms while carrying in minutes.

seconds = 2
milliseconds = 50
msToSub = 5000
secondsAcc = 0
timecode = "0:00:05.660,0:00:08.960"
def calculateMs(n):
	newMs = milliseconds+n
	if(abs(n)>9999999):
		confirm=raw_input("ms is very large, this may take a while. Continue? (Y/N)\n")
		if(confirm=="N".lower()):
			print "exiting"
	#do we need to add or subtract seconds?
	if(newMs<0):
		subtractMs(newMs)
	if(newMs>999):
		addMs(newMs)



#subtracts ms
#determines how many seconds to carry over in an accumulator.
def subtractMs(msInput):
	global secondsAcc
	while (msInput<0):
		print "in while loop"
		msInput = 1000+msInput #we're adding because msInput is negative.
		secondsAcc -= 1
	print "final ms: "+str(msInput)+". seconds acc: "+str(secondsAcc)

def addMs(msInput):
	global secondsAcc
	while (msInput>999):
		print "in while loop"
		msInput = msInput-1000
		secondsAcc += 1
	print "final ms: "+str(msInput)+". seconds acc: "+str(secondsAcc)

calculateMs(msToSub)

print timecode[8:11]
print timecode[20:23]