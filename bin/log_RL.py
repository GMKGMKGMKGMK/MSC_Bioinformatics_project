import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(data, ylabel, output_folder):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Plotting data
    ax.semilogx(data['read length'], data['percentage classified (Kraken2)'], 'g^', label='Kraken2',markersize =12)
    ax.semilogx(data['read length'], data['percentage classified (braken)'], 'o', color='orange', label='braken')
    ax.semilogx(data['read length'], data['percentage classified (Centrifuge)'], 'd', color='blue', label='Centrifuge')

    # Setting labels, title, and legend
    ax.set_title(ylabel + ' vs. Read Length')
    ax.set_xlabel('Read Length')
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both", ls="--", c='0.7')
    ax.legend(loc='upper left', bbox_to_anchor=(1,1))


    # Set specific x-ticks to ensure 10^2 is displayed
    xticks = [0.5, 1.0, 10.0, 15, 20, 25, 30, 35, 40]
    yticks = list(range(80, 101))
    ax.set_ylim(80, 101)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    plt.tight_layout()
    filename = ylabel.replace(" ", "_").lower() + '_plot.png'
    plt.savefig(os.path.join(output_folder, filename))
    plt.close()

def plot_data_unclass(data, ylabel, output_folder):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Plotting data
    ax.semilogx(data['read length'], data['percentage unclassified (Kraken2)'], 'g^', label='Kraken2',markersize =12)
    ax.semilogx(data['read length'], data['percentage unclassified (braken)'], 'o', color='orange', label='braken')
    ax.semilogx(data['read length'], data['percentage unclassified (Centrifuge)'], 'd', color='blue', label='Centrifuge')

    # Setting labels, title, and legend
    ax.set_title(ylabel + ' vs. Read Length')
    ax.set_xlabel('Read Length')
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both", ls="--", c='0.7')
    ax.legend(loc='upper left', bbox_to_anchor=(1,1))


    # Set specific x-ticks to ensure 10^2 is displayed
    xticks = [0.5, 1.0, 10.0, 15, 20, 25, 30, 35, 40]
    yticks = list(range(0, 20))
    ax.set_ylim(-1, 20)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    plt.tight_layout()
    filename = ylabel.replace(" ", "_").lower() + '_plot.png'
    plt.savefig(os.path.join(output_folder, filename))
    plt.close()


if __name__ == "__main__":
    # Check if CSV path and output folder are provided
    if len(sys.argv) < 3:
        print("Usage: python script_name.py path_to_csv output_folder")
        sys.exit(1)

    # Load the CSV data
    data_path = sys.argv[1]
    output_folder = sys.argv[2]
    data = pd.read_csv(data_path)

    # Plot the data
    plot_data_unclass(data, 'Percentage Unclassified', output_folder)
    plot_data(data, 'Percentage Classified', output_folder)
