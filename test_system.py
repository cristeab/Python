#!/usr/bin/env python

from subprocess import call
from os import geteuid
from sys import exit

device="/dev/sda"
test_prog1="/home/bogdan/C++/TempPrj/bin/archive_data"

if geteuid() != 0:
	print "you need to run this script as root"
	exit(1)

retcode = call(["/sbin/hdparm", "-t", "-T", device])
if 0 != retcode:
	print "error when running hdparm"

retcode = call([test_prog1])
if 0 != retcode:
	print "error when running ", test_prog1

retcode = call([test_prog1, "-s", "10"])
if 0 != retcode:
        print "error when running ", test_prog1

retcode = call([test_prog1, "-p", "fifo"])
if 0 != retcode:
        print "error when running ", test_prog1

retcode = call([test_prog1, "-p", "fifo", "-s", "10"])
if 0 != retcode:
        print "error when running ", test_prog1

retcode = call([test_prog1, "-p", "rr"])
if 0 != retcode:
        print "error when running ", test_prog1

retcode = call([test_prog1, "-p", "rr", "-s", "10"])
if 0 != retcode:
       print "error when running ", test_prog1
