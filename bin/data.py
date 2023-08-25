import pandas as pd
import os

# Function to convert FTP URL to rsync-compatible URL
def getRsyncURL(url_path, suffix):
    '''change input ncbi FTP url to rsync compatible'''
    prefix = url_path.split('/')[-1]
    newurl = url_path.replace('https', 'rsync')
    slash="/"
    url_path = '{}{}{}{}'.format(newurl,slash,prefix, suffix)
    # print(url_path)
    return url_path.replace("\n",'')

# Function to download sequences
def download_sequences(df, suffix, path):
    '''download sequences for each species'''
    for ftp_path in df['ftp_path']:
        rsync_path = getRsyncURL(ftp_path, suffix)
        os.system('rsync -avP {} {}'.format(rsync_path, path))
        # print(rsync_path)
        
# Read in the assembly summary file with pandas
df = pd.read_csv('assembly_summary.txt', sep='\t', skiprows=1)

# Filter for complete genomes and reference/representative genomes
df = df.loc[(df['assembly_level'] == 'Complete Genome') &
            (df['refseq_category'].isin(['reference genome', 'representative genome']))]

# Group the data by species_taxid and get the first ftp_path for each species
df = df.groupby('species_taxid').first()[['ftp_path']]

# Download the genomic DNA sequences
download_sequences(df, '_genomic.fna.gz', '/home/muhammedk/masters/database/genomes')

# Download the protein amino acid sequences
download_sequences(df, '_protein.faa.gz', '/home/muhammedk/masters/database/amino_acids')

# Save the filtered assembly summary file with the genomes you downloaded
df.to_csv('filtered_assembly_summary2.txt', sep='\t', index=True)
