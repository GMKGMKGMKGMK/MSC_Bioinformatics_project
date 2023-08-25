nextflow.enable.dsl=2

//Create nessary folders and simulate reference fasta into fastq files using PBSIM2
process SimulateFastq {
    cpus 16

    input:
    val(refs)
    val(outdir)
    val(bin)
    val(outdir2)
    val(dir)

    output: 
    path("Combined.fastq"), emit: fq 

    script:
    """
    mkdir -p $dir/files $dir/plots $dir/fastq $dir/files_tests_RL $dir/fastq_testdata $dir/data $dir/results $dir/results $dir/results/Classified_percentage
    (cd $outdir && for file in $refs/*.fasta; do cat "\$file"; echo; done > $outdir/completed.fasta)
    (cd $outdir && wgsim -e 0 -N 100 -1 22000 -2 1 -r 0 -R 0 $outdir/completed.fasta $outdir/Combined.fastq $outdir/Comb_p2.fq )
    cat $outdir/Combined.fastq > Combined.fastq
    python3 $bin/percentage_count.py $refs $outdir2/percent_count.csv
    
    """
}

//Adjust read length to the desire range for analysis
process ReadLengthAdjust {
    cpus 16

    input:
    path("Combined.fastq")
    val(bin)
    val(outdir)
    val(min)
    val(max)
    val(steps)
    val(refs)

    output:
    path("Combined.fastq"), emit: fq1

    script:
    """

    echo "data" > Combined.txt
    python3 $bin/read_adjust.py Combined.fastq $outdir $min $max $steps

    """
}

//Zip the files to prepared for classification
process Zipped {

    input:
    val(outdir)
    val(min)
    val(max)
    val(steps)
    path("Combined.fastq")
    val(refs)

    output:
    val(outdir), emit: out

    script:
    """
    for length in {$min..$max..$steps}; 
    do
        if [ -f $outdir/\${length}_adjusted.fastq.gz ]; then
            echo "File $outdir/\${length}_adjusted.fastq.gz exists, skipping."
        else
            gzip $outdir/\${length}_adjusted.fastq
        fi
    done



    """
}  

// Classify the fastq files with each tool to generate report files
process Classifier {
    cpus 16

    input:
    val(outdir)
    val(bin)
    val(outdir2)
    val(min)
    val(max)
    val(steps)
    val(refs)

    output:
    val(outdir2), emit: out
    
    script:
    """

    if [ -f "$outdir/Combined.fastq".gz ]; then
        echo "File "$outdir/Combined.fastq" exists, skipping."
    else
        gzip "$outdir/Combined.fastq"
    fi
    bash $bin/classifer_package.sh $outdir/Combined.fastq.gz $outdir2
    for length in {$min..$max..$steps}; 
    do
    bash $bin/classifer_package.sh $outdir/\${length}_adjusted.fastq.gz $outdir2
    
    done
    """
}

//Create plots and other tables for later analsysis and figuring out the theorhtical minuimum read length(RL) thats closest to 100% classification
process Plotter{
    cpus 16
    input:
    val(bin)
    val(outdir2)
    val(outplots)
    val(min)
    val(max)
    val(steps)
    val(data)
    val(refs)

    output:
    path("closest_RL1.txt"), emit: out

    script:
    """
    
    #python3 $bin/stats_refV1.py $outdir2/centrifuge_Combined_Cent_K1.report $outdir2/kraken_Combined.kreport.txt $outdir2/braken_Combined.braken.report $data
    python3 $bin/taxon_levels_count_plot_cent.py $outdir2/ $outplots/ $min $max $steps
    python3 $bin/taxon_levels_count_plot_kraken.py $outdir2/ $outplots/ $min $max $steps
    python3 $bin/taxon_levels_count_plot_braken.py $outdir2/ $outplots/ $min $max $steps

    python3 $bin/best_read_length_plus1.py $outdir2/percent_count.csv $min $max $steps $outdir2 $outplots

    python3 $bin/closest_RL.py $outplots/best_RL.csv $outplots/closest_RL1.txt
    cat $outplots/closest_RL1.txt > closest_RL1.txt
    python3 $bin/mod_brak.py $outplots/closest_RL1.txt $outplots/closest_RL1.txt
    
    python3 $bin/pie_taxon_braken.py $outdir2/braken_Combined.braken.report $outplots
    python3 $bin/pie_taxon_centrifuge.py $outdir2/centrifuge_Combined_Cent_K1.report $outplots
    python3 $bin/pie_taxon_kraken.py $outdir2/kraken_Combined.kreport.txt $outplots
    python3 $bin/best_read_length.py $outdir2 $outdir2 $outdir2 $min $max $steps $outplots
    python3 $bin/ref_percent.py $outdir2/percent_count.csv $outplots/simulated_pie.png
    bash $bin/krona_test.sh $outdir2/centrifuge_Combined_Cent_K1.report $outdir2/kraken_Combined.kreport.txt $outdir2/braken_Combined.braken.report $outplots
    """
}

//Subsample test data at random for faster processing
process Subsample {
    cpus 16

    input:
    val(bin)
    val(outdir_testdata)
    val(r9)
    val(r10)
    path("closest_RL1.txt")
    

    output:
    path(seq), emit: out

    script:
    """
    (cd $outdir_testdata && for file in $r9/*.gz; 
    do
        zcat \$file | head -n 40000 > "r9_\$(basename "\$file" .gz)"
    done)
    
    (cd $outdir_testdata && for file in $r10/*.gz; 
    do
        gunzip \$file
    done)
    (cd $outdir_testdata && for file in $r10/*.fastq; 
    do
        python3 $bin/RL.py \$file /mnt/data/analysis/muhammedk/TMSC/r10
        
    done)
    (cd $outdir_testdata && for file in /mnt/data/analysis/muhammedk/TMSC/r10/*.fastq; 
    do
        gzip \$file
        
    done)
    (cd $outdir_testdata && for file in /mnt/data/analysis/muhammedk/TMSC/r10/*.gz; 
    do
        
        zcat \$file | head -n 40000 > "r10_\$(basename "\$file" .gz)"
    done)



    echo "sequence" > seq
    """
}

// Calculate the best RL, and apply it to the test data
process Test_Dataset_RL{

    cpus 16

    input:
    val(bin)
    val(outdir_testdata)
    val(test_files)
    val(outplots)
    val(seq)
    val(refs)
    val(outdir)
    val(species)

    output:
    path("closest_RL1.txt"), emit: out

    script:
    """

    while read -r line; do
        # Split the line into words
        words=(\$line)
        
        # Check the first word and assign the value to the appropriate variable
        case "\${words[0]}" in
            "Braken_Percentage") braken_percentage=\${words[1]};;
            "Kraken_Percentage") kraken2_percentage=\${words[1]};;
            "Centrifuge_Percentage") centrifuge_percentage=\${words[1]};;
        esac
    done < "$outplots/closest_RL2.txt"

   
    for file in $refs/*.fasta; 
    do
        base="\${file##*/}"; base="\${base%.fasta}"

        wgsim -e 0 -N 100 -1 22000 -2 1 -r 0 -R 0 "\$file" "$outdir_testdata/\${base}.fastq" "\${base}_p2.fq"
    done
    
    for file in $outdir_testdata/*.fastq;
    do

        python3 $bin/read_adjust_test_data.py \$file $test_files \$braken_percentage \$kraken2_percentage \$centrifuge_percentage
    done

    cat closest_RL1.txt > closest_RL1.txt
    """
    
}

// Classify each test data file using the metagenomic classifiers 
process Test_Dataset_classify {
    cpus 16

    input:
    val(bin)
    val(test_files)
    val(test_out)
    path("closest_RL1.txt")
    val(refs)
    val(outdir)
    val(species)
    val(outdir2)
    
    output:
    path("closest_RL1.txt"), emit: out

    script:
    """
   

    find "$test_files/" -type f -name "*.fastq" | while read -r file; do
    # Check if there's a corresponding .gz file
    if [[ ! -f "\${file}.gz" ]]; then
        gzip "\$file"
    else
        echo "exists"
        fi
    done
    
    for file in $test_files/centrifuge*.fastq.gz;
    do
    bash $bin/centrifuge_classify.sh \$file $test_out
    done
    
    for file in $test_files/kraken*.fastq.gz;
    do
    bash $bin/kraken_classify.sh \$file $test_out
    done

    for file in $test_files/braken*.fastq.gz;
    do
    bash $bin/braken_classify.sh \$file $test_out
    done

    
        
        

    
    cat closest_RL1.txt > closest_RL1.txt
    """
}

//Create final plots and tables for analysis
process Test_plots {
    cpus 16 

    input:
    val(bin)
    val(test_out)
    val(data)
    val(min)
    val(max)
    val(steps)
    val(outplots)
    path("closest_RL1.txt")
    val(results)
    val(outdir2)
    val(outdir3)



    script:
    """
    #!/bin/bash -ue
    while read -r line; do
    # Split the line into words
    words=(\$line)

    # Check the first word and assign the value to the appropriate variable
    case "\${words[0]}" in
        "Braken_Percentage") braken_percentage=\${words[1]};;
        "Kraken_Percentage") kraken2_percentage=\${words[1]};;
        "Centrifuge_Percentage") centrifuge_percentage=\${words[1]};;
    esac
    done < "$outplots/closest_RL1.txt"

    species=("Pa01" "MRSA" "Kpneumo" "Ecoli")

    centrifuge_percentage=\$centrifuge_percentage
    kraken2_percentage=\$kraken2_percentage
    braken_percentage=\$braken_percentage

    
    flowcell=("" "_r9_sup")
    for t in \$(seq 0 1)
    do
    flow=\${flowcell[\$t]}
    
    python3 $bin/stats_s_aureus.py $test_out/centrifuge_r9_MRSA\${flow}_\${centrifuge_percentage}_Cent_K1.report $test_out/kraken_r9_MRSA\${flow}_\${kraken2_percentage}.kreport.txt $test_out/braken_r9_MRSA\${flow}_\${braken_percentage}.braken.report $data "MRSA"
    python3 $bin/stats_p_aerug.py $test_out/centrifuge_r9_Pa01\${flow}_\${centrifuge_percentage}_Cent_K1.report $test_out/kraken_r9_Pa01\${flow}_\${kraken2_percentage}.kreport.txt $test_out/braken_r9_Pa01\${flow}_\${braken_percentage}.braken.report $data "Pa01"
    python3 $bin/stats_ecoli.py $test_out/centrifuge_r9_Ecoli\${flow}_\${centrifuge_percentage}_Cent_K1.report $test_out/kraken_r9_Ecoli\${flow}_\${kraken2_percentage}.kreport.txt $test_out/braken_r9_Ecoli\${flow}_\${braken_percentage}.braken.report $data "Ecoli"
    python3 $bin/stats_k_pneu.py $test_out/centrifuge_r9_Kpneumo\${flow}_\${centrifuge_percentage}_Cent_K1.report $test_out/kraken_r9_Kpneumo\${flow}_\${kraken2_percentage}.kreport.txt $test_out/braken_r9_Kpneumo\${flow}_\${braken_percentage}.braken.report $data "Kpneu"
    done
    flowcell=( "" "_duplex" "_sup")
    for t in \$(seq 0 2)
    do
    flow=\${flowcell[\$t]}
    python3 $bin/stats_s_aureus.py $test_out/centrifuge_r10_RBK114_BSAPOS_MRSA\${flow}_\${centrifuge_percentage}_Cent_K1.report $test_out/kraken_r10_RBK114_BSAPOS_MRSA\${flow}_\${kraken2_percentage}.kreport.txt $test_out/braken_r10_RBK114_BSAPOS_MRSA\${flow}_\${braken_percentage}.braken.report $data "MRSA"
    python3 $bin/stats_p_aerug.py $test_out/centrifuge_r10_RBK114_BSAPOS_Pa01\${flow}_\${centrifuge_percentage}_Cent_K1.report $test_out/kraken_r10_RBK114_BSAPOS_Pa01\${flow}_\${kraken2_percentage}.kreport.txt $test_out/braken_r10_RBK114_BSAPOS_Pa01\${flow}_\${braken_percentage}.braken.report $data "Pa01"
    python3 $bin/stats_ecoli.py $test_out/centrifuge_r10_RBK114_BSAPOS_Ecoli\${flow}_\${centrifuge_percentage}_Cent_K1.report $test_out/kraken_r10_RBK114_BSAPOS_Ecoli\${flow}_\${kraken2_percentage}.kreport.txt $test_out/braken_r10_RBK114_BSAPOS_Ecoli\${flow}_\${braken_percentage}.braken.report $data "Ecoli"
    python3 $bin/stats_k_pneu.py $test_out/centrifuge_r10_RBK114_BSAPOS_Kpneu\${flow}_\${centrifuge_percentage}_Cent_K1.report $test_out/kraken_r10_RBK114_BSAPOS_Kpneu\${flow}_\${kraken2_percentage}.kreport.txt $test_out/braken_r10_RBK114_BSAPOS_Kpneu\${flow}_\${braken_percentage}.braken.report $data "Kpneu"
    done


    python3 /$bin/stats_ecoli.py $outdir3/centrifuge_Ecoli_\${centrifuge_percentage}_Cent_K1.report $outdir3/kraken_Ecoli_\${kraken2_percentage}.kreport.txt $outdir3/braken_Ecoli_\${braken_percentage}.braken.report $data "Ecoli"
    python3 /$bin/stats_k_pneu.py $outdir3/centrifuge_Kpneu_\${centrifuge_percentage}_Cent_K1.report $outdir3/kraken_Kpneu_\${kraken2_percentage}.kreport.txt $outdir3/braken_Kpneu_\${braken_percentage}.braken.report $data "Kpneu"
    python3 /$bin/stats_s_aureus.py $outdir3/centrifuge_MRSA_\${centrifuge_percentage}_Cent_K1.report $outdir3/kraken_MRSA_\${kraken2_percentage}.kreport.txt $outdir3/braken_MRSA_\${braken_percentage}.braken.report $data "MRSA"
    python3 /$bin/stats_p_aerug.py $outdir3/centrifuge_Pa01_\${centrifuge_percentage}_Cent_K1.report $outdir3/kraken_Pa01_\${kraken2_percentage}.kreport.txt $outdir3/braken_Pa01_\${braken_percentage}.braken.report $data "Pa01"



    #Plot data 
    
    python3 $bin/test_csv.py $data $results/output.csv
    python3 $bin/test_plot_species_and_classifier.py $results/output.csv $results/Statistics
    python3 $bin/classified_percent.py $data $results/Classified_percentage
    python3 $bin/log_RL.py $outplots/classification_percentages.csv $outplots
    """


}
