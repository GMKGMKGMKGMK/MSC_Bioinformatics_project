import csv
import sys

expected = set(["pseudomonas aeruginosa"])

def parse_centrifuge_report(report_file):
    bacteria_reads = {}
    # Initialize the dictionary with the expected keys to maintain order
    bacteria_reads["unclassified"] = 0
    bacteria_reads["classified"] = 0
    for bacterium in expected:
        bacteria_reads[bacterium] = 0
    with open(report_file, 'r') as file:
        lines = file.readlines()
        second_line = lines[1]
        lines=second_line.strip().split("\t")
        bacteria_reads["unclassified"]=int(lines[4])
        total_reads = 0
    with open(report_file, 'r') as file:
        next(file)
        for line in file:
            data = line.lower().strip().split("\t")
            num_reads = int(data[4])
            total_reads += num_reads
            for i in expected:
                bacterium = i
                for p in data:
                    p = "".join(p.split()) 
                    i = "".join(i.split()) 
                    if data[2]=="strain":
                        if str(i) in str(p):
                            bacteria_reads[bacterium] = num_reads
        bacteria_reads["classified"]=total_reads

    return bacteria_reads

def parse_braken_report(report_file,kraken_file):
    # Calculate percentages for each bacterium based on the number of reads
    bacteria_percentages = {}
    total_reads = 0
    bacteria_reads = {}
    with open(kraken_file, 'r') as file:
        first_line = file.readline()
        first_line=first_line.strip().split("\t")
        bacteria_reads["unclassified"]=int(first_line[1])
        next(file)
        first_line = file.readline()
        first_line=first_line.strip().split("\t")
        bacteria_reads["classified"]=int(first_line[1])
    with open(report_file, 'r') as file:
        next(file)
        second_line = file.readline()
        total_reads+=int(second_line[1])
        for line in file:            
            data = line.lower().strip().split("\t")
            num_reads = int(data[1])
            for i in expected:
                if data[3]=="s":
                    bacterium = i
                    for p in data:
                        p = "".join(p.split()) 
                        i = "".join(i.split()) 
                        if str(i) in str(p):
                            target=i
                            bacteria_reads[bacterium] = num_reads

    return bacteria_reads

def parse_kraken2_report(report_file):
    bacteria_reads = {}
    with open(report_file, 'r') as file:
        first_line = file.readline()
        first_line=first_line.strip().split("\t")
        bacteria_reads["unclassified"]=int(first_line[1])
        next(file)
        first_line = file.readline()
        first_line=first_line.strip().split("\t")
        bacteria_reads["classified"]=int(first_line[1])

        for line in file:
            data = line.lower().strip().split("\t")
            bacterium = data[-1]
            for i in expected:
                
                if i in bacterium:
                    if data[3]=="s":
                        reads = int(data[1])
                        bacteria_reads[i] = reads
        
    return bacteria_reads

def save_to_csv(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Bacterium", "Num_Reads"])
        for bacterium, reads in data.items():
            writer.writerow([bacterium,reads])

def main(centrifuge_report, kraken2_report, braken_report, output_loc, spec):
    centrifuge_results = parse_centrifuge_report(centrifuge_report)
    kraken2_results = parse_kraken2_report(kraken2_report)
    braken_results = parse_braken_report(braken_report, kraken2_report)

    basecaller_mapping = {}
    for filename in [centrifuge_report, kraken2_report, braken_report]:
        if "r9" in filename:
            basecaller = "r9SUP" if "sup" in filename else "r9HAC"
        elif "r10" in filename:
            if "sup" in filename:
                basecaller = "r10SUP"
            elif "duplex" in filename:
                basecaller = "r10DUP"
            else:
                basecaller = "r10DOR"
        else:
            basecaller = "simulated" 

        basecaller_mapping[filename] = basecaller

    # Save results to CSV files with the "basecaller" value in the name
    save_to_csv(output_loc + "/"+ spec + "_centrifuge_results_" + basecaller_mapping[centrifuge_report] + ".csv", centrifuge_results)
    save_to_csv(output_loc + "/"+ spec + "_kraken2_results_" + basecaller_mapping[kraken2_report] + ".csv", kraken2_results)
    save_to_csv(output_loc + "/"+ spec + "_braken_results_" + basecaller_mapping[braken_report] + ".csv", braken_results)

centrifuge_report_file = sys.argv[1]
kraken2_report_file = sys.argv[2]
braken_report_file = sys.argv[3]
output_loc = sys.argv[4]
species=sys.argv[5]

main(centrifuge_report_file, kraken2_report_file, braken_report_file, output_loc, species)



