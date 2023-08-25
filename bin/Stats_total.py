import argparse
import csv
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate metrics for all report files in the directory.')
    parser.add_argument('base_dir', type=str, help='Directory containing the report files.')
    parser.add_argument('csv_file', type=str, help='Path to the csv file directory.')
    parser.add_argument('output', type=str, help='Path to the output directory.')
    args = parser.parse_args()

    main(args.base_dir, args.output)

# import argparse

# def calculate_metrics(TP, FP, FN):
#     precision = TP / (TP + FP) if TP + FP > 0 else 0
#     recall = TP / (TP + FN) if TP + FN > 0 else 0
#     F1 = (2 * precision * recall) / (precision + recall) if precision + recall > 0 else 0
#     F05 = ((1 + 0.5**2) * precision * recall) / ((0.5**2 * precision) + recall) if precision + recall > 0 else 0
#     return precision, recall, F1, F05

# def parse_results(file):
#     expected = set(["staphylococcus aureus", "klebsiella pseudomonas", "escherichia coli", "pseudomonas aeruginosa"])
#     with open(file, 'r') as f:
#         results = set()
#         for line in f:
#             line = line.lower()
#             for name in expected:
#                 if name in line:
#                     results.add(name)
#     return results

# def main(centrifuge_report, kraken2_report, braken_report):
#     # Parse the results from Centrifuge, Kraken2, and Braken
#     results = {
#         "Centrifuge": parse_results(centrifuge_report),
#         "Kraken2": parse_results(kraken2_report),
#         "Braken": parse_results(braken_report)
#     }

#     # Define the expected taxa (expected results)
#     expected = set(["staphylococcus aureus", "klebsiella pseudomonas", "escherichia coli", "pseudomonas aeruginosa"])

#     # Calculate the metrics for each tool
#     for tool, result in results.items():
#         TP = len(expected & result)  # True positives: taxa present in both the expected and the result
#         FP = len(result - expected)  # False positives: taxa present in the result but not in the expected
#         FN = len(expected - result)  # False negatives: taxa present in the expected but not in the result

#         precision, recall, F1, F05 = calculate_metrics(TP, FP, FN)
#         print(f"{tool}:\nPrecision: {precision}\nRecall: {recall}\nF1 Score: {F1}\nF0.5 Score: {F05}\n")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Calculate Precision, Recall, and F-scores.')
#     parser.add_argument('centrifuge_report', type=str, help='Path to the Centrifuge report file.')
#     parser.add_argument('kraken2_report', type=str, help='Path to the Kraken2 report file.')
#     parser.add_argument('braken_report', type=str, help='Path to the Braken report file.')
#     args = parser.parse_args()

#     main(args.centrifuge_report, args.kraken2_report, args.braken_report)
