#!/bin/bash

# First argument is the input file
input_file=$1
output_file=$2

# Extract base name for output files
length=$(basename ${input_file} .fastq.gz)
echo ${input_file}
echo $length

# Classify file with Kraken2
kraken2 -db /mnt/data/analysis/muhammedk/MSC4/step2/stepB/databases/New_kraken2_database \
	--report $output_file/${length}.kreport.txt \
	--threads 12 \
	${input_file} \
	--output $output_file/${length}.kraken2.txt 