#!/bin/sh

# Get the number of rules for each configuration of taint tracking
# based on simulation output

# /scratch/safe/alpha_binaries/alpha_sim/taint_tracking/stats
for config in io libs headers "functions"; do #
  rm ~/${config}_1.rls
  echo ${config}
  #cd "/scratch/safe/alpha_binaries/alpha_sim/taint_tracking/stats/${config}/results/"
  for f in /scratch/safe/alpha_binaries/alpha_sim/taint_tracking/stats/${config}/results/*.rules; do
    echo ${f}
    r=$(cat ${f} | sort -u | wc -l)
    echo "${f}  ${r}" >> ~/${config}_1.rls
    #python ~/extract-uniques.py ${f} >> ~/${config}.rls
  done
done

