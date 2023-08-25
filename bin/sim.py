def fasta_to_simulated_fastq(input_fasta, output_fastq):
    with open(input_fasta, 'r') as input_file, open(output_fastq, 'w') as output_file:
        for line in input_file:
            if line.startswith('>'):
                sequence_id = line.strip()[1:]
                sequence = next(input_file).strip()
                
                quality_scores = 'I' * len(sequence)  # Simulated perfect quality scores
                
                output_file.write(f'@{sequence_id}\n')
                output_file.write(f'{sequence}\n')
                output_file.write('+\n')
                output_file.write(f'{quality_scores}\n')

input_fasta = '/mnt/data/analysis/muhammedk/MSCP7/Nextflow/fastq/completed.fasta'
output_fastq = 'simulated_output.fastq'

fasta_to_simulated_fastq(input_fasta, output_fastq)
