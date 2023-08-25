def count_new_est_reads(results_file):
    new_est_reads = []

    with open(results_file, 'r') as file:
        next(file)
        for line in file:
            fields = line.strip().split('\t')
            new_est_reads.append(int(fields[5]))
    return sum(new_est_reads)



# Calculate the total number of reads
total_reads = count_new_est_reads('/mnt/data/analysis/muhammedk/MSC4/Nextflow/new_outputs/files/Braken_1000_adjusted.bracken')

print(total_reads)