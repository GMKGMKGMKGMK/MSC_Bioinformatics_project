import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import numpy as np

def visualize_and_annotate_swarm_combined(df, metric, output_directory):
    order = ["r9HAC", "r9SUP", "r10SUP", "r10DOR", "r10DUP", "simulated"]
    plt.figure(figsize=(34, 30))
    
    # Define unique shapes for each classifier
    classifier_shapes = df['classifier'].unique()
    markers = ['D', '^','p']
    classifier_marker_map = {classifier: marker for classifier, marker in zip(classifier_shapes, markers)}
    
    # Define fixed colors for each species
    species_colors = {
        "Pa01": "green",
        "MRSA": "orangered",
        "Kpneu": "#FF81C0",
        "Ecoli": "purple"
    }
    
    # Plot each species and classifier combination as a single point
    ax = None
    for classifier, marker_shape in classifier_marker_map.items():
        classifier_df = df[df['classifier'] == classifier]
        ax = sns.swarmplot(x="basecaller", y=metric, hue="species", data=classifier_df, palette=species_colors, order=order, dodge=True, size=20, marker=marker_shape, ax=ax, alpha=0.8)
        # Set x-ticks and rotate them
    ax.set_xticks(np.arange(len(order)))
    plt.xticks(rotation=45)

    # Compute midpoints between x-ticks for gridlines
    midpoints = np.arange(0.5, len(order), 1)
    ax.set_xticks(midpoints, minor=True)
    ax.xaxis.grid(True, which='minor', linestyle='--', color='black', alpha=0.5)
    
    ax.set_title(f'{metric.capitalize()} Distribution by Basecaller for each Species and Classifier', fontsize=28)
    ax.set_ylabel(metric.capitalize(), fontsize=30)
    ax.set_xlabel("Basecaller", fontsize=30)
    ax.yaxis.grid(True, linestyle='--', which='major', color='black', alpha=0.35)
    # ax.xaxis.grid(True, linestyle='--', which='major', color='black', alpha=0.5)
    if metric == "sensitivity":
        ax.set_ylim(0.85, 1.01)
        ax.set_yticks(np.arange(0, 1.01, 0.05))
    else:
        ax.set_ylim(0, 1.01)
        ax.set_yticks(np.arange(0, 1.01, 0.05))
        
    ax.tick_params(axis='x', labelsize=22)
    ax.tick_params(axis='y', labelsize=22)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Create custom legend elements for classifiers
    classifier_legend_elements = [plt.Line2D([0], [0], marker=marker, color="w", markerfacecolor="gray", markersize=20, label=classifier) for classifier, marker in classifier_marker_map.items()]
    
    # Create custom legend elements for species
    species_legend_elements = [plt.Line2D([0], [0], color=color, marker='o', markersize=20, label=species, linestyle='None') for species, color in species_colors.items()]
    
    # Combine the two legends
    all_legend_elements = species_legend_elements + classifier_legend_elements
    
    ax.legend(handles=all_legend_elements, loc="upper left", bbox_to_anchor=(1, 1), fontsize=24, title="Species & Classifiers")
    
    plt.savefig(os.path.join(output_directory, f'{metric}_combined.png'), bbox_inches="tight")



def main():
    if len(sys.argv) != 3:
        print("Usage: python combined_script.py <input_csv_file> <output_directory>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_directory = sys.argv[2]

    df = pd.read_csv(input_csv)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    metrics = ['sensitivity', 'precision', 'f1_score']
    for metric in metrics:
        visualize_and_annotate_swarm_combined(df, metric, output_directory)

if __name__ == "__main__":
    main()
