import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def annotate_bars(ax, data):
    """Annotate the bars with their values."""
    for i, v in enumerate(data.values):
        ax.text(i, v + 0.02, '{:1.2f}'.format(v), ha='center', va='bottom')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python plot_script.py <input_csv_file> <output_sensitivity_plot> <output_precision_plot> <output_f1_plot>")
        sys.exit(1)

    input_csv = sys.argv[1]
    sensitivity_output = sys.argv[2]
    precision_output = sys.argv[3]
    f1_output = sys.argv[4]
    
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Group by basecaller and calculate the mean for sensitivity, precision, and F1
    grouped = df.groupby('basecaller').mean()

    # Calculate F1 score
    grouped['f1'] = 2 * (grouped['precision'] * grouped['sensitivity']) / (grouped['precision'] + grouped['sensitivity'])

    # Plotting average sensitivity for each basecaller
    plt.figure(figsize=(10, 6))
    ax_sensitivity = grouped['sensitivity'].plot(kind='bar', color='skyblue')
    annotate_bars(ax_sensitivity, grouped['sensitivity'])
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.title('Average Sensitivity by Basecaller')
    plt.ylabel('Sensitivity')
    plt.xlabel('Basecaller')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(sensitivity_output)  

    # Plotting average precision for each basecaller
    plt.figure(figsize=(10, 6))
    ax_precision = grouped['precision'].plot(kind='bar', color='salmon')
    annotate_bars(ax_precision, grouped['precision'])
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.title('Average Precision by Basecaller')
    plt.ylabel('Precision')
    plt.xlabel('Basecaller')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(precision_output)  

    # Plotting average F1 score for each basecaller
    plt.figure(figsize=(10, 6))
    ax_f1 = grouped['f1'].plot(kind='bar', color='green')
    annotate_bars(ax_f1, grouped['f1'])
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.title('Average F1 Score by Basecaller')
    plt.ylabel('F1 Score')
    plt.xlabel('Basecaller')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f1_output)
