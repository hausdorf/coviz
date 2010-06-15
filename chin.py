#chin.py
import sys

# Class that holds information for every bytespan
class ByteSpan:
	def __init__(self, start, end, corefId):
		self.start = start
		self.end = end
		self.corefId = corefId
	
	# For debugging
	def printargs(self):
		print self.start, self.end, self.corefId
	
	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end

	def getCorefId(self):
		return self.corefId

def generateTagOpen(id):
	return "<div class=\"" + str(id) + "\">"

def generateTagClose():
	return "</div>"

# Open file from argument
raw = open(sys.argv[1], 'r')

# Create a list of all lines from file
lines = raw.readlines()

# Create a list to hold the ByteSpan objects
bss = list()

# Process each line in succession
for line in lines:
	words = line.split()
	byteRange = words[1].split(",")
	id = filter(lambda x: x in '1234567890', words[5])
	bs = ByteSpan(int(byteRange[0]), int(byteRange[1]), int(id))
	bss.append(bs)

# Create the html file
overlay = open("corefoverlay.html", 'w')
mirror = open(sys.argv[2], 'rb')

index = 0
# Begin generating html file
for item in bss:
	item.printargs() #debug
	# while placeholder <= start of bytespan
	while index < item.getStart():
		print mirror.read(1);
		index+=1
	# while placeholder in bytespan
	while index <= item.getEnd():
		print mirror.read(1)
		index+=1


#for item in bss:
#	while index < item.getStart():
#		overlay.write(mirror.read(index))
#		index = index + 1
#	index = item.getStart()
#	overlay.write(generateTagOpen(item.getCorefId()))
#	index = index+1
#	for n in range(index, item.getEnd()):
#		overlay.write(mirror.read(1))
#		index = index+1
#	overlay.write(generateTagClose())
