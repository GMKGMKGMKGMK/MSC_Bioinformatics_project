#!/bin/bash

# First argument is the input file
input_file=$1
output_file=$2

# Extract base name for output files
length=$(basename ${input_file} .fastq.gz)
echo ${input_file}
echo $length

# Classify with Centrifuge
centrifuge --mm -q \
    -x /mnt/data/analysis/muhammedk/MSC4/step2/stepB/databases/centrifuge_2023_05_16/ex \
    -U ${input_file} \
    --report-file $output_file/centrifuge_${length}_Cent_K1.report \
    -S $output_file/centrifuge_${length}.results \
    --threads 12 \
    --min-hitlen 16 -k 1

# Classify with Kraken2
kraken2 -db /mnt/data/analysis/muhammedk/MSC4/step2/stepB/databases/New_kraken2_database \
	--report $output_file/kraken_${length}.kreport.txt \
	--threads 12 \
	${input_file} \
	--output $output_file/kraken_${length}.kraken2.txt 

# Classsify with Braken
bracken -d /mnt/data/analysis/muhammedk/MSC4/step2/stepB/databases/New_kraken2_database \
    -i $output_file/kraken_${length}.kreport.txt \
    -o $output_file/braken_${length}.braken \
    -w $output_file/braken_${length}.braken.report
