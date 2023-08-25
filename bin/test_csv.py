import os
import sys
import pandas as pd

def process_csv_files(directory):
    results = []

    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    for file in files:
        # Extract basecaller and classifier
        basecaller = file.split('_')[-1].replace('.csv', '')
        classifier = file.split('/')[-1].split('_')[1] 
        
        df = pd.read_csv(os.path.join(directory, file))
        
        unclassified_reads = df[df['Bacterium'] == 'unclassified']['Num_Reads'].values[0]
        classified_reads = df[df['Bacterium'] == 'classified']['Num_Reads'].values[0]
        
        # Extracting species from the third row
        species = file.split('_')[-4].replace('.csv', '')
        correct_reads = df[(df['Bacterium'] != 'classified') & (df['Bacterium'] != 'unclassified')]['Num_Reads'].values[0]
        print(file)
        sensitivity = round(correct_reads / (classified_reads + unclassified_reads), 2)
        precision = round(correct_reads / classified_reads, 2)
        
        # Compute F1 score
        if (precision + sensitivity) != 0:
            f1_score = round(2 * (precision * sensitivity) / (precision + sensitivity), 2)
        else:
            f1_score = 0
        
        results.append({
            'basecaller': basecaller,
            'classifier': classifier,
            'species': species,
            'sensitivity': sensitivity,
            'precision': precision,
            'f1_score': f1_score
        })
        
    return results

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_directory> <output_csv_file>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_file = sys.argv[2]
    
    results = process_csv_files(input_directory)
    
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

    print(f"Results saved to {output_file}")


# python3 /mnt/data/analysis/muhammedk/MSC7/Nextflow/bin/test_csv.py /mnt/data/analysis/muhammedk/MSC7/Nextflow/plots_and_data savv.csv