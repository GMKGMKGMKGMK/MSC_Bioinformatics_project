import matplotlib.pyplot as plt
import numpy as np
import argparse

# Function to parse Kraken results and count occurrences of each taxon level
def parse_results_kra(results_file):
    taxon_levels = {'S': 0, 'S1': 0, 'G': 0, 'G1': 0, 'F': 0, 'O': 0, 'C': 0, 'P':0}
    with open(results_file, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                classification = fields[3].split(';')
                taxon_level = classification[0]
                if taxon_level in taxon_levels:
                    taxon_levels[taxon_level] += 1
    return taxon_levels

# Setting up command line argument parsing
parser = argparse.ArgumentParser(description='Plot braken taxon levels from a single result file.')
parser.add_argument('braken_results_file', type=str, help='Path to the braken result file.')
parser.add_argument('output_directory', type=str, help='Path to the directory to store the pie chart.')
args = parser.parse_args()

braken_results = parse_results_kra(args.braken_results_file)

# Remove taxon levels with a count of zero
filtered_taxon_levels = {k: v for k, v in braken_results.items() if v != 0}

labels = list(filtered_taxon_levels.keys())
sizes = list(filtered_taxon_levels.values())
colors = ['#D32F2F', '#1976D2', '#388E3C', '#FFA000', '#512DA8', '#00796B', '#5D4037', '#616161']

# Convert taxon level abbreviations to full descriptive names
label_mapping = {
    'S': 'Species(S)',
    'S1': 'Species1(S1)',
    'G': 'Genus(G)',
    'G1': 'Genus1(G1)',
    'F': 'Family(F)',
    'O': 'Order(O))',
    'C': 'Class(C)',
    'P': 'Phylum(P)'
}
descriptive_labels = [label_mapping[label] for label in labels]

# Plotting the pie chart
plt.figure(figsize=(10, 8))
wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct=lambda p: '{:.1f}%'.format(p) if p > 2 else '', startangle=140)
plt.legend(wedges, descriptive_labels, title="Taxon Levels", loc=(0.95, 0.85))
plt.setp(autotexts, size=10, weight="bold")
plt.setp(texts, size=10, weight="bold")
plt.axis('equal')
plt.title('braken Taxon Levels')
plt.savefig(args.output_directory + '/taxon_levels_pie_chart_braken.png', dpi=300)

# How to run the script
# python3 pie_taxon_braken.py /mnt/data/analysis/muhammedk/MSC5/Nextflow/files/braken_650_adjusted.braken.report /mnt/data/analysis/muhammedk/MSC5/Nextflow/testing
