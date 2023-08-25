#!/bin/bash

# Read the text file line by line
while read -r line; do
    # Split the line into words
    words=($line)
    
    # Check the first word and assign the value to the appropriate variable
    case "${words[0]}" in
        "Braken_Classified_Percentage") braken_percentage=${words[1]};;
        "Kraken2_Classified_Percentage") kraken2_percentage=${words[1]};;
        "Centrifuge_Classified_Percentage") centrifuge_percentage=${words[1]};;
    esac
done < "/mnt/data/analysis/muhammedk/MSC4/Nextflow2/plots/closest_RL1.txt"

# Print the extracted percentages
echo "Braken_Percentage: $braken_percentage"
echo "Kraken2_Percentage: $kraken2_percentage"
echo "Centrifuge_Percentage: $centrifuge_percentage"
