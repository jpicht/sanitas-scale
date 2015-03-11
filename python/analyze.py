#!/usr/bin/env python

import sys, os

BLOCK_SIZE=128

def readPerson(f):
	"""Read all data for one profile from a file like object."""
	return {
		'weight': f.read(BLOCK_SIZE),
		'body_fat': f.read(BLOCK_SIZE),
		'water_content': f.read(BLOCK_SIZE),
		'muscle_content': f.read(BLOCK_SIZE),
		'date': f.read(BLOCK_SIZE),
		'time': f.read(BLOCK_SIZE)
	}

def parseDate(raw):
	return ( 1920 + (raw >> 9), (raw >> 5) & 15, raw & 31 )

def formatDate(d):
	return "{2:02d}.{1:02d}.{0:04d}".format( *d )

class p16(object):
	"""Parser for 16 bit data blocks"""
	def __init__(self, buffer, suffix=""):
		self.buffer = buffer
		self.suffix = suffix

	def get(self, num):
		return ord(self.buffer[num*2]) << 8 | ord(self.buffer[num*2+1])

	def getf(self, num):
		return "{0:5d}".format(self.get(num)) + self.suffix

class p16time(p16):
	"""Parser for the 16 bit time format"""
	def get(self, num):
		return ord(self.buffer[num*2]), ord(self.buffer[num*2+1])

	def getf(self, num):
		return "{0:02d}:{1:02d}".format( *self.get(num) ) + self.suffix

class p16date(p16):
	"""Parser for the 16 bit date format"""
	def get(self, num):
		raw = p16.get(self, num)
		return parseDate(raw)

	def getf(self, num):
		return formatDate(self.get(num)) + self.suffix

class p16p1(p16):
	"""Parser for the weight block"""
	def get(self, num):
		return p16.get(self, num) / 10.

	def getf(self, num):
		return "{0:5.1f}".format(self.get(num)) + self.suffix
		

class meta1(object):
	"""Parser for the meta data block 1"""
	OFFSET_DOB     = 2
	OFFSET_COUNTER = 5
	OFFSET_HEIGHT  = 1
	OFFSET_PERSON  = 8

	def __init__(self, buffer):
		self.buffer = buffer

	def read16(self, person, offset):
		offset = person * meta1.OFFSET_PERSON + meta1.OFFSET_DOB
		return  (ord(self.buffer[offset]) << 8) | ord(self.buffer[offset + 1])

	def getActive(self, person = 0):
		if self.getHeight(person) > 0:
			return True
		return False

	def getDob(self, person = 0):
		return formatDate(parseDate(self.read16(person, meta1.OFFSET_DOB)))

	def getHeight(self, person = 0):
		return ord(self.buffer[person * meta1.OFFSET_PERSON + meta1.OFFSET_HEIGHT])

	def getCount(self, person = 0):
		return ord(self.buffer[person * meta1.OFFSET_PERSON + meta1.OFFSET_COUNTER])

class personData(object):
	"""Encapsulation for the decoded data of one profile"""
	def __init__(self, data):
		self.weight   = p16p1(data['weight'], " kg")
		self.fat      = p16p1(data['body_fat'], "% fat")
		self.water    = p16p1(data['water_content'], "% water")
		self.muscle   = p16p1(data['muscle_content'], "% muscle")
		self.date     = p16date(data['date'])
		self.time     = p16time(data['time'])

	def get(self, idx):
		return (
			self.date.get(idx),
			self.time.get(idx),
			self.weight.get(idx),
			self.fat.get(idx),
			self.water.get(idx),
			self.muscle.get(idx),
		)

	def getf(self, idx):
		return (
			self.date.getf(idx),
			self.time.getf(idx),
			self.weight.getf(idx),
			self.fat.getf(idx),
			self.water.getf(idx),
			self.muscle.getf(idx),
		)

class analyze(object):
	def __init__(self, fN):
		"""Parser function for one file"""
		if os.lstat(fN).st_size != 8192:
			print fN + ": Unknown file size!"
			return

		f = file(fN)
		data = []
		for p in range(10):
			data.append(readPerson(f))

		# the next two blocks seem to be unused
		skipA = f.read(BLOCK_SIZE)
		skipB = f.read(BLOCK_SIZE)
		metaA = f.read(BLOCK_SIZE)
		metaB = f.read(BLOCK_SIZE)

		self.meta1 = meta1(metaA)
		self.data = [personData(x) for x in data]

	def dump(self):
		for p in range(10):
			if not self.meta1.getActive(p):
				continue
			print "Person %d" % p
			print "--------"
			print "DOB:     %s" % self.meta1.getDob(p)
			print "Height:  %d cm" % self.meta1.getHeight(p)
			print "Counter: %d measurements" % self.meta1.getCount(p)
			print

			for i in range(self.meta1.getCount()):
				print " ".join( self.data[p].getf(i) )

if __name__ == "__main__":
	for f in sys.argv[1:]:
		analyze(f).dump()

