
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import os
import seaborn as sns
def visualize_and_annotate_sen(df, metric, output_directory):
    # Set color based on metric
    colors = {
        'sensitivity': 'skyblue',
        'precision': 'lightgreen',
        'f1_score': 'salmon'
    }
    chosen_color = colors[metric]

    # Set the order of the categories
    order = ["r9HAC", "r9SUP", "r10SUP", "r10DUP", "r10DOR", "simulated"]
    
    # Create a figure and axis
    plt.figure(figsize=(28, 28))
    ax = sns.boxplot(x="basecaller", y=metric, hue="species", data=df, palette="Set2", order=order, linewidth=2.5)

    # Overlay jittered strip plots with larger points
    sns.stripplot(x="basecaller", y=metric, hue="species", data=df, dodge=True, jitter=True, size=7, alpha=0.5, ax=ax, marker="D", edgecolor="black", linewidth=1, order=order) 
    
    # Adjust title, axis labels, and formatting
    ax.set_title(f'{metric.capitalize()} Distribution by Basecaller for each Species', fontsize=28)
    ax.set_ylabel(metric.capitalize(), fontsize=30)
    ax.set_xlabel("Basecaller", fontsize=30)
    ax.set_ylim(0.9, 1.001)  
    ax.set_yticks(np.arange(0.93, 1.005, 0.005))
    ax.yaxis.grid(True, linestyle='--', which='major', color='black', alpha=.25)

    ax.tick_params(axis='x', labelsize=22)
    ax.tick_params(axis='y', labelsize=22)
    plt.ylim(0.93,1.001)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(loc="upper left", bbox_to_anchor=(1,1), fontsize=24)
    plt.savefig(os.path.join(output_directory, f'{metric}_combined.png'), bbox_inches="tight")

def visualize_and_annotate(df, metric, output_directory):
    # Set color based on metric
    colors = {
        'sensitivity': 'skyblue',
        'precision': 'lightgreen',
        'f1_score': 'salmon'
    }
    chosen_color = colors[metric]

    # Set the order of the categories
    order = ["r9HAC", "r9SUP", "r10SUP", "r10DUP", "r10DOR", "simulated"]
    
    # Create a figure and axis
    plt.figure(figsize=(28, 30))
    ax = sns.boxplot(x="basecaller", y=metric, hue="species", data=df, palette="Set2", order=order, linewidth=2.5)

    # Overlay jittered strip plots with larger points
    sns.stripplot(x="basecaller", y=metric, hue="species", data=df, dodge=True, jitter=True, size=7, alpha=0.5, ax=ax, marker="D", edgecolor="black", linewidth=1, order=order) 
    
    # Adjust title, axis labels, and formatting
    ax.set_title(f'{metric.capitalize()} Distribution by Basecaller for each Species', fontsize=28)
    ax.set_ylabel(metric.capitalize(), fontsize=30)
    ax.set_xlabel("Basecaller", fontsize=30)
    ax.yaxis.grid(True, linestyle='--', which='major', color='black', alpha=.25)
    ax.set_ylim(0.4, 1.1) 
    ax.set_yticks(np.arange(0.0, 1.01, 0.05))
    ax.tick_params(axis='x', labelsize=22)
    ax.tick_params(axis='y', labelsize=22)
    plt.ylim(0,1.01)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(loc="upper left", bbox_to_anchor=(1,1), fontsize=24)
    plt.savefig(os.path.join(output_directory, f'{metric}_combined.png'), bbox_inches="tight")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python plot_script.py <input_csv_file> <output_directory>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_directory = sys.argv[2]

    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    metrics = ['sensitivity', 'precision', 'f1_score']

    for metric in metrics:
        if metric=='sensitivity':
            visualize_and_annotate_sen(df, metric, output_directory)
        else:
            visualize_and_annotate(df, metric, output_directory)
