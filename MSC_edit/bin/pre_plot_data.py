import pandas as pd
import sys

csv_file = sys.argv[1]
# Read the CSV file into a pandas DataFrame
data = pd.read_csv(csv_file)

# Convert the 'Percentage' column to numeric values
data['Percentage'] = data['Percentage'].str.rstrip('%').astype('float')

# Replace 'root' with 'unclassified' in the 'Bacterium' column
data['Bacterium'].replace('root', 'unclassified', inplace=True)

# Calculate sensitivity
sensitivity = (data[data['Bacterium'] != 'other']['Percentage'].sum()) / 100

# Calculate precision
precision = (data[data['Bacterium'] != 'unclassified']['Percentage'].sum()) / (data[data['Bacterium'] != 'unclassified']['Percentage'].sum() + data[data['Bacterium'] == 'other']['Percentage'].values[0])

# Calculate F1 score
f1_score = 2 * (precision * sensitivity) / (precision + sensitivity)

# Convert sensitivity, precision, and F1 score to percentages and round to two decimal places
sensitivity = round(sensitivity * 100, 2)
precision = round(precision * 100, 2)
f1_score = round(f1_score * 100, 2)

print(f"Sensitivity: {sensitivity}%")
print(f"Precision: {precision}%")
print(f"F1 Score: {f1_score}%")

# python3 /mnt/data/analysis/muhammedk/MSC4/Nextflow2/bin/pre_plot_data.py '/mnt/data/analysis/muhammedk/MSC4/Nextflow2/kraken2_results.csv'
