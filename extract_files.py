#!/usr/bin/env python

import re
import argparse

# you can tweak the defaults by:
#  --asm <objdump output>  (default: gcc.asm)
#  --ctags <ctags output>  (default: functions.lib)
# otherwise mmtgs.sha <SPECMark source> does both

class cFunction():
  """Information per C function"""
  def __init__(self):
    self.addresses = []
    # another idea would be [(start,end)]
    self.count = 1
    self.fpaths = []
    self.library = -1
  def add(self):
    """Increase by One"""
    self.count += 1

def parseAsm(fname):
  """Parse .asm to fetch address range and functions
  Given an filename it creates a map from function names to cFunction
  objects """
  functions = {}
  prev = "" # previous address
  prevPrime = "" # quickfix for the case of disassemble line
  lastFun = "" # cache previous line for function return
  f = open(fname)
  i=0;
  for l in f.readlines():
    if "Disassembly of section .rdata:" in l:
      break
    match = re.search("<.*>:$", l)
    line = l.replace("\n", "").split()
    #print(line)
    if match is not None and l[0] != " " :
      fun = line[1][1:-2] #substring
      lastFun = fun
      start = line[0]
      if fun in functions:
        functions[fun].add()
      else:
        fu = cFunction()
        fu.count= 1
        functions[fun] = fu
      i += 1;
    # empty line *after* we see first function directive or rdata line
    # at the same time lastFun is kept so we find where to append ending
    # address
    elif ( (len(line) <= 1 and lastFun in functions) or 
        ("Disassembly" in line and ".init:" not in line)):
      end = prev[:-1]
#      if ("Disassembly" in line):
#        print("==>" + start + " | 00" + end)
#      else:
#        print("" + start + " | 00" + end)
      a = (start, "00" + end) #hack to elongate end address
      #if len(functions[lastFun].addresses) > 1:
      #  print lastFun
      functions[lastFun].addresses.append(a) 
# this shows no duplicates till here
      #print len(functions[lastFun].addresses)
      lastFun = ""
    elif len(line) > 0:
      prev2 = prev # record two values before
      prev = line[0]
  print ("functions:" + str(len(functions)) + " Unique:" + str(len(list(set(functions)))))
  return functions

def output(maxValidTaint, functions):
  """Write results to file; maxValidTaint is the maximum taint value 
  from internal functioins/files/libraries -- after that, taints come
  from external sources (e.g., glibc etc.)
  """
  valid = []
  invalid = []
  for f in (sorted(functions.iterkeys())): #in-order
    #print functions[f].addresses
    for i in functions[f].addresses:
      if functions[f].library != -1: #this should be file \/
        valid.append(i[0] + " " + i[1] + " " + str(functions[f].library) + "\n")
      else: # there was no library found for this
        invalid.append(i[0] + " " + i[1] + " " + str(maxValidTaint)+"\n") #" "+f+"\n") # output also functions
        maxValidTaint+=1
  #print ("Total Tags: " + str(maxValidTaint))
  return (valid, invalid)

def parseCTags(functions, fname):
  """Parse .lib output from the ctags script"""
  resolve = {} # library file-> id
  f = open(fname)
  i = 1 # start taints from 1

  checkFns = []
  doubleCheck = []
  for l in f.readlines():
    fun = l.split()[0]
    lib = l.split()[1]
    # ctags (rightly) returns multiple copies of the same function
    # so we need to filter duplicates
    if fun in checkFns:
      continue
    checkFns.append(fun)
    if fun in functions:
      # assign what it was or a new Taint Tag
      dupl = ""
      #print len(functions[fun].addresses)
      for z in functions[fun].addresses:
        dupl += z[0] + " " + z[1]
      doubleCheck.append(dupl)
      if (lib in resolve):
        resolve[lib] = resolve[lib] 
      else:
        i += 1 #new lib found = new tag assigned
        resolve[lib] = i
      functions[fun].library = resolve[lib]
  print ("Internal tags: " + str(i))
  with open("dbg", "w") as f:
    f.write("\n" + "\n".join(doubleCheck))
  return (i, functions)

def runTests(args):
  """Run the tests"""
  e = parseAsm(args.asm) 
  for l in e:
    for a in e[l].addresses:
      if a[0] == "00400140": # double?
        print ""
        #print ("found: " + l)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--asm", 
              help="The input asm file containing assembly code")
  parser.add_argument("-c", "--ctags",
              help="The ctags file containing functions declarations per src file")
  args = parser.parse_args()
  test = False
  if test:
    runTests(args)
  else:
    e = parseAsm("gcc.asm" if args.asm == None else args.asm)
    (maxTaint, fns) = parseCTags(e,("headers.lib" if args.ctags == None else args.ctags))
    (v,i) = output(maxTaint, fns)
    # append invalid after valid
    v = list(set(v))
    i = list(set(i))
    with open("init_taints." + (args.ctags).split(".")[0], 'w') as f:
      f.write("".join(v))
    with open("init_taints." + (args.ctags).split(".")[0], 'a') as f:
      f.write( "" + "".join(i))
