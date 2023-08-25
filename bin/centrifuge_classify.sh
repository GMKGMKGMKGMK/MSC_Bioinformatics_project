#!/bin/bash

# First argument is the input file
input_file=$1
output_file=$2

# Extract base name for output files
length=$(basename ${input_file} .fastq.gz)
echo ${input_file}
echo $length

#Classify file with centrifuge
centrifuge --mm -q \
    -x /mnt/data/analysis/muhammedk/MSC4/step2/stepB/databases/centrifuge_2023_05_16/ex \
    -U ${input_file} \
    --report-file $output_file/${length}_Cent_K1.report \
    -S $output_file/${length}.results \
    --threads 12 \
    --min-hitlen 16 -k 1