#!/usr/bin/env python

import sys, os

# the file constists of 64 blocks with 128 bytes each
#
#  #    description  bytes  interpretation
#  0: P0 weight          2           100 g
#  1: P0 % body fat      2            .1 %
#  2: P0 % water         2            .1 %
#  3: P0 % muscle        2            .1 %
#  4: P0 date            2               ?
#  5: P0 time            2  [hour, minute]
#
#  6: P1?
#  7: P1?
#  8: P1?
#  9: P1?
# 10: P1?
# 11: P1?
#
# ...
#
# 54: P9?
# 55: P9?
# 56: P9?
# 57: P9?
# 58: P9?
# 59: P9?
# 60: ??
# 61: ??
# 62: META1
# 63: META2
#
# date format:
#   bit  : f e d c b a 9 8 7 6 5 4 3 2 1 0
#   value: 1 0 1 1 1 1 0 0 0 1 1 0 1 0 0 1
#         |-------------|-------|--------|
#          year-1921(?)  month    day
#
# META1:
# 62.00: ??
# 62.01: height
# 62.05: counter

BLOCK_SIZE=128

def readPerson(f):
	return {
		'weight': f.read(BLOCK_SIZE),
		'body_fat': f.read(BLOCK_SIZE),
		'water_content': f.read(BLOCK_SIZE),
		'muscle_content': f.read(BLOCK_SIZE),
		'date': f.read(BLOCK_SIZE),
		'time': f.read(BLOCK_SIZE)
	}

def dumpHex(buff, lineWidth = 16):
	for idx in range(len(buff)):
		if idx > 0 and idx % lineWidth == 0:
			print
		print "%02x" % ord(buff[idx]),
	print

class p16(object):
	def __init__(self, buffer, suffix=""):
		self.buffer = buffer
		self.suffix = suffix

	def get(self, num):
		return ord(self.buffer[num*2]) << 8 | ord(self.buffer[num*2+1])

	def getf(self, num):
		return "{0:5d}".format(self.get(num)) + self.suffix

class p16time(p16):
	def get(self, num):
		return ord(self.buffer[num*2]), ord(self.buffer[num*2+1])

	def getf(self, num):
		return "{0:02d}:{1:02d}".format( *self.get(num) ) + self.suffix

class p16date(p16):
	def get(self, num):
		raw = p16.get(self, num)
		return ( 1921 + (raw >> 9), (raw >> 5) & 15, raw & 31 )

	def getf(self, num):
		return "{2:02d}.{1:02d}.{0:04d}".format( *self.get(num) ) + self.suffix

class p16p1(p16):
	def get(self, num):
		return p16.get(self, num) / 10.

	def getf(self, num):
		return "{0:5.1f}".format(self.get(num)) + self.suffix
		

class meta1(object):
	OFFSET_HEIGHT  = 1
	OFFSET_COUNTER = 5

	OFFSET_PERSON  = 8

	def __init__(self, buffer):
		self.buffer = buffer

	def getHeight(self, person = 0):
		return ord(self.buffer[person * meta1.OFFSET_PERSON + meta1.OFFSET_HEIGHT])

	def getCount(self, person = 0):
		return ord(self.buffer[person * meta1.OFFSET_PERSON + meta1.OFFSET_COUNTER])

class personData(object):
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

def analyze(fN):
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

	m = meta1(metaA)
	print "Person 0"
	print "--------"
	print "Height:  %3d cm" % m.getHeight()
	print "Counter: %3d measurements" % m.getCount()
	print

	w = p16p1(data[0]['weight'])
	for i in range(m.getCount()):
		print "Weight %2d: %.1f kg" % (i, w.get(i))

	d = personData(data[0])
	for i in range(m.getCount()):
		print " ".join( d.getf(i) )

	# dumpHex(metaA)
	# dumpHex(metaB)

if __name__ == "__main__":
	for f in sys.argv[1:]:
		analyze(f)

