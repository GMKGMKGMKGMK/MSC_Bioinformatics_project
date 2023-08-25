#!/usr/env python3

# Import necessary libraries
from Bio import SeqIO
import sys

# Gather command line arguments
input_file = sys.argv[1]
output_file = sys.argv[2]
minimum_RL = sys.argv[3]
maximum_RL = sys.argv[4]
steps_RL = sys.argv[5]


# Convert input arguments to respective data types
minimum_RL = int(minimum_RL)
maximum_RL = int(maximum_RL)
steps_RL = int(steps_RL)

# Loop through specified range and truncate sequences to each target length
# Then, write truncated sequences to corresponding output files
for i in range(minimum_RL, maximum_RL + steps_RL, steps_RL):
    target_length = i
    output_file1 = output_file + "/" + str(target_length) + "_adjusted.fastq"
    with open(output_file1, 'w') as out_handle:
        for record in SeqIO.parse(input_file, 'fastq'):
            record = record[:target_length]
            SeqIO.write(record, out_handle, 'fastq')
