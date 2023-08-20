#!/bin/bash

# Check if the correct number of arguments is provided
if [[ $# -ne 4 ]]; then
    echo "Usage: $0 <Kraken2 report> <Centrifuge report> <Braken report> <Output>"
    exit 1
fi

# Extract file paths from arguments
CENTRIFUGE_REPORT=$1
KRAKEN2_REPORT=$2
BRAKEN_REPORT=$3
OUTPUT=$4

# Process Centrifuge report
cat $CENTRIFUGE_REPORT > $OUTPUT/centrifuge.krona
ktImportTaxonomy $OUTPUT/centrifuge.krona -o $OUTPUT/taxonomy_Centrifuge.krona.html
# To view in a browser: firefox taxonomy_Centrifuge.krona.html

# Process Kraken2 report
cat $KRAKEN2_REPORT > $OUTPUT/kraken2.krona
ktImportTaxonomy -t 5 -m 3 $OUTPUT/kraken2.krona -o $OUTPUT/taxonomy_Kraken2.krona.html
# To view in a browser: firefox taxonomy_Kraken2.krona.html

# Process Braken report
cat $BRAKEN_REPORT > $OUTPUT/braken.krona
ktImportTaxonomy -t 5 -m 3 $OUTPUT/braken.krona -o $OUTPUT/taxonomy_Braken.krona.html
# To view in a browser: firefox taxonomy_Braken.krona.html

# bash /mnt/data/analysis/muhammedk/MSC8/Nextflow/bin/krona_test.sh /mnt/data/analysis/muhammedk/MSC8/Nextflow/files/centrifuge_Combined_Cent_K1.report /mnt/data/analysis/muhammedk/MSC8/Nextflow/files/kraken_Combined.kreport.txt /mnt/data/analysis/muhammedk/MSC8/Nextflow/files/braken_Combined.braken.report