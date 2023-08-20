import matplotlib.pyplot as plt
import numpy as np
import argparse

# Function to parse Centrifuge results and count occurrences of each taxon level
def parse_results_Cent(results_file):
    taxon_levels = {'species': 0, 'genus': 0, 'family': 0, 'order': 0, 'class': 0, 'phylum':0}
    with open(results_file, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                classification = fields[2].split(';')
                taxon_level = classification[0]
                if taxon_level in taxon_levels:
                    taxon_levels[taxon_level] += 1
    return taxon_levels

# Setting up command line argument parsing
parser = argparse.ArgumentParser(description='Plot Centrifuge taxon levels from a single result file.')
parser.add_argument('cent_results_file', type=str, help='Path to the Centrifuge result file.')
parser.add_argument('output_directory', type=str, help='Path to the directory to store the pie chart.')
args = parser.parse_args()

cent_results = parse_results_Cent(args.cent_results_file)

# Remove taxon levels with a count of zero
filtered_taxon_levels = {k: v for k, v in cent_results.items() if v != 0}

labels = list(filtered_taxon_levels.keys())
sizes = list(filtered_taxon_levels.values())
colors = ['#D32F2F', '#1976D2', '#388E3C', '#FFA000', '#512DA8', '#00796B', '#5D4037', '#616161']

# Convert taxon level names to full descriptive names and abbreviations
label_mapping = {
    'species': 'Species(S)',
    'genus': 'Genus(G)',
    'family': 'Family(F)',
    'order': 'Order(O)',
    'class': 'Class(C)',
    'phylum': 'Phylum(P)'
}
label_mapping2 = {
    'species': 'S',
    'genus': 'G',
    'family': 'F',
    'order': 'O',
    'class': 'C',
    'phylum': 'P'
}
descriptive_labels = [label_mapping[label] for label in labels]
descriptive_labels2 = [label_mapping2[label] for label in labels]

# Plotting the pie chart
plt.figure(figsize=(16, 20))
wedges, texts, autotexts = plt.pie(sizes, labels=descriptive_labels2, colors=colors, autopct=lambda p: '{:.1f}%'.format(p) if p > 2 else '', startangle=140)
plt.legend(wedges, descriptive_labels, title="Taxon Levels", loc=(0.95, 0.85))
plt.setp(texts, size=12, weight="bold")
plt.axis('equal')
plt.title('Centrifuge Taxon Levels')
plt.savefig(args.output_directory + '/taxon_levels_pie_chart_cent.png', dpi=300)

# How to run the script
# python3 pie_taxon_centrifuge.py /mnt/data/analysis/muhammedk/MSC5/Nextflow/files/centrifuge_500_adjusted_Cent_K1.report /mnt/data/analysis/muhammedk/MSC5/Nextflow/testing
