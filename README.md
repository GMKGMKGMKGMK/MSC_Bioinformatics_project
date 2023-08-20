# MSC Bioinformatics project
This workflow contains the files necessary to run the analysis, besides the databases, test data, and Fasta files. 
In order to run this workflow one must:
1. Set inputs to the directories of necessary files in the main.nf file. 
2. Add databases to the metagenomic classifier bash files in the bin folder{metagenomic classifier}_classify.sh).
3. Ensure that at least 100GB of storage is available before running and set cpus to your values in the workflow.nf.
4. Set the max, min, and step values for the read lengths you wish to analyze.
5. Create a conda environment using the MSC_ENV.yml file in the conda_env folder
``` bash
conda env create -f ./conda_env/MSC_ENV.yml
```
6. Run the workflow by running:
``` bash
bash run_nexflow.sh 
```
or 
``` bash
nextflow run ./main.nf
```
The outputs will be in the plots and results folders
