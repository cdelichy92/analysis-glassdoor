#!/usr/bin/env python2.7

import sys

for line in sys.stdin.replace('\r','\n'):
    print "___________________"
    elems = line.split("\t")
    print elems
