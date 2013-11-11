#!/bin/bash
  
##
# A script that processes SPEC benchmarks source repository to
# initialize TT tags
##


# get source directory to lookup
src="./my/taint/" # for gcc

glibc="./glibc-1.09/"

#ctags 5.8 instead of built-in
/usr/bin/ctags -x --c-kinds=fp ${src}*.c | grep ' function ' | awk '{print $1 " " $4}' | sed "s;${src};;" > functions.lib

#parse libc
/usr/bin/ctags -x --c-kinds=fp ${glibc}**/*.c | grep ' function ' | awk '{print $1 " " $4}' | sed "s;${glibc};;" >> functions.lib

# add -asm -ctags
python extract_files.py  --asm taint.asm
