import sys
from Bio import SeqIO
import os
import pandas as pd
# Initialize a list to hold dictionaries, which will then be converted to a DataFrame
data = []
total_bases = 0

# Directory provided as a command line argument
directory = sys.argv[1]

# Output file provided as a command line argument
output_file = sys.argv[2]

# Walk through all files in the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.fasta'):
            # Parse the FASTA file
            for seq_record in SeqIO.parse(os.path.join(root, file), 'fasta'):
                # Count the bases and add them to the total
                num_bases = len(seq_record)
                total_bases += num_bases
                
                # Check if the id contains a space
                if ' ' in seq_record.description:
                    # If a space is present, split the id on the first space to separate the identifier from the species
                    id, species = seq_record.description.split(' ',1)
                else:
                    # If a space is not present, assign the entire id to id and use a placeholder for species
                    id = seq_record.description
                    species = 'Unknown'
                data.append({'id': id, 'species': species, 'num_bases': num_bases})

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Calculate the percentages
df['percentage'] = df['num_bases'] / total_bases * 100

# Add the total row
df = df.append({'id': 'Total', 'species': 'All', 'num_bases': total_bases, 'percentage': 100}, ignore_index=True)

# Write the DataFrame to the TSV file specified by the command line argument
df.to_csv(output_file, sep=',', index=False)
