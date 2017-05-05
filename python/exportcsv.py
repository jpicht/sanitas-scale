#!/usr/bin/env python

from analyze import analyze, formatDate
import sys

def formatLine(person, date, time, weight, fat, water, muscle):
	return ";".join([str(x) for x in (person, formatDate(date) + " {0:02d}:{1:02d}".format(*time), weight, fat, water, muscle)])

def main():
	if len(sys.argv) != 2:
		sys.stderr.write("Syntax:\n  {0} <input file>".format(sys.argv[0]))
		sys.exit(1)

	a = analyze(sys.argv[1])
	for p in range(10):
		if not a.meta1.getActive(p):
			continue

		for i in range(a.meta1.getCount(p)):
			print formatLine(p, *a.data[p].get(i))

if __name__ == "__main__":
	main()
