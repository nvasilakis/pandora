#!/bin/sh

##
# Generates the rules base (needs post processing) for all policies
##
exp="/scratch/safe/alpha_binaries/pump_alpha_sim/"

rm data

echo "Policy    Tags    Rules   N0   N_" >> data
echo "" >> data
echo "PTypes    30" >> data
echo "" >> data

##
# Mem Safety Rules
# t = unique allocs * 2 + 10 (rest of opgroups)
# This calculates UA only -- needs postproc
#/scratch/safe/alpha_binaries/traces/*/;
##
function ms {
  rm ./ms.rls
  for d in /scratch/safe/alpha_binaries/traces/*/; do
    if [[ -e "${d}alloc.out.gz" ]]; then
      r=$(zcat ${d}alloc.out.gz | sort -u | wc -l)
      echo "${d}  ${r}" >> ./ms.rls
    fi
  done
  ./post-proc.py ms ms.rls >> data
  echo "" >> data
}


##
# CFI
# t = {return,calls,br} * 4 + 10
# RoP: returns
# AD: calls
# Intra: returns + calls
# Inter: br
# ccfi: returns + calls + br
#/scratch/safe/alpha_binaries/alpha_sim/cfi/ccfi_stats/results/*; do
##
function cfi {
  now="cfi/"
  for config in allowdeny  ccfi  inter_proc  intra_proc  rop; do
    rm ./cfi.${config}.tgs ./cfi.${config}.rls
    cat ${exp}${now}${config}/tags/* >> ./cfi.${config}.tgs
    for f in ${exp}${now}${config}/rules/*1024.1024*; do
      echo ${f}
      r=$(cat ${f} | sort -u | wc -l)
      echo "${f}  ${r}" >> ./cfi.${config}.rls
    done
  done
}

function cfi1 {
  for f in ./cfi.*.rls; do
    ./post-proc.py cfi ${f} "rules" >> data
  done
  echo "" >> data
  for f in ./cfi.*.tgs; do
    ./post-proc.py cfi ${f} "tags" >> data
  done
  echo "" >> data
}

##
# Taint Tracking Rules
#
# /scratch/safe/alpha_binaries/alpha_sim/taint_tracking/stats
##
function tt {
  now="taint_tracking/"
  for config in io libs headers "functions"; do #
    rm ./tt.${config}.rls ./tt.${config}.tgs
    cat ${exp}${now}${config}/tags/* >> ./tt.${config}.tgs
    for f in ${exp}${now}${config}/rules/*1024.1024*; do
      echo ${f}
      r=$(cat ${f} | sort -u | wc -l)
      echo "${f}  ${r}" >> ./tt.${config}.rls
    done
  done
}

function tt1 {
  for f in ./tt*.rls; do
    ./post-proc.py tt ${f} "rules" >> data
  done
  echo "" >> data
  for f in ./tt*.tgs; do
    ./post-proc.py tt ${f} "tags" >> data
  done
  echo "" >> data
}

##
# Product LMs
#
# /scratch/safe/alpha_binaries/alpha_sim/taint_tracking/stats
##
function pl {
  now="products/"
  for config in tt_ccfi_types  tt_interproc_types; do #
    rm ./p.${config}.rls ./p.${config}.tgs
    cat ${exp}${now}${config}/tags/* >> ./p.${config}.tgs
    for f in ${exp}${now}${config}/rules/*1024.1024*; do
      echo ${f}
      r=$(cat ${f} | sort -u | wc -l)
      echo "${f}  ${r}" >> ./p.${config}.rls
    done
  done
}

function pl1 {
  for f in ./p*.rls; do
    ./post-proc.py pl ${f} "rules" >> data
  done
  echo "" >> data
  for f in ./p*.tgs; do
    ./post-proc.py pl ${f} "tags" >> data
  done
  echo "" >> data
}

ms
cfi
cfi1
tt
tt1
pl
pl1
