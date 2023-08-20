import csv
import sys

# Get command-line arguments for the script
percent_csv = sys.argv[1]
MIN=int(sys.argv[2])
MAX=int(sys.argv[3])
STEPS=int(sys.argv[4])
location=sys.argv[5]
outdir=sys.argv[6]

# Initialize a list to store data for CSV output
data_to_write = []

# Add headers to the CSV data
data_to_write.append(["Read_lengths", "Braken_Percentage", "Kraken_Percentage", "Centrifuge_Percentage"])

# Function to parse a CSV file and extract species and their associated percentages
def parse_percentage_count(csv_file):
    species_percentages = {}
    
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        
        # Skip the header row
        next(csv_reader)
        
        for row in csv_reader:
            species = row[1]
            species_name=species.split(" ")
            species=",".join(species_name[0:2])
            genus_species1 = species.split(",")
            species=" ".join(genus_species1)

            percentage = float(row[3])
            species_percentages[species] = percentage
    species_percentages.pop('All')
    return species_percentages

species_percentages = parse_percentage_count(percent_csv)
print("ref")
print(species_percentages)

correct_percentages = parse_percentage_count(percent_csv)
target_species = map(str.lower, correct_percentages.keys())

# Function to extract percentages of target species from a classifier's percentages
def extract_genus_species_percentages(target_species, classifier_percentages):
    extracted_percentages = {}
    for full_species_name in target_species:
        genus_species = full_species_name
        extracted_value = classifier_percentages.get(genus_species, 0.0)
        extracted_percentages[genus_species] = extracted_value
    return extracted_percentages

# Function to extract percentages of target species specifically for Centrifuge
def extract_genus_species_percentages_cent(target_species, classifier_percentages):
    return extract_genus_species_percentages(target_species, classifier_percentages)

# Function to parse Braken results and extract species percentages
def parse_braken_results(file_path):
    percentages = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        fields = line.strip().lower().split("\t")
        if fields[3] == "s":
            species = fields[5].strip()
            percentage = float(fields[0])
            percentages[species] = percentage
    return percentages

# Function to parse Kraken2 results and extract species percentages, this is similar to Braken
def parse_kraken2_results(file_path):
    return parse_braken_results(file_path)

# Function to parse Centrifuge results, extract species percentages and convert read counts to percentages
def parse_centrifuge_results(file_path):
    percentages = {}
    total_reads = 0
    with open(file_path, 'r') as f:
        next(f)
        lines = f.readlines()
    for line in lines:
        fields = line.strip().lower().split("\t")
        species = fields[0].strip()
        species=species.split() 
        species = " ".join(species[:2]) 
        num_reads = int(fields[4])
        percentages[species] = num_reads
        num_reads = int(fields[4])
        total_reads += num_reads

    # Convert number of reads to percentages
    for species in percentages:
        percentages[species] = round((percentages[species] / total_reads) * 100,2)
    return percentages

# Parse results for different read lengths and calculate summed percentages for target species
for i in range(MIN,MAX,STEPS):
    cent=f"{location}/centrifuge_{i}_adjusted_Cent_K1.report"
    kra=f"{location}/kraken_{i}_adjusted.kreport.txt"
    brak=f"{location}/braken_{i}_adjusted.braken.report"
    RL=i
    centrifuge_percentages = parse_centrifuge_results(cent)
    kraken2_percentages = parse_kraken2_results(kra)
    braken_percentages = parse_braken_results(brak)

    target_species = map(str.lower, correct_percentages.keys())
    braken_target_percentages = extract_genus_species_percentages(target_species, braken_percentages)
    target_species = map(str.lower, correct_percentages.keys())
    kraken2_target_percentages = extract_genus_species_percentages(target_species, kraken2_percentages)
    target_species = map(str.lower, correct_percentages.keys())
    centrifuge_target_percentages = extract_genus_species_percentages_cent(target_species, centrifuge_percentages)

    sum_of_values_bra = round(sum(braken_target_percentages.values()),2)
    sum_of_values_kra = round(sum(kraken2_target_percentages.values()),2)
    sum_of_values_cent = round(sum(centrifuge_target_percentages.values()),2)
    
    data_to_write.append([i, sum_of_values_bra, sum_of_values_kra, sum_of_values_cent])

# Parse combined results and calculate summed percentages for target species
cent=f"{location}/centrifuge_Combined_Cent_K1.report"
kra=f"{location}/kraken_Combined.kreport.txt"
brak=f"{location}/braken_Combined.braken.report"
RL="Combined"
centrifuge_percentages = parse_centrifuge_results(cent)
kraken2_percentages = parse_kraken2_results(kra)
braken_percentages = parse_braken_results(brak)

target_species = map(str.lower, correct_percentages.keys()) 
braken_target_percentages = extract_genus_species_percentages(target_species, braken_percentages)
target_species = map(str.lower, correct_percentages.keys())
kraken2_target_percentages = extract_genus_species_percentages(target_species, kraken2_percentages)
target_species = map(str.lower, correct_percentages.keys())
centrifuge_target_percentages = extract_genus_species_percentages_cent(target_species, centrifuge_percentages)

sum_of_values_bra = round(sum(braken_target_percentages.values()),2)
sum_of_values_kra = round(sum(kraken2_target_percentages.values()),2)
sum_of_values_cent = round(sum(centrifuge_target_percentages.values()),2)

data_to_write.append([RL, sum_of_values_bra, sum_of_values_kra, sum_of_values_cent])

# Save the compiled data to a CSV file
csv_file_path = f"{outdir}/best_RL.csv"
with open(csv_file_path, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(data_to_write)

print("Data saved to:", csv_file_path)

# how to run the script
#python3 /bin/best_read_length_plus1.py /files/percent_count.csv "/files/centrifuge_300_adjusted_Cent_K1.report" "/files/kraken_300_adjusted.kreport.txt" "/files/braken_300_adjusted.braken.report"
