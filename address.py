#!/usr/bin/env python

# Grab address boundaries of memory allocations and frees from the
# assembly tracefile

import sys

#bms="/scratch/safe/udit/asplos2014/asplos2014_binaries/asm"
alloc="<__libc_malloc>:"
free="<__cfree>:"
bm = sys.argv[1].rsplit('/',1)[-1]
bmasm = sys.argv[1]

inAlloc = False
inFree  = False
inline = 0

print("BM" + bm)

with open(bmasm,'r') as f:
  lines = f.readlines()
  for line in lines:
    if alloc in line:
      print("found alloc:  " + line)
      inline = 0
      inAlloc = True
    elif free in line:
      print("found free:  " + line)
      inline = 0
      inFree = True
    if inAlloc and inline == 3:
      with open(bm+".malloc", 'w') as f:
        datum = "00" + line.split(":")[0].strip()
        print("ret: "+datum)
        f.write(datum)
    if inAlloc and "ret" in line:
      with open(bm+".ret", 'w') as f:
        datum = "00" + line.split(":")[0].strip()
        print("ret: "+datum)
        f.write(datum)
      inline = 0
      inAlloc = False
    if inFree and inline == 3:
      with open(bm+".free", 'w') as f:
        datum = "00" + line.split(":")[0].strip()
        print("free: " + datum)
        f.write(datum)
    if inFree and "ret" in line:
      inline = 0
      inFree = False
    if (inAlloc or inFree) and inline < 4:
      if inAlloc:
        print("in alloc: " + str(inline))
      if inFree:
        print("in free: " + str(inline))
      inline += 1

