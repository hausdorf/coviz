#chin.py
# usage: python chin.py [coref_output] [original source text] [muc_annot]
import sys
import pdb
import os

#### GLOBAL CONTROLS ####
####                 ####
# These are easy-access variables to change the behavior of the program.
# Want to change things like what your output file is called? Start here.
overlayFileTitle = "out.html" # what the generated HTML file is called

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
		self.assocCorefId = list()

	def __str__(self):
		return str(self.start) + " " + str(self.end) + " " \
			+ str(self.corefId)

	def addAssocCorefId(self, id):
		self.assocCorefId.append(id)

	def getAssocCorefIds(self):
		for id in self.assocCorefId:
			yield id

	def printAssocCorefIds(self):
		allIds = ""
		for ids in self.getAssocCorefIds():
			allIds = allIds + str(ids) + " "
		print(allIds)

	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end

	def getCorefId(self):
		return self.corefId

	# For debugging

	def __str__(self):
		return str(self.start) + " " + str(self.end) + " " \
			+ str(self.corefId)

	def printargs(self):
		print self.start, self.end, self.corefId


#### GLOBAL METHODS ####
####                ####
# Generally handle tasks that happen more than once, or that potentially
# need to be customized easily and quickly.

# Generates a span tag with an id specified in the formal params. The
#  intended use of this function is to generate a span tag whose id
#  is the same as the bytespan object's coref ID.
def generateTagOpen(id):
	ids = ""
	for assocId in bss[id].getAssocCorefIds():
		ids = ids + str(assocId) + ","
	ids = ids[:len(ids)-1]

	return "<span class=\"" + str(bss[id].getCorefId()) \
		+ "\" onmouseover=\"printAttributes(" + str(id) \
		+ ", " + str(bss[id].getStart()) + ", " \
		+ str(bss[id].getEnd()) + ");\" " \
		+ "assocCorefId=\"" + ids + "\" " \
		+ "style=\"border: solid 1px #000;padding: 0;\">"

def generateTagOpenTracking(id):
	ids = ""
	for assocId in bss2[id].getAssocCorefIds():
		ids = ids + str(assocId) + ","
	ids = ids[:len(ids)-1]

	return "<span class=\"" + str(bss2[id].getCorefId()) \
		+ "-tracking\" onmouseover=\"printAttributes(" + str(id) \
		+ ", " + str(bss2[id].getStart()) + ", " \
		+ str(bss2[id].getEnd()) + ");\" " \
		+ "assocCorefId=\"" + ids + "\" " \
		+ "style=\"border:solid 1px #000;padding: 0;\">"

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
	return "<span onclick=\"peek('" + str(itemId) \
		+ "')\" style=\"background-color:#DDD;cursor:pointer;\">" \
		+ str(itemId) \
		+ "</span>\t"

def parse_coref_output(file):
	# Open file from argument
	raw = open(file, 'r')

	# Create a list of all lines in the key
	lines = raw.readlines()

	# Create a list to hold the ByteSpan objects
	bss = list()

	# Process each line of the KEY file in succession, put in ByteSpan object
	for line in range(0, len(lines)):
		words = lines[line].split()
		byteRange = words[1].split(",")	#parse bytespan
		for word in words:
			if(word[0:9] == 'CorefID="'):
				# bytespans to numbers
				id = filter(lambda x: x in '1234567890', word)
			# DO WE WANT TO CHECK TO MAKE SURE THAT COREFID PROPERTY IS HERE?
		#store bytespan in object
		bs = ByteSpan(int(byteRange[0]), int(byteRange[1]), int(id))
		bss.append(bs)	#add object to list

	# Sort the list. Begin with starting position of bytespan; in the
	#  event of a tie, the largest bytespan comes first.
	return sorted(bss, cmp=orderBss)

def parse_muc_annots(file):
	# Coreferent NPs in the muc_annots file are (somewhat annoyingly)
	# annotated linearly.
	#
	# It's a bit tricky to explain. So first of all, EVERY SINGLE NP gets
	# its own ID field. If some NP is coreferent to another NP, then that is
	# noted in the REF field. So, for example, if you have two coreferent NPs
	# with IDs 5 and 12, then the NP with the ID of 12 would have a REF field
	# with a value of 5, which is the ID of the last NP that is coreferent.
	#
	# THE TRICKY BIT: The REF field contains only ONE value; in other words,
	# it represents the ID of the LAST NP that it is coreferent to. We can
	# derive the entire coref chain by searching backwards using the REF tags.
	# One example is, if we have a coref chain $ 4 <- 10 <- 15, then the way
	# to get all the coreferent NPs in that chain would be to traverse it.
	#
	# We modify this CS101 algorithm to get the coref chain for the
	# muc_annots.

	raw2 = open(file, 'r')  # open the raw text file
	lines2 = raw2.readlines()  # the muc_annots file, split into lines
	bss2 = list()  # holds all bytespan objects

	# will assign a "base" corefid to NPs, and thus help us track which
	# NPs are part of the same coref chain
	corefIdTracker = {}

	# Process each of muc_annots's lines
	for line2 in range(1, len(lines2)):
		words2 = lines2[line2].split()
		# NPs will are noted as type "COREF"
		if(words2[3] == "COREF"):
			ref = -1  # holds the value of REF; set to "safe" value
			currId = -1  # holds the current NP's ID field

			for word in words2:
				# set vars tracking this NP's REF and ID fields as we get them
				if(word[:5] == 'REF="'):
					ref = filter(lambda x: x in '1234567890', word)
				if(word[:4] == 'ID="'):
					currId = filter(lambda x: x in '1234567890', word)

			baseId = -1  # all coreferet NPs get the same baseId

			# Important: set the baseId
			#
			# IF the current NP had no ref tag, it is the first NP in a chain.
			# Thus, ITS ID BECOMES THE baseId!
			if(ref == -1):
				baseId = currId
			# ELSE, look at the baseId of the previous NP, set the current
			# NP's baseId to be that baseId, and continue
			else:
				baseId = corefIdTracker[ref]
			corefIdTracker[currId] = baseId

			# Finally, create the Bytespan object
			byteRange2 = words2[1].split(",")
			bs2 = ByteSpan(int(byteRange2[0]), int(byteRange2[1]), baseId)
			bss2.append(bs2)

	return sorted(bss2, cmp=orderBss)

def build_coref_bitvector(arr1, arr2, file):
	raw = open(file, 'rb')
	char = True  # current character
	charIndex = 0  # current character index
	i1 = 0
	i2 = 0
	currOpenArr1 = list()
	currOpenArr2 = list()
	vector = list()

	while(char):
		char = raw.read(1)
		vector.append([[],[]])

		while(i1 < len(arr1) and charIndex == arr1[i1].getStart()):
			currOpenArr1.append(i1)
			i1 += 1
		while(i2 < len(arr2) and charIndex == arr2[i2].getStart()):
			currOpenArr2.append(i2)
			i2 += 1

		for index in currOpenArr1:
			if(charIndex == arr1[index].getEnd()):
				vector[charIndex][0].append(arr1[index].getCorefId())
				currOpenArr1[currOpenArr1.index(index)] = -1
		for index in currOpenArr2:
			if(charIndex == arr2[index].getEnd()):
				vector[charIndex][1].append(arr2[index].getCorefId())
				currOpenArr2[currOpenArr2.index(index)] = -1

		currOpenArr1 = filter(lambda a: a != -1, currOpenArr1)
		currOpenArr2 = filter(lambda a: a != -1, currOpenArr2)

		for index in currOpenArr1:
			vector[charIndex][0].append(arr1[index].getCorefId())
		for index in currOpenArr2:
			vector[charIndex][1].append(arr2[index].getCorefId())
		charIndex += 1

	return vector

def add_assoc_corefids_from_bitvector(arr1, arr2, vector):
	# the following is a nested function that allows us to do the same
	# operation once each on both incoming arrays without code
	# duplication or another visible method
	def add_assoc_corefids_one_array(arr, numberOtherArray, vector):
		i1 = 0
		for charIndex in range(len(vector)):
			#print(str(charIndex) + " " + str(vector[charIndex]))  # Debug!
			while(i1 < len(arr) and charIndex == arr[i1].getStart()):
				# temporarily store coref ids in a hash table
				# this masks the "check for duplicates" step for us
				ids = {}

				# move one character forward continuously until bs ends
				tmpi = charIndex
				while(tmpi < len(vector) and tmpi <= arr[i1].getEnd()):
					# when we encounter corefid we haven't added, add to list
					for corefid in vector[tmpi][numberOtherArray]:
						ids[corefid] = corefid
					tmpi += 1

				for assocCorefId in ids:
					arr[i1].addAssocCorefId(assocCorefId)

				# once it ends, increment i1
				i1 += 1
		return arr

	arr1 = add_assoc_corefids_one_array(arr1, 1, vector)
	arr2 = add_assoc_corefids_one_array(arr2, 0, vector)
	return arr1, arr2

def write_outputfile_head(writeTo):
	start = '<html>\n\n<head>' + generateJs()
	start += '<link href="style.css" rel="stylesheet" type="text/css">'
	start += '</head>\n\n<body>\n<div id="attribute-display"></div>'
	writeTo.write(start)

#### CLI PROCESSING ####
####                ####

if sys.argv[1] == "open":
	# OPEN OVERLAY HTML HERE!
	os.system('open "http://www.google.com"')
	sys.exit()


#### SETUP ####
####       ####

# Parse coref_output file, put corefids into Bytespan objects,
# sort the objects
bss = parse_coref_output(sys.argv[1])

# Do the same for the muc_annots file
bss2 = parse_muc_annots(sys.argv[3])

# Build bit vector such that every element represents one character
# in the source document (usually called raw.txt). At each element,
# there will be a list of associated corefids that correspond to a
# noun phrase that this character lies directly in.
vector = build_coref_bitvector(bss, bss2, sys.argv[2])

# Finds out which corefids between two interpretations have words in
# common (i.e., are "associated") and put them inside internal lists
# that track these things. Note that this is a symmetrical operation,
# i.e., associated corefids are applied to both arrays we give
# as formal parameters to the method.
bss1, bss2 = add_assoc_corefids_from_bitvector(bss, bss2, vector)

# Make the file handlers we will use to write our output file (which
# is usually called out.html).
write = open(overlayFileTitle, 'w')
read = open(sys.argv[2], 'rb')

# Write the output file's head (e.g., "<html><head>..." and so on).
write_outputfile_head(write)

write.write('<div id="original">')
write.write('<span class="title">Name of interpretation file: <tt>' \
	+ str(sys.argv[1]) + '</tt></span><p><p>')

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
#   write the actual content into the overlay file. We handle this in a
#   special way: (a) if it's a newline, we also insert a < p> tag so that it
#   looks like it should when we open it in a browser; (b) in any other case,
#   we just the actual character.

char = True
charIndex = 0
bytespanIndex = 0
bytespanStack = list()

# Create div#original
while char:
	char = read.read(1) #1
	while bytespanIndex < len(bss) \
	and bss[bytespanIndex].getStart() == charIndex: #2
		write.write(generateTagOpen(bytespanIndex)) #2a
		bytespanStack.insert(0, bss[bytespanIndex]) #2b
		bytespanIndex+=1

	while len(bytespanStack) != 0 \
	and bytespanStack[0].getEnd() == charIndex: #3
		write.write(generateTagClose())
		bytespanStack.pop(0)

	# 4
	if char == "\n":
		write.write("<br>\n") #4a
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
write.write('<span class="title">Name of interpretation file: <tt>' \
	+ str(sys.argv[3]) + '</tt></span><p><p>')
while char:
	char = read.read(1) #1
	while bytespanIndex < len(bss2) \
	and bss2[bytespanIndex].getStart() == charIndex: #2
		write.write(generateTagOpenTracking(bytespanIndex)) #2a
		bytespanStack.insert(0, bss2[bytespanIndex]) #2b
		bytespanIndex+=1

	while len(bytespanStack) != 0 \
	and bytespanStack[0].getEnd() == charIndex: #3
		write.write(generateTagClose())
		bytespanStack.pop(0)

	# 4
	if char == "\n":
		write.write("<br>\n") #4a
	else:
		write.write(char) #4b
	charIndex+=1
write.write("</div>")

sys.exit()

