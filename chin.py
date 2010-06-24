#chin.py
import sys
import os

# Class that holds information for every bytespan.
#	 A bytespan is typically a NP that is associated with a coref
#	 chain. The actual bytespan of a Bytespan object refers to the
#	 literal place in a document at which the NP resides: for example,
#	 1,12 is a bytespan that begins at 1 and ends at 12. The bytespan
#	 object also keeps track of the coref ID associated with the
#	 bytespan, which essentially indicates to which coref chain the
#	 NP belongs.
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

# Generates a span tag with an id specified in the formal params. The
#	 intended use of this function is to generate a span tag whose id
#	 is the same as the bytespan object's coref ID.
def generateTagOpen(id):
	return "<span class=\"" + str(id) + "\">"

# Generates a closing for a span tag.
#	 Intended to be close a tag that was openend with generateTagOpen()
def generateTagClose():
	return "</span>"

def generateJs():
	print "this is a stub for later"

# The ordering function that helps sort() sort the bss objects. It first
#	 looks at initial position, indicated by bss[anything].getStart(); if
#	 one of them starts first, that one should come before the other in
#	 the list. If they tie, the one that has the longest bytespan comes
#	 first.
def orderBss(x, y):
	if y.getStart() != x.getStart():
		return x.getStart() - y.getStart()
	else:
		return (y.getEnd() - y.getStart()) - (x.getEnd() - x.getStart())

# Copies all characters in the overlay file from the point pos to EOF.
#	 We use this to insert tags into the document; we don't want to
#	 overwrite everything, but instead, to add some text, and preserve
#	 whatever comes after this. The way to do this is to copy everything
#	 after into a buffer, and then write it back afterwards. Because we
#	 sort the bytespan objects in bss, this tends to be no more than a
#	 few characters.
def createBuffer(endPosOfBytespan):
	readOverlay = open("corefoverlay.html", 'r')
	readOverlay.seek(endPosOfBytespan, 0)
	buffer = readOverlay.read()
	return buffer

def readBytes(start, stop):
	readOverlay = open("corefoverlay.html", 'r')
	readOverlay.seek(start, 0)
	sentence = readOverlay.read(stop-start)
	return sentence



# --- BEGIN MAIN ALGORITHM ---

if sys.argv[1] == "open":
	# OPEN OVERLAY HTML HERE!
	os.system("open \"http://www.google.com\"")
	sys.exit()

# Open file from argument
raw = open(sys.argv[1], 'r')

# Create a list of all lines in the key
lines = raw.readlines()

# Create a list to hold the ByteSpan objects
bss = list()

# Process each line in succession
#	 Parse bytespan and corefid, put in object, place object in list
for line in range(1, len(lines)):
	words = lines[line].split()
	byteRange = words[1].split(",")	#parse bytespan
	id = filter(lambda x: x in '1234567890', words[5])	#turn bytespan into numbers
	bs = ByteSpan(int(byteRange[0]), int(byteRange[1]), int(id))	#store bytespan in object
	bss.append(bs)	#add object to list

# Sort the list. Begin with starting position of bytespan; in the
#	 event of a tie, the largest bytespan comes first.
bss = sorted(bss, cmp=orderBss)

# Open new html file, begin writing basic template data to it.
write = open("corefoverlay.html", 'w')
read = open(sys.argv[2], 'rb')
start = "<html><head></head>\n<body>\n"
write.write(start)










char = True
charIndex = 0
bytespanOpen = 0
bytespanClose = 0
bytespanStack = list()

while char:
	char = read.read(1)
	while bytespanOpen < len(bss) and bss[bytespanOpen].getStart() == charIndex:
		write.write(generateTagOpen(bss[bytespanOpen].getCorefId()))
		bytespanStack.insert(0, bss[bytespanOpen])
		bytespanOpen+=1

	while len(bytespanStack) != 0 and bytespanStack[0].getEnd() == charIndex:
		write.write(generateTagClose())
		bytespanStack.pop(0)

	if char == "\n":
		write.write("<p>\n")
	else:
		write.write(char)
	charIndex+=1

sys.exit()

