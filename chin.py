#chin.py
import sys
import os

# Class that holds information for every bytespan.
# 	A bytespan is typically a NP that is associated with a coref
# 	chain. The actual bytespan of a Bytespan object refers to the
# 	literal place in a document at which the NP resides: for example,
# 	1,12 is a bytespan that begins at 1 and ends at 12. The bytespan
# 	object also keeps track of the coref ID associated with the
# 	bytespan, which essentially indicates to which coref chain the
# 	NP belongs.
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

# Generates a span tag with an id specified in the formal params.
# 	Each bytespan object has covers a span of bytes. For example, the
# 	bytespan 0,12 covers the bytes from 0 - 12. Each of these objects
# 	is associated with a coref chain, indicated by the coref ID. The
# 	intended use of this function is to generate a span tag whose id
# 	is the same as the bytespan object's coref ID.
def generateTagOpen(id):
	return "<span class=\"" + str(id) + "\">"

# Generates a closing for a span tag.
# 	Intended to be close a tag that was openend with generateTagOpen()
def generateTagClose():
	return "</span>"

def generateJs():
	print "this is a stub for later"

# The ordering function that helps sort() sort the bss objects. It first
# 	looks at initial position, indicated by bss[anything].getStart(); if
# 	one of them starts first, that one should come before the other in
# 	the list. If they tie, the one that has the longest bytespan comes
# 	first.
def orderBss(x, y):
	if y.getStart() != x.getStart():
		return x.getStart() - y.getStart()
	else:
		return (y.getEnd() - y.getStart()) - (x.getEnd() - x.getStart())

# Updates the offset graph given a position (pos) and an amount (amt).
# 	When writing the NP/coref chain overlay, we add span tags to the html,
# 	which allows us to identify NPs as in one coref chain or another. The
# 	graph tells us how many characters have been added to the document at
# 	any given position. For example, if graph[x] holds the integer 43, we
# 	know that there are 43 characters added before that position. Thus,
# 	when we add to the overlay document, we know that we should seek to
# 	the position x + 43, or whatever position we wanted, plus the 43 chars
# 	we've added to the document.
def updateGraph(pos, updateAmt):
	for placeholder in range(pos, len(graph)):
		graph[placeholder] += updateAmt

# Copies all characters in the overlay file from the point pos to EOF.
# 	We use this to insert tags into the document; we don't want to
# 	overwrite everything, but instead, to add some text, and preserve
# 	whatever comes after this. The way to do this is to copy everything
# 	after into a buffer, and then write it back afterwards. Because we
# 	sort the bytespan objects in bss, this tends to be no more than a
# 	few characters.
def createBuffer(endPosOfBytespan):
	print "here"



# Open file from argument
raw = open(sys.argv[1], 'r')

# Create a list of all lines in the key
lines = raw.readlines()

# Create a list to hold the ByteSpan objects
bss = list()

# Process each line in succession
# 	Parse bytespan and corefid, put in object, place object in list
for line in range(1, len(lines)):
	words = lines[line].split()
	byteRange = words[1].split(",")	#parse bytespan
	id = filter(lambda x: x in '1234567890', words[5])	#turn bytespan into numbers
	bs = ByteSpan(int(byteRange[0]), int(byteRange[1]), int(id))	#store bytespan in object
	bss.append(bs)	#add object to list

# Sort the list. Begin with starting position of bytespan; in the
# 	event of a tie, the largest bytespan comes first.
bss = sorted(bss, cmp=orderBss)
#for i in bss:
	#i.printargs()

# Create graph that tells how much the offset is at any given point in the file.
# 	Adding the <span> tags to the HTML file changes how many bytes into the file
# 	a word is; This graph is used to tell how many bytes the offset at any point
# 	in the file is.
graph = list()
fileSize = os.path.getsize(sys.argv[2])
for i in range(0, fileSize):
	graph.append(0)

# Open new html file, begin writing basic template data to it.
write = open("corefoverlay.html", 'w')
read = open(sys.argv[2], 'rb')
start = "<html><head></head>\n<body>\n"
print start
write.write(start)

# Update offset graph
updateGraph(0, len(start))



index = 0
# Handle everything that happens before the first bytespan
while index < bss[0].getStart():
	c = read.read(1)
	print c
	write.write(c)
	index+=1

# Process 1 bytespan object:
# 	1. Reset the var index, which we use to keep track of where our "cursor" is in the
# 		original (raw) text file. Seek read's cursor to this point, as we want to start
# 		reading from here. If you don't seek, then you end up continuing reading from the
# 		last point you were at.
# 	2. Seek to the byte in the overlay file that's delineated by [item].getStart()
# 		Because we are adding tags, the location of the byte in the original file will
# 		not correspond directly to the byte in the overlay file; to get the corresponding
# 		byte, we must include the "offset" generated by the tags, which is stored in
# 		the list called "graph". So the location of any byte in the overlay file can
# 		be expressed as overlayPos = originalPos + graph[x], where the integer at graph[x]
# 		contains the offset at the point x.
# 	3. Copy everything from the position we will be inserting to until the end of the
# 		overlay file into a buffer. This may sound expensive, but remember that the
# 		bytespan objects are sorted, so the cost of this is actually usually only a few
# 		characters.
# 	4. Insert opening tag that will hold the NP in the given bytespan
# 	5. Update the graph that keeps track of offset
# 	6. Write content of tag
# 	7. Insert closing tag
# 	8. Update graph that keeps track of offset
# 	9. Copy back the buffer
bssItem = 0
while bssItem < 2:
	index = bss[bssItem].getStart() # 1
	read.seek(index)
	write.seek(bss[bssItem].getStart() + graph[bss[bssItem].getStart()]) # 2
	buffer = createBuffer(bss[bssItem].getEnd()) # 3
	tag = generateTagOpen(bss[bssItem].getCorefId())
	print tag
	write.write(tag) # 4
	updateGraph(bss[bssItem].getStart(), len(generateTagOpen(bss[bssItem].getCorefId()))) # 5
	while index < bss[bssItem].getEnd(): # 6
		c = read.read(1)
		print c
		write.write(c)
		index+=1
	tag = generateTagClose()
	print tag
	write.write(tag) # 7
	updateGraph(bss[bssItem].getEnd(), len(generateTagClose())) # 8

	bssItem+=1
