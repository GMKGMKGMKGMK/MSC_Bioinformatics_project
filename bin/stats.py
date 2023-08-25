import argparse
import csv
import os

def parse_results(file,expected):
    # expected = set(["staphylococcus aureus", "klebsiella pseudomonas", "escherichia coli", "pseudomonas aeruginosa"])
    with open(file, 'r') as f:
        results = set()
        for line in f:
            line = line.lower()
            for name in expected:
                if name in line:
                    results.add(name)
    return results

def calculate_metrics(TP, FP, FN, TN):
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    F1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    F05 = 1.25 * precision * recall / (0.25 * precision + recall) if (0.25 * precision + recall) > 0 else 0
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0
    
    return precision, recall, F1, F05, specificity
    

def determine_version(filename):
    
    if "r9" or "R9" in filename:
        return "R9"
    return "R10"

def main(base_dir, output_dir):
    # Set up output CSV
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "compiled_resultsV1.csv")
    with open(output_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Tool", "Precision", "Recall", "F1 Score", "F0.5 Score", "Specificity", "Species", "Filename", "Version"])

        for filename in os.listdir(base_dir):
            full_path = os.path.join(base_dir, filename)
            
            if filename.startswith('centrifuge') and filename.endswith('Cent_K1.report'):
                tool = "Centrifuge"
               
            elif filename.startswith('kraken') and filename.endswith('kreport.txt'):
                tool = "Kraken2"
            elif filename.startswith('braken') and filename.endswith('kreport.txt'):
                tool = "Braken"
            else:
                continue 

            if "Pa01" in filename:
                expected = set(["pseudomonas aeruginosa"])
            elif "MRSA" in filename:
                expected = set(["staphylococcus aureus"])
            elif "Kpneu" in filename:
                expected = set(["klebsiella pneumoniae"])
            elif "Ecoli" in filename:
                expected = set(["escherichia coli"])   
            else:
                continue

            if "r9" in filename:
                version = "R9"
                if "sup" in filename:
                    type_of_basecall = "SUP"   
                else:
                    type_of_basecall = "HAC"                   
            elif "RBK114" in filename:
                version = "R10"     
                if "sup" in filename:
                    type_of_basecall = "SUP"   
                elif "duplex" in filename:
                    type_of_basecall = "duplex" 
                else:
                    type_of_basecall = "dorado" 
            else:
                continue  



            # print(tool,expected,version)


            result = parse_results(f"{base_dir}/{filename}",expected)
            print(f"{filename}")
            print(result)
            # if filename ()
            # expected = set(["staphylococcus aureus", "klebsiella pneumoniae", "escherichia coli", "pseudomonas aeruginosa"])
            total_species = len(expected)

            TP = len(expected & result)
            FP = len(result - expected)
            FN = len(expected - result)
            TN = total_species - TP - FP - FN

            precision, recall, F1, F05, specificity = calculate_metrics(TP, FP, FN, TN)

            species_detected = ", ".join(result) if result else "No Species Detected"
            
            csvwriter.writerow([tool, precision, recall, F1, F05, specificity, species_detected, filename, version, type_of_basecall])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate metrics for all report files in the directory.')
    parser.add_argument('base_dir', type=str, help='Directory containing the report files.')
    parser.add_argument('output', type=str, help='Path to the output directory.')
    args = parser.parse_args()

    main(args.base_dir, args.output)
