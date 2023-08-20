import matplotlib.pyplot as plt
import numpy as np
import sys

def parse_results_Cent(results_file):
    taxon_levels = {'species': 0, 'genus': 0, 'family': 0, 'order': 0, 'class': 0, 'phylum': 0, 'no rank': 0}

    with open(results_file, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                classification = fields[2].split(';')
                taxon_level = classification[0]
                if taxon_level in taxon_levels:
                    taxon_levels[taxon_level] += 1
    return taxon_levels

def parse_results_kra(results_file):
    taxon_levels = {'U': 0}

    with open(results_file, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                classification = fields[3].split(';')
                taxon_level = classification[0]
                if taxon_level in taxon_levels:
                    unclassified = float(fields[0].split(';')[0])
                    classified = 100.0 - unclassified
                    taxon_levels[taxon_level] += classified

    return taxon_levels

kraken2_results_directory = sys.argv[1]
Cent_results_directory = sys.argv[2]
braken_results_directory= sys.argv[3]
MIN=int(sys.argv[4])
MAX=int(sys.argv[5])
STEPS=int(sys.argv[6])
outdir=sys.argv[7]

# Read lengths and directories
read_lengths = [length for length in range(MIN, MAX, STEPS)]

# Calculate Kraken2 taxon levels at each read length
kraken2_taxon_levels = []
braken_taxon_levels = []
for length in read_lengths:
    kraken2_results_file = kraken2_results_directory + f"/kraken_{length}_adjusted.kreport.txt"
    kraken2_results = parse_results_kra(kraken2_results_file)
    kraken2_taxon_levels.append(kraken2_results['U'])
    braken_results_file = braken_results_directory + f"/braken_{length}_adjusted.braken.report"
    braken_results = parse_results_kra(braken_results_file)
    adjusted_braken_result = kraken2_results['U'] 
    braken_taxon_levels.append(adjusted_braken_result)

kraken2_results_file = kraken2_results_directory + f"/kraken_Combined.kreport.txt"
kraken2_results = parse_results_kra(kraken2_results_file)
kraken2_taxon_levels.append(kraken2_results['U'])
braken_results_file = braken_results_directory + f"/braken_Combined.braken.report"
braken_results = parse_results_kra(braken_results_file)
adjusted_braken_result_combined = kraken2_results['U']
braken_taxon_levels.append(adjusted_braken_result_combined)

# Calculate Centrifuge taxon levels at each read length
Cent_taxon_levels = []
for length in read_lengths:
    Cent_results_file = Cent_results_directory + f"/centrifuge_{length}_adjusted_Cent_K1.report"
    Cent_results = parse_results_Cent(Cent_results_file)
    Cent_taxon_levels.append(Cent_results)

Cent_results_file = Cent_results_directory + f"/centrifuge_Combined_Cent_K1.report"
Cent_results = parse_results_Cent(Cent_results_file)
Cent_taxon_levels.append(Cent_results)

# Calculate percentages for Centrifuge
cent_no_rank_percentage_data = np.zeros(len(Cent_taxon_levels))

for i, Cent_results in enumerate(Cent_taxon_levels):
    total_count = sum(Cent_results.values())
    if total_count != 0:
        cent_no_rank_percentage_data[i] = 100 - (Cent_results['no rank'] / total_count) * 100

# Adjust the x-values
read_lengths.append("Combined")
x_ticks = np.arange(len(read_lengths))

# Plotting the line graphs
plt.figure(figsize=(18, 6))
plt.plot(x_ticks, braken_taxon_levels, marker='o', label='braken')
plt.plot(x_ticks, kraken2_taxon_levels, marker='*', label='Kraken2')
plt.plot(x_ticks, cent_no_rank_percentage_data, marker='o', label='Centrifuge')
plt.xticks(x_ticks, read_lengths)
plt.xticks(rotation=45)
plt.xlabel('Read Length')
plt.ylabel('Percentage')
plt.title('Taxon Classification by Read Length')
plt.grid(True)
plt.legend()
plt.savefig(outdir+'/combined_taxon_classification.png')
plt.show()
