#!/usr/bin/env python

import sys

# Calculates the average of CFI stats
# e.g., returns, calls, branches


def ms(fname):
  """Process memory safety"""
  with open(fname, "r") as f:
    lines = f.readlines()
    ln = 0
    rules = 0
    for line in lines:
      if "#" in line:
        print (line + ".. skipping")
        continue
      rules += int(line.split()[1])
      ln += 1
  print("Mem Safety: " + str(rules/float(ln)) + " \t " +  str(2*rules/float(ln) + 10))



def cfi_rules(fname):
  """Process CFI"""
  with open(fname, "r") as f:
    lines = f.readlines()
    ln = 0
    rules = 0
    # four counters
    for line in lines:
      if "#" in line:
        print (line + ".. skipping")
        continue
      #print(line.split())
      ln += 1
      rules += int(line.split()[1])
    print(fname.replace("./cfi.", "").replace(".rls","") + " Rules: " + str(rules/float(ln)))

def cfi_tags(fname):
  with open(fname, "r") as f:
    lines = f.readlines()
    ln = 0
  # start, finish tags
    sta = 0
    fin = 0
    for line in lines:
      if "#" in line:
        print (line + ".. skipping")
        continue
      #print(line.split())
      sta += int(line.split()[0])
      fin += int(line.split()[1])
      ln += 1
    print(fname.replace("./cfi.", "").replace(".tgs","") + " Tags: " + str(sta/float(ln)) + " " + str(fin/float(ln)))

def tt_rules(fname):
  """Process taint tracking"""
  with open(fname, "r") as f:
    lines = f.readlines()
    ln = 0
    rules = 0
    for line in lines:
      if "#" in line:
        print (line + ".. skipping")
        continue
      ln += 1
      rules += int(line.split()[1])
  print(fname.replace("./tt.", "").replace(".rls","") + " Rules: " + str(rules/float(ln)))

def tt_tags(fname):
  with open(fname, "r") as f:
    lines = f.readlines()
    ln = 0
    sta = 0
    fin = 0
    for line in lines:
      if "#" in line:
        print (line + ".. skipping")
        continue
      #print(line.split())
      sta += int(line.split()[0])
      fin += int(line.split()[1])
      ln += 1
    print(fname.replace("./tt.", "").replace(".tgs","") + " Tags: " + str(sta/float(ln)) + " " + str(fin/float(ln)))

def p_rules(fname):
  """Product LM rule processing"""
  with open(fname, "r") as f:
    lines = f.readlines()
    ln = 0
    rules = 0
    for line in lines:
      if "#" in line:
        print (line + ".. skipping")
        continue
      ln += 1
      rules += int(line.split()[1])
  print(fname.replace("./p.", "").replace(".rls","") + " Rules: " + str(rules/float(ln)))

def p_tags(fname):
  with open(fname, "r") as f:
    lines = f.readlines()
    ln = 0
    sta = 0
    fin = 0
    for line in lines:
      if "#" in line:
        print (line + ".. skipping")
        continue
      #print(line.split())
      sta += int(line.split()[0])
      fin += int(line.split()[1])
      ln += 1
    print(fname.replace("./p.", "").replace(".tgs","") + " Tags: " + str(sta/float(ln)) + " " + str(fin/float(ln)))

call = {"ms": ms, 
        "cfirules":cfi_rules, 
        "cfitags":cfi_tags,
        "ttrules": tt_rules,
        "tttags": tt_tags,
        "plrules": p_rules,
        "pltags": p_tags}

sub = "" if not len(sys.argv) > 3 else sys.argv[3]
call[(sys.argv[1]+sub)](sys.argv[2])
