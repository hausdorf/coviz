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
		return (y.getEnd() - y.getStart()) - (x.getEnd() - x.getStart())



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
write.write(start)

# Update offset graph
for n in range(len(graph)):
	graph[n] += len(start)



index = 0
# Handle everything that happens before the first bytespan
while index < bss[0].getStart():
	c = read.read(1)
	print c
	index+=1

# Handle each bytespan
currBss = 0
while currBss < len(bss):
	# Count bytespans that tie
	count = 0
	currTmp = currBss+1
	while bss[currTmp].getStart() == bss[currBss].getStart():
		count+=1
		currTmp+=1

	# Generate opening tag for each
	for i in range(currBss, currTmp): # might need to be changed back to currBss+count+1
		tag = generateTagOpen(bss[i].getCorefId())
		print tag
	

	# Write until it's time to close the current tag
	curr = currBss+count
	while curr >= currBss:
		# Check to see how many tags open between now and when
		# the next tag closes
		nextTagList = list()
		print bss[currTmp].getStart(), bss[curr].getEnd()
		while bss[curr].getEnd() < bss[currTmp].getStart(): 
			print bss[currTmp].getStart()


		#if bss[currTmp].getStart() < bss[currIndex].getEnd():
		#	print bss[currTmp].getStart()
		#	writeOpenTag = True

		while index <= bss[currIndex].getEnd():
			c = read.read(1)
			print c
			index+=1
		
		#if writeOpenTag:
		#	tag = generateTagOpen(bss[currTmp].getCorefId())
		#	print tag
		#currIndex-=1
		currIndex-=1
		sys.exit()

	sys.exit()






index = 0
for n in range(len(bss)):
	if n > 0:
		n = i

	# Write to overlay until beginning of next bytespan
	while index < bss[n].getStart():
		c = mirror.read(1)
		print c
		index+=1

	#print index, bss[n].getEnd(), bss[n+1].getStart()

	tag = generateTagOpen(bss[n].getCorefId())
	print tag

	i = n+1

	# Traverse list until we find a non-tied bytespan
	while i < len(bss) and bss[n].getStart() == bss[i].getStart():
		tag = generateTagOpen(bss[i].getCorefId())
		print tag
		i+=1
	
	# Write the content until the end of that bytespan: then
	tmp = i
	while tmp > n:
		print i, len(bss)
		while index <= bss[tmp].getEnd():
			print mirror.read(1)
			index+=1
		tag = generateTagClose()
		print tag
		tmp-=1
	
	#sys.exit()

sys.exit()





index = 0
# Begin overlay work on the HTML file.
for item in bss:
	# reset if next bytespan is before current position
	if item.getStart() < index:
		mirror.seek(item.getStart()+graph[item.getStart()])
		overlay.seek(item.getStart()+graph[item.getStart()])
		index = item.getStart()+graph[item.getStart()]

	# while placeholder <= start of bytespan
	while index < item.getStart():
		#overlay.write(mirror.read(1))
		c = mirror.read(1)
		print c
		overlay.write(c)
		index+=1

	overlay.write(generateTagOpen(item.getCorefId()))
	
	# while placeholder in bytespan
	while index <= item.getEnd():
		#overlay.write(mirror.read(1))
		c = mirror.read(1)
		overlay.write(c)
		graph[index] += 15 + len(str(item.getCorefId()))
		index+=1

	overlay.write(generateTagClose())

	for i in range(item.getEnd()+1, fileSize):
		graph[i] += 15 + len(str(item.getCorefId())) + 7
		i+=1


overlay.write("\n</body>\n</html>")
