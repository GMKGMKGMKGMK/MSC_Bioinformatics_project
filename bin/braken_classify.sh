#!/bin/bash

# First argument is the input file
input_file=$1
output_file=$2

# Extract base name for output files
length=$(basename ${input_file} .fastq.gz)
echo ${input_file}
echo $length

#First get the kraken2 report
kraken2 -db /mnt/data/analysis/muhammedk/MSC4/step2/stepB/databases/New_kraken2_database \
	--report $output_file/${length}.kreport.txt \
	--threads 12 \
	${input_file} \
	--output $output_file/${length}.braken.txt 

#Then compute abundances from the reports with braken
bracken -d /mnt/data/analysis/muhammedk/MSC4/step2/stepB/databases/New_kraken2_database \
    -i $output_file/${length}.kreport.txt \
    -o $output_file/${length}.braken \
	-w $output_file/${length}.braken.report

