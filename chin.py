#chin.py
import sys
import os

#### GLOBAL CONTROLS ####
####                 ####
# These are easy-access variables to change the behavior of the program.
# Want to change things like what your output file is called? Start here.
overlayFileTitle = "corefoverlay.html" # what the generated HTML file is called

#### INTERNAL DATA-HANDLING CLASSES ####
####                                ####
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

	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end

	def getCorefId(self):
		return self.corefId
	
	# For debugging
	def printargs(self):
		print self.start, self.end, self.corefId


#### GLOBAL METHODS ####
####                ####
# Generally handle tasks that happen more than once, or that potentially
# need to be customized easily and quickly.

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
	script = "\n<script language=\"JavaScript\">\n"
	script += "function peek() {\nalert('hi!');\n}\n"
	script += "</script>\n"
	return script

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

def createIdLink(itemId):
	return "<a href=\"\" onclick=\"peek()\">" + str(itemId) + "</a>\t"

#### CLI PROCESSING ####
####                ####

if sys.argv[1] == "open":
	# OPEN OVERLAY HTML HERE!
	os.system("open \"http://www.google.com\"")
	sys.exit()


#### SETUP ####
####       ####
# Parsing KEY, sorting the ByteSpan objects, etc.


# Open file from argument
raw = open(sys.argv[1], 'r')

# Create a list of all lines in the key
lines = raw.readlines()

# Create a list to hold the ByteSpan objects
bss = list()

# Process each line of the KEY file in succession, put in ByteSpan object
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
write = open(overlayFileTitle, 'w')
read = open(sys.argv[2], 'rb')
start = "<html>\n\n<head>" + generateJs() + "</head>\n\n<body>\n"
write.write(start)


#### WRITE ID LINKS ####
####                ####
corefIdList = list()
for item in bss:
	if corefIdList.count(item.getCorefId()) == 0:
		corefIdList.append(item.getCorefId())

corefIdList.sort()

for id in corefIdList:
	write.write(createIdLink(id))


#### WRITE THE OVERLAY FILE ####
####                        ####
# Finally!

char = True
charIndex = 0
bytespanIndex = 0
bytespanStack = list()

while char:
	char = read.read(1)
	while bytespanIndex < len(bss) and bss[bytespanIndex].getStart() == charIndex:
		write.write(generateTagOpen(bss[bytespanIndex].getCorefId()))
		bytespanStack.insert(0, bss[bytespanIndex])
		bytespanIndex+=1

	while len(bytespanStack) != 0 and bytespanStack[0].getEnd() == charIndex:
		write.write(generateTagClose())
		bytespanStack.pop(0)

	if char == "\n":
		write.write("<p>\n")
	else:
		write.write(char)
	charIndex+=1

sys.exit()

