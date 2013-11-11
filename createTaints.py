#!/usr/bin/env python

# parse a headers.c file
functions = []
libraries = []
one = []
with open("headers.lib", "r") as f:
  lines = f.readlines()
  for line in lines:
    functions.append(line.split()[0] + " " + line.split()[0])
    libraries.append(line.split()[0] + " " + line.split()[1].split("/")[0])
    one.append(line.split()[0] + " one.lib")

with open("one.lib", "w") as f:
  f.write("\n".join(one))

with open("functions.lib", "w") as f:
  f.write("\n".join(functions))

with open("libraries.lib", "w") as f:
  f.write("\n".join(libraries))

