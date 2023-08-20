#!/usr/env python3

# Import necessary libraries
from Bio import SeqIO
import sys
import os

# Gather command line arguments
input_file = sys.argv[1]
output_file = sys.argv[2]
braken = sys.argv[3]
kraken = sys.argv[4]
centrifuge = sys.argv[5]

# Convert input arguments to respective data types
braken_val = int(braken)
kraken_val = int(kraken)
centrifuge_val = int(centrifuge)

# Extract base name from the input file name
filename = os.path.basename(input_file)
base_name = filename.split(".")[0]

# Truncate sequences to the specified length for Braken and write to an output file
target_length = braken_val
output_file1 = output_file + "/" + "braken_" + str(base_name) + "_" + str(braken_val) + ".fastq"
with open(output_file1, 'w') as out_handle:
    for record in SeqIO.parse(input_file, 'fastq'):
        record = record[:target_length]
        SeqIO.write(record, out_handle, 'fastq')

# Truncate sequences to the specified length for Kraken and write to an output file
target_length = kraken_val
output_file1 = output_file + "/" + "kraken_" + str(base_name) + "_" + str(kraken_val) + ".fastq"
with open(output_file1, 'w') as out_handle:
    for record in SeqIO.parse(input_file, 'fastq'):
        record = record[:target_length]
        SeqIO.write(record, out_handle, 'fastq')

# Truncate sequences to the specified length for Centrifuge and write to an output file
target_length = centrifuge_val
output_file1 = output_file + "/" + "centrifuge_" + str(base_name) + "_" + str(centrifuge_val) + ".fastq"
with open(output_file1, 'w') as out_handle:
    for record in SeqIO.parse(input_file, 'fastq'):
        record = record[:target_length]
        SeqIO.write(record, out_handle, 'fastq')
