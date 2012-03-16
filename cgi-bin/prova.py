#!/usr/bin/python

import cgi


def main():
	fs = cgi.FieldStorage()
	print "Content-type: text/plain\n"
	if "name" in fs:
	  	print str(fs["nome"].value)
	else:
		print "nome not found"


main()
