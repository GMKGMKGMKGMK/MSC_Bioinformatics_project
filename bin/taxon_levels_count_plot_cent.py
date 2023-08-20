import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import argparse

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
    completed_taxon = taxon_levels
    return completed_taxon


# Create an argument parser to handle user input
parser = argparse.ArgumentParser(description='Plot Centrifuge taxon levels count by read length.')
parser.add_argument('Cent_results_directory', type=str, help='Path to the directory containing Centrifuge result files.')
parser.add_argument('Cent_plot_output_directory', type=str, help='Path to the directory to store plot files.')
parser.add_argument('MIN', type=str, help='MIN')
parser.add_argument('MAX', type=str, help='MAX')
parser.add_argument('STEPS', type=str, help='STEPS')
args = parser.parse_args()

MIN=int(args.MIN)
MAX=int(args.MAX)
STEPS=int(args.STEPS)

# Read lengths and directories
read_lengths = [length for length in range(MIN, MAX+STEPS, STEPS)]

# Calculate taxon levels at each read length
Cent_taxon_levels = []
for length in read_lengths:
    Cent_results_file_len = args.Cent_results_directory + f"centrifuge_{length}_adjusted_Cent_K1.report"
    Cent_results = parse_results_Cent(Cent_results_file_len)
    Cent_taxon_levels.append(Cent_results)
Cent_results_file_com = args.Cent_results_directory + f"centrifuge_Combined_Cent_K1.report"
Cent_results_com = parse_results_Cent(Cent_results_file_com)
Cent_taxon_levels.append(Cent_results_com)

# Calculate percentages
taxon_labels = list(Cent_taxon_levels[0].keys()) 
num_taxon_levels = len(taxon_labels)
percentage_data = np.zeros((len(Cent_taxon_levels), num_taxon_levels))

for i, Cent_results in enumerate(Cent_taxon_levels):
    total_count = sum(Cent_results.values())
    if total_count != 0:
        for j, taxon_label in enumerate(taxon_labels):
            percentage_data[i, j] = (Cent_results[taxon_label] / total_count) * 100

# Plotting
bar_width = 0.5
colors = ['#BBDEFB', '#C8E6C9', '#FFE0B2', '#E1BEE7', '#B2EBF2', '#F8BBD0', '#FFECB3'] 
legend_patches = []

fig, ax = plt.subplots(figsize=(20, 6))

x = np.arange(len(Cent_taxon_levels))

bottom_values = np.zeros(len(Cent_taxon_levels))

for j, taxon_label in enumerate(taxon_labels):
    ax.bar(x, percentage_data[:, j], bar_width, bottom=bottom_values, color=colors[j])
    for i in range(len(Cent_taxon_levels)):
        if percentage_data[i, j] > 1: 
            percentage_label = f"{percentage_data[i, j]:.1f}%"
            ax.text(x[i], bottom_values[i] + (percentage_data[i, j] / 2), percentage_label, ha='center', va='center', fontsize=7)
    bottom_values += percentage_data[:, j]
    legend_patch = mpatches.Patch(color=colors[j], label=f"Taxon Level {taxon_label}")
    legend_patches.append(legend_patch)

ax.set_xlabel('Read Length')
ax.set_ylabel('Percentage')
ax.set_title('Centrifuge Percentage of Taxon Levels Counted by Read Length')
ax.set_xticks(x)
ax.set_xticklabels(read_lengths + ["simulated"])
ax.set_yticks(np.arange(MIN, MAX+STEPS, STEPS)) 
ax.set_ylim(0, 100)  

# Place the legend outside the graph and adjust the font size
legend_patches.reverse() 
ax.legend(handles=legend_patches, bbox_to_anchor=(1.138, 0.99), loc='right', prop={'size': 8})

# Save the plot to a larger PNG file
plt.savefig(args.Cent_plot_output_directory+'taxon_levels_count_plot_cent.png', dpi=300)
