import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import argparse

def parse_results_brak(results_file):
    taxon_levels = {'S': 0, 'S1': 0, 'G': 0, 'G1': 0, 'F': 0, 'O': 0, 'C': 0}

    with open(results_file, 'r') as file:
        next(file)
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                classification = fields[3].split(';')
                print(classification)
                taxon_level = classification[0]
                if taxon_level in taxon_levels:
                    taxon_levels[taxon_level] += 1
    completed_taxon = taxon_levels
    return completed_taxon


parser = argparse.ArgumentParser(description='Plot Braken taxon levels count by read length.')
parser.add_argument('Braken_results_directory', type=str, help='Path to the directory containing Braken result files.')
parser.add_argument('brak_plot_output_directory', type=str, help='Path to the directory to store plot files.')
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
Braken_taxon_levels = []

for length in read_lengths:
    Braken_results_file = args.Braken_results_directory + f"braken_{length}_adjusted.braken.report"
    Braken_results = parse_results_brak(Braken_results_file)
    Braken_taxon_levels.append(Braken_results)
Braken_results_file = args.Braken_results_directory + f"braken_Combined.braken.report"
Braken_results = parse_results_brak(Braken_results_file)
Braken_taxon_levels.append(Braken_results)

# Calculate percentages
taxon_labels = list(Braken_taxon_levels[0].keys()) 
num_taxon_levels = len(taxon_labels)
percentage_data = np.zeros((len(Braken_taxon_levels), num_taxon_levels))

for i, Braken_results in enumerate(Braken_taxon_levels):
    total_count = sum(Braken_results.values())
    if total_count != 0:
        for j, taxon_label in enumerate(taxon_labels):
            percentage_data[i, j] = (Braken_results[taxon_label] / total_count) * 100

# Plotting
bar_width = 0.5
colors = ['#FFCDD2', '#BBDEFB', '#C8E6C9', '#FFE0B2', '#E1BEE7', '#B2EBF2', '#F8BBD0', '#FFECB3']  
legend_patches = []

fig, ax = plt.subplots(figsize=(20, 6)) 

x = np.arange(len(Braken_taxon_levels))

bottom_values = np.zeros(len(Braken_taxon_levels))

for j, taxon_label in enumerate(taxon_labels):
    ax.bar(x, percentage_data[:, j], bar_width, bottom=bottom_values, color=colors[j])
    for i in range(len(Braken_taxon_levels)):
        if percentage_data[i, j] > 1:
            percentage_label = f"{percentage_data[i, j]:.1f}%"
            ax.text(x[i], bottom_values[i] + (percentage_data[i, j] / 2), percentage_label, ha='center', va='center', fontsize=7)
    bottom_values += percentage_data[:, j]
    legend_patch = mpatches.Patch(color=colors[j], label=f"Taxon Level {taxon_label}")
    legend_patches.append(legend_patch)

ax.set_xlabel('Read Length')
ax.set_ylabel('Percentage')
ax.set_title('Braken Percentage of Taxon Levels Counted by Read Length')
ax.set_xticks(x)
ax.set_xticklabels(read_lengths + ["simulated"])
ax.set_yticks(np.arange(MIN, MAX, STEPS))  
ax.set_ylim(0, 100)  

# Place the legend outside the graph and adjust the font size
legend_patches.reverse() 
ax.legend(handles=legend_patches, bbox_to_anchor=(1.138, 0.99), loc='right', prop={'size': 8})

# Save the plot to a larger PNG file
plt.savefig(args.brak_plot_output_directory+'taxon_levels_count_plot_braken.png', dpi=300)
