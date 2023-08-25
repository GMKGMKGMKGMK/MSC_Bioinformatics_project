#!/bin/bash

# Base directory for search
base_dir="/mnt/data/analysis/muhammedk/MSC4/Nextflow2/test_classification"

# Directories to be searched
target_dirs=("${base_dir}/centrifuge" "${base_dir}/kraken" "${base_dir}/braken")

# File patterns to look for
patterns=("ecoli" "kpneumo" "MRSA" "Pa01")

# Destination directory for matched files
dest_root="/mnt/data/analysis/muhammedk/MSC4/Nextflow2/test_by_species"

# Iterate over the patterns
for pattern in "${patterns[@]}"; do
    # Create a directory for the current pattern
    mkdir -p "$dest_root/$pattern"
    
    # Search and copy matching files to the destination directory
    for dir in "${target_dirs[@]}"; do
        find "$dir" -type f -iname "*${pattern}*" -exec cp {} "$dest_root/$pattern/" \;
    done
done
