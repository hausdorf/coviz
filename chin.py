#chin.py
import sys
import os

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
	return "<span class=\"" + str(id) + "\">"

def generateTagClose():
	return "</span>"

def generateJs():
	print "this is a stub for later"

def orderBss(x, y):
	if y.getStart() != x.getStart():
		return x.getStart() - y.getStart()
	else:
		return (x.getEnd() - x.getStart()) - (y.getEnd() - y.getStart())


# Open file from argument
raw = open(sys.argv[1], 'r')

# Create a list of all lines from file
lines = raw.readlines()

# Create a list to hold the ByteSpan objects
bss = list()

# Process each line in succession
# 	Parse bytespan and corefid, put in object, place object in list
for line in range(1, len(lines)):
	words = lines[line].split()
	byteRange = words[1].split(",")
	id = filter(lambda x: x in '1234567890', words[5])
	bs = ByteSpan(int(byteRange[0]), int(byteRange[1]), int(id))
	bss.append(bs)

# Sort the list
bss = sorted(bss, cmp=orderBss)
for i in bss:
	i.printargs()
sys.exit()

# Create graph that tells how much the offset is at any given point
graph = list()
fileSize = os.path.getsize(sys.argv[2])
for i in range(0, fileSize):
	graph.append(0)

# Create the html file
overlay = open("corefoverlay.html", 'w')
mirror = open(sys.argv[2], 'rb')
start = "<html><head></head>\n<body>\n"
overlay.write(start)

for n in range(len(graph)):
	graph[n] += len(start)

index = 0
# Overlay HTML with divs
for item in bss:
	# reset if bytespan is before current position
	if item.getStart() < index:
		mirror.seek(item.getStart())
		overlay.seek(item.getStart())
		index = item.getStart()

	# while placeholder <= start of bytespan
	while index < item.getStart():
		overlay.write(mirror.read(1))
		index+=1

	overlay.write(generateTagOpen(item.getCorefId()))
	
	# while placeholder in bytespan
	while index <= item.getEnd():
		overlay.write(mirror.read(1))
		graph[index] += 15 + len(str(item.getCorefId()))
		index+=1

	overlay.write(generateTagClose())

	for i in range(item.getEnd()+1, fileSize):
		graph[i] += 15 + len(str(item.getCorefId())) + 7
		i+=1


overlay.write("\n</body>\n</html>")
print graph
