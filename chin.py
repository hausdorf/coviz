#chin.py
# usage: python chin.py key raw.txt
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
#  A bytespan is typically a NP that is associated with a coref
#  chain. The actual bytespan of a Bytespan object refers to the
#  literal place in a document at which the NP resides: for example,
#  1,12 is a bytespan that begins at 1 and ends at 12. The bytespan
#  object also keeps track of the coref ID associated with the
#  bytespan, which essentially indicates to which coref chain the
#  NP belongs.
class ByteSpan:
	def __init__(self, start, end, corefId):
		self.start = start
		self.end = end
		self.corefId = corefId
		self.count = 0
		self.levelsNested = 0

	def __str__(self):
		return str(self.start) + " " + str(self.end) + " " + str(self.corefId)

	def incCount():
		self.count += 1

	def getCount():
		return self.count

	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end

	def getCorefId(self):
		return self.corefId

	def getLevelsNested(self):
		return self.levelsNested

	def incLevelsNested(self):
		self.levelsNested += 1

	def decLevelsNested(self):
		self.levelsNested -= 1

	# For debugging

	def __str__(self):
		return str(self.start) + " " + str(self.end) + " " + str(self.corefId)

	def printargs(self):
		print self.start, self.end, self.corefId, self.levelsNested
	
	def printNested(self):
		print str(self.start) + " " + str(self.levelsNested)


#### GLOBAL METHODS ####
####                ####
# Generally handle tasks that happen more than once, or that potentially
# need to be customized easily and quickly.

# Generates a span tag with an id specified in the formal params. The
#  intended use of this function is to generate a span tag whose id
#  is the same as the bytespan object's coref ID.
def generateTagOpen(id, levelsNested):
	return_val = "<span class=\"" + str(id) + "\" onmouseover=\"printAttributes(" + str(id)
	return_val += ", " + str(bss[id].getStart()) + ", " + str(bss[id].getEnd()) + ");\" "
	return_val += "style=\"border:solid 1px #000;padding:" + str(levelsNested*2) + ";\">"
	return return_val

# Generates a closing for a span tag.
#  Intended to be close a tag that was openend with generateTagOpen()
def generateTagClose():
	return "</span>"

def generateJs():
	return "<script type=\"text/javascript\" src=\"scripts.js\"></script>"

# The ordering function that helps sort() sort the bss objects. It first
#  looks at initial position, indicated by bss[anything].getStart(); if
#  one of them starts first, that one should come before the other in
#  the list. If they tie, the one that has the longest bytespan comes
#  first.
def orderBss(x, y):
	if y.getStart() != x.getStart():
		return x.getStart() - y.getStart()
	else:
		return (y.getEnd() - y.getStart()) - (x.getEnd() - x.getStart())

def createIdLink(itemId):
	return_val = "<span onclick=\"peek('" + str(itemId)
	return_val += "')\" style=\"background-color:#DDD;cursor:pointer;\">" + str(itemId)
	return_val += "</span>\t"
	return return_val


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
#  event of a tie, the largest bytespan comes first.
bss = sorted(bss, cmp=orderBss)

# Open new html file, begin writing basic template data to it.
write = open(overlayFileTitle, 'w')
read = open(sys.argv[2], 'rb')
start = "<html>\n\n<head>" + generateJs() + "<link href=\"style.css\" rel=\"stylesheet\" type=\"text/css\">"
start += "</head>\n\n<body>\n<div id=\"attribute-display\"></div>"
write.write(start)

write.write("<div id=\"original\">")

#### WRITE ID LINKS ####
####                ####
# corefIdList = list()
# for item in bss:
# 	if corefIdList.count(item.getCorefId()) == 0:
# 		corefIdList.append(item.getCorefId())
# 
# corefIdList.sort()
# 
# for id in corefIdList:
# 	write.write(createIdLink(id))

#### ADD NESTING DATA ####
####                  ####
nestCount = 0
bsCount = 1
openBsObjects = list()
openBsObjects.append(bss[0])

while bsCount < len(bss):
	openBsObjects.append(bss[bsCount])
	if openBsObjects[len(openBsObjects)-2].getStart() < openBsObjects[len(openBsObjects)-1].getEnd():
		nestCount += 1
		if nestCount > openBsObjects[len(openBsObjects)-1].getLevelsNested():
			for bs in openBsObjects:
				bs.incLevelsNested()

	n = 0
	while len(openBsObjects) >= 1 and n < len(openBsObjects):
		print "n: " + str(n)
		for bs in openBsObjects:
			bs.printargs()

		traverse = 0
		while traverse < len(openBsObjects):
			if openBsObjects[len(openBsObjects)-1].getStart() > openBsObjects[traverse].getEnd():
				print "eject: " + str(openBsObjects[traverse])
				openBsObjects.pop(traverse)
				nestCount-=1
			traverse += 1
		n+=1
	print "\n"

	bsCount += 1

#### WRITE THE OVERLAY FILE ####
####                        ####
# 1. Read one character from raw.txt
# 2. Traverse through all bytespans that begin at the location of the current
#   character. For each bytespan that begins at this character, generate an
#   open tag (a), insert it into a stack the tracks unclosed tags (b).
# 3. Traverse through all unclosed bytespans; if the current location is the
#   place that a bytespan closes, then insert a closing tag. Do this for all
#   tags that end at this position.
# 4. Write the current character to file. At this point, we will have added
#   all tags that need to open and close, and all that's left to do is append
#   write the actual content into the overlay file. We handle this in a special
#   way: (a) if it's a newline, we also insert a < p> tag so that it looks like
#   it should when we open it in a browser; (b) in any other case, we just
#   the actual character.

char = True
charIndex = 0
bytespanIndex = 0
bytespanStack = list()

# Create div#original
while char:
	char = read.read(1) #1
	while bytespanIndex < len(bss) and bss[bytespanIndex].getStart() == charIndex: #2
		write.write(generateTagOpen(bss[bytespanIndex].getCorefId(), bss[bytespanIndex].getLevelsNested())) #2a
		bytespanStack.insert(0, bss[bytespanIndex]) #2b
		bytespanIndex+=1

	while len(bytespanStack) != 0 and bytespanStack[0].getEnd() == charIndex: #3
		write.write(generateTagClose())
		bytespanStack.pop(0)

	# 4
	if char == "\n":
		write.write("<p>\n") #4a
	else:
		write.write(char) #4b
	charIndex+=1

write.write("</div>")

# Re-initialize the variables
char = True
charIndex = 0
bytespanIndex = 0
bytespanStack = list()
read = open(sys.argv[2], 'rb')

# Create div#tracking
write.write("<div id=\"tracking\">")
while char:
	char = read.read(1) #1
	while bytespanIndex < len(bss) and bss[bytespanIndex].getStart() == charIndex: #2
		write.write(generateTagOpen(bss[bytespanIndex].getCorefId(), bss[bytespanIndex].getLevelsNested())) #2a
		bytespanStack.insert(0, bss[bytespanIndex]) #2b
		bytespanIndex+=1

	while len(bytespanStack) != 0 and bytespanStack[0].getEnd() == charIndex: #3
		write.write(generateTagClose())
		bytespanStack.pop(0)

	# 4
	if char == "\n":
		write.write("<p>\n") #4a
	else:
		write.write(char) #4b
	charIndex+=1
write.write("</div>")

sys.exit()

