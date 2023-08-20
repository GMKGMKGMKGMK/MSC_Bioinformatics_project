nextflow.enable.dsl=2

//Data input
params.fastas='/mnt/data/analysis/muhammedk/MSC_data/Ncbi_references'
params.test_data_r9='/mnt/data/analysis/muhammedk/MSC_data/r9'
params.test_data_r10='/mnt/data/analysis/muhammedk/MSC_data/r10'

//Nessary files
params.directory="$PWD"
params.unzipped="$PWD/data_unzipped"
params.test_files_RL="$PWD/files_tests_RL"
params.outputdir="$PWD/fastq"
params.bin="$PWD/bin"
params.outputdir2="$PWD/files"
params.outputdir3="$PWD/fastq_testdata"
params.outplots="$PWD/plots"
params.data="$PWD/data"
params.results="$PWD/results"

//Model location
params.model="$PWD/model/R94.model"

//Read length range
params.max_RL="20500"
params.min_RL="10500"
params.steps_RL="500"


include {
SimulateFastq; ReadLengthAdjust; Zipped; Classifier; Plotter; Test_Dataset_RL; Subsample; Test_Dataset_classify; Test_plots
} from './modules/workflow.nf'


workflow {
    Channel.fromPath( "${params.model}" )
           .set{ model_ch }.collect()

    Channel.fromPath( "${params.outputdir}" )
           .set{ outdir_ch }.collect()

    Channel.fromPath( "${params.outputdir2}" )
           .set{ outdir2_ch }.collect()



    main:
       simulate = SimulateFastq(params.fastas, model_ch,outdir_ch,params.bin,outdir2_ch,params.directory)
       adjust = ReadLengthAdjust(simulate.fq, params.bin, params.outputdir, params.min_RL, params.max_RL, params.steps_RL)
       zipping = Zipped(outdir_ch,params.min_RL,params.max_RL,params.steps_RL,adjust.fq1)
       classify = Classifier(zipping.out, params.bin, outdir2_ch,params.min_RL,params.max_RL,params.steps_RL)
       plots = Plotter(params.bin, classify.out, params.outplots, params.min_RL, params.max_RL, params.steps_RL,params.data)

       subsamples=Subsample(params.bin, params.outputdir3, params.test_data_r9, params.test_data_r10,plots.out)
       test_RL=Test_Dataset_RL(params.bin, params.outputdir3, params.test_files_RL,params.outplots,subsamples.out)
       classify_test=Test_Dataset_classify(params.bin, params.test_files_RL, params.outputdir3,test_RL.out)
       test_plots=Test_plots(params.bin,params.outputdir3, params.data, params.min_RL, params.max_RL, params.steps_RL,params.outplots,classify_test.out,params.results,classify.out)
}
