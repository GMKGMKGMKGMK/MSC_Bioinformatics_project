import sys
import os
def filter_fastq_by_length(input_filename, output_filename, min_length=11000):
    count = 0
    with open(input_filename, 'r') as fin, open(output_filename, 'w') as fout:
        while True:
            header = fin.readline().strip()
            sequence = fin.readline().strip()
            plus_sign = fin.readline().strip()
            quality = fin.readline().strip()
            
            if not header:
                break
            
            if len(sequence) >= min_length:
                fout.write(header + '\n')
                fout.write(sequence + '\n')
                fout.write(plus_sign + '\n')
                fout.write(quality + '\n')
                count += 1

    return count

if __name__ == "__main__":
    # Check if the required arguments are provided
    if len(sys.argv) < 3:
        print("Usage: script_name.py path_to_input.fastq output_directory")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    base_name = os.path.basename(input_file).rsplit('.', 1)[0]
    output_file = os.path.join(output_dir, base_name + "_filtered.fastq")

    filtered_count = filter_fastq_by_length(input_file, output_file)
    print(f"Number of reads with length >= 11,000: {filtered_count}")
# awk 'NR%4==2 {sum+=length($0); count++} END {print sum/count}' /mnt/data/analysis/muhammedk/MSC_data/test/path_to_output.fastq
