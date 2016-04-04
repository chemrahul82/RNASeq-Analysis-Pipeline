#!/bin/bash

#####################################################################################

#Script for performing cuffmerge and cuffdif analyses on the STAR+BOWTIE2.bam files
# and assembles transcripts by cufflinks
#Rahul K. Das
#03/31/2016

#<usage>: ./run_cuffdiff_merge.sh <sample_1> <sample_2>

######################################################################################

if [ "$#" -ne 4 ]; then 
        echo "Oops! Wrong command"
        echo "<usage>: $0 <sample_1> <sample_2>"
        exit 1
fi


while getopts a:b: opt; do
        case $opt in
                a)
                        sample1=$OPTARG
                        ;;
                b)
                        sample2=$OPTARG
                        ;;

                \?)
                        echo "Unrecognized options or improper usage"
                        echo "<usage>: $0 -a <sampleid_1> -b <sampleid_2>"
                        ;;
                :)
                        echo "Missing option argument for -$OPTARG"; exit 1
                        ;;
        esac
done
shift $((OPTIND-1))

#sample1="$1"
#sample2="$2"

nt=16 #no. of threads to use
CUFFLINKDIR="/results/plugins/RNASeqAnalysis/bin/cufflinks-2.2.1"
CUFFMERGE="$CUFFLINKDIR/cuffmerge"
CUFFDIFF="$CUFFLINKDIR/cuffdiff"
REFGENEGTF="/results/plugins/RNASeqAnalysis/annotations/hg19/gene.gtf"
REFFASTA="/results/referenceLibrary/tmap-f3/hg19/hg19.fasta"
MERGEDGTF="merged_asm/merged.gtf" 
PREFX="RNA_Barcode_None_001_rawlib" #file prefix
BAMFILE="$PREFX.bam"
projdir="/rawdata/projects/RNA-seq/LS"
anadir="$projdir/DiffExpress/cuffmerge_diff"
rundir="$anadir/$sample1_$sample2"
ASSEMBLIES="$rundir/assemblies.txt"
currdir=`pwd`


if [ ! -d "$rundir" ]; then
	mkdir -p "rundir"
else
	echo "Run directory for the sample-pair $sample1 and $sample2 exists; not overwriting"
fi

#go to the run directory and perform cuffmerge and cuffdiff analysis there
cd $rundir

#make the assemblies.txt file for cuffmerge run
cat <<EOF > $ASSEMBLIES
$projdir/$sample1/Run1/$PREFX.transcripts.gtf
$projdir/$sample1/Run2/$PREFX.transcripts.gtf
$projdir/$sample2/Run1/$PREFX.transcripts.gtf
$projdir/$sample2/Run2/$PREFX.transcripts.gtf
EOF	

#run cuffmerge to make merged.gtf
if [ -f "$rundir/$MERGEDGTF" ]; then
	echo "merged.gtf exists; cuffmerge may have been already run for this pair; not rerunning cuffmerge"
else
	echo "$(date):: Starting cuffmerge run on $sample1 and $sample2...."
	$CUFFMERGE -g $REFGENEGTF -s $REFFASTA -p $nt $ASSEMBLIES > cuffmerge.log 2>&1&
	if [ $? -eq 0 ]; then
    		echo "$(date):: Successfully finished cuffmerge run on $sample1 and $sample2...." 
	else
    		echo "$(date):: cuffmerge run failed for $sample1 and $sample2...." 
	fi
fi

#run cuffdiff
echo "$(date):: Starting cuffdiff run on $sample1 and $sample2...."

nohup $CUFFDIFF -o $rundir -b $REFFASTA -p $nt -L $sample1,$sample2 -u $rundir/$MERGEDGTF -m 100 -s 60\
 --library-type fr-secondstrand\
 "$projdir/$sample1/Run1/$BAMFILE","$projdir/$sample1/Run2/$BAMFILE"\
 "$projdir/$sample2/Run1/$BAMFILE","$projdir/$sample2/Run2/$BAMFILE" > cuffdiff.log 2>&1&

if [ $? -eq 0 ]; then
    echo "$(date):: Successfully finished cuffdiff run on $sample1 and $sample2...." 
else
    echo "$(date):: cuffdiff run failed for $sample1 and $sample2...." 
fi

cd $currdir
