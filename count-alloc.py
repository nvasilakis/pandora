#!/usr/bin/env python

##
# Aggregate and summarize (output mean) of number of 
# rules for memory safety 
## 

import gzip
import sys

def unique(fname):
  """Grab all the unique addresses"""
  addresses = []
  with gzip.open(fname, "rb") as f:
    lines = f.readlines()
    for line in lines:
      #print("["+line.split()[1]+"]")
      if line.split()[0] not in addresses:
        addresses.append(line.split()[0])
  return addresses 

def aggregate():
  a = unique(sys.argv[1])
  print(sys.argv[1] + " " + str(len(a)))

def summarize():
  s = 0
  i = 0
  with open("./memory-allocs.nvas", "r") as f:
    lines = f.readlines()
    for line in lines:
      s += int(line.split()[1])
      i += 1
  w = (s/float(i))
  print w
  return  w

summarize()
