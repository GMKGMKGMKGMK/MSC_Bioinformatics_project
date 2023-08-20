import csv
import sys

# Check if the file path was provided
if len(sys.argv) < 3:
    print("Please provide the path to the CSV file and output file as command line arguments.")
    sys.exit(1)

# Path to CSV file is the first command line argument
file_path = sys.argv[1]

# Path to output file is the second command line argument
output_path = sys.argv[2]

# Read the CSV file
with open(file_path, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    data = list(reader)

# Get the header row (classifier names)
headers = data[0]

# Remove the header row from the data
data = data[1:]

# Initialize the result list
results = []

# Iterate over each classifier column
for i in range(1, len(headers)):
    # Find the combined read length for the current classifier
    combined = next((float(row[i]) for row in data if row[0] == "Combined"), None)

    if combined is None:
        results.append("No combined read length found for " + headers[i])
    else:
        # Initialize min_diff with a large number
        min_diff = float('inf')
        min_read_length = None

        # Calculate the absolute difference for each read length
        for row in data:
            if row[0] != "Combined":
                diff = abs(float(row[i]) - 100)
                if diff < min_diff:
                    min_diff = diff
                    min_read_length = row[0]

        # Append the read length with the value closest to the combined read length
        results.append(f"{headers[i]}   {min_read_length}"+"\n")

# Write the results to the output file
with open(output_path, 'w') as f:
    f.write(''.join(results))
