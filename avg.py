#!/usr/bin/env python

# Calculates the average of CFI stats
# e.g., returns, calls, branches

with open("stats", "r") as f:
  lines = f.readlines()
  ln = 0
# four counters
  ret = 0
  cal = 0
  bra = 0
  for line in lines:
    if "#" in line:
      print (line + ".. skipping")
      continue
    print(line.split())
    if  "returns" in line:
      ret += int(line.split()[1])
    if  "calls" in line:
      cal += int(line.split()[1])
    if  "branches" in line:
      bra += int(line.split()[1])
    ln += 1
  print("Returns : " + str(ret/float(ln)))
  print("Calls   : " + str(cal/float(ln)))
  print("Branches: " + str(bra/float(ln)))
