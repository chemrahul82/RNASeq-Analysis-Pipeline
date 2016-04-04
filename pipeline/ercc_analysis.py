import os, sys
import subprocess
import time
from datetime import datetime
from operator import itemgetter
from scipy.stats.stats import pearsonr   
import numpy as np




def ercc_analysis(projDir,sampleName,timePoint,runId,outlog,fastq,erccpool_id):
	
# =========First map the raw fastq to ERCC reference and extract the non-ERCC reads=============
	
	ercc_reference="/results/plugins/ERCC_Analysis/ERCC92/ERCC92.fasta"
		

	#make ERCC analysis directory
	#for liver samples that have time-points
        if timePoint != 'None':
                erccDir = os.path.join(projDir,sampleName,timePoint,runId,'ERCC_analysis')
                if not os.path.exists(erccDir):
                        os.mkdir(erccDir)
                else:
                        with open(outlog, 'a') as logfile:
                                logfile.write('ERCC analysis directory already exists; not overwriting\n')
        #samples where different time points do not exist
        else:
                erccDir = os.path.join(projDir,sampleName,runId,'ERCC_analysis')
                if not os.path.exists(erccDir):
                        os.mkdir(erccDir)
                else:
                        with open(outlog, 'a') as logfile:
                                logfile.write('ERCC analysis directory already exists; not overwriting\n')
        
	#go to ERCC directory and perform analyses there
	os.chdir(erccDir)
	ERCCOUTFILE=os.path.join(erccDir,'ercc_anaysis.log')
	ERCC_SAM=os.path.join(erccDir,'ercc_mapped.sam')
	NO_ERCC_BAM=os.path.join(erccDir,'no_ercc.bam')

	ercclog=open(ERCCOUTFILE,'w')

	#map raw preprocessed fastq to ERCC reference by tmap; using parameters used in iontorrent ercc_anslysis plugin
	if not os.path.exists(ERCC_SAM):
		erccmap = 'tmap mapall -f %s -r %s -s %s -a 1 -g 0 -n 8 stage1 map1 --seed-length 18 stage2 map2 map3 --seed-length 18 > tmap.log' %(ercc_reference,fastq,ERCC_SAM)
		with open(outlog, 'a') as logfile:
			logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' =>Mapping fastq reads to ERCC reference....' +'\n')

		os.system(erccmap)
	else:
		with open(outlog, 'a') as logfile:
			 logfile.write('ERCC_mapped sam already exists; not overwriting; delete the sam file if you want to rerun tmap\n')	

	#extract the non-ERCC reads; the subsequenct bam file will be fed in the RNASEqAnalysis plugin
	if not os.path.exists(NO_ERCC_BAM):
		nonercc = 'samtools view -b -f 4 %s > %s' %(ERCC_SAM,NO_ERCC_BAM)
		with open(outlog, 'a') as logfile:
			logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' =>Extracting non-ERCC reads....' +'\n')
	
		os.system(nonercc)
	else:
		with open(outlog, 'a') as logfile:
                         logfile.write('non-ERCC bam already exists; not overwriting; delete the bam file if you want to rerun samtools\n')

# ===============Now perform the ercc transcripts count and subsequent analyses======================
	
	#ercc gemome file and concentration files
	erccgenome='/results/plugins/ERCC_Analysis/data/ercc.genome'
	ercc_conc='/results/plugins/ERCC_Analysis/data/ERCCconcentration.txt'
	
	#output file for saving ercc transcript read counts
	ercc_countfile='ercc.counts'
	fo=open(ercc_countfile,'w')
	
	#extract ercc mapped reads with mapQ scores;
	os.system('samtools view -S -F 4 %s | awk \'{print $3,"\t",$5}\' > temp' %ERCC_SAM)

	#save the log2_conc of the ERCC transcripts depending on pool id
	ercclog.write('ERCC pool id: %s\n' %erccpool_id)
	if int(erccpool_id)== 1:
		col=4
	elif int(erccpool_id)==2:
		col=5
	else:
		with open(outlog, 'a') as logfile:
			logfile.write('invalid ercc pool id; it should be either 1 or 2\n')
	
	#----------count ercc reads---------
	min_mapq = 30 #minimum mapQ score to consider
	ercclog.write('Minimum value of MAPQ score to consider count ERCC reads: %s\n' %min_mapq)

	#print total ercc reads
	total_ercc_reads = subprocess.check_output('cat temp | wc -l', shell=True) #total number of ercc-mapped reads
	ercclog.write('Total number of ERCC mapped reads: %s\n' %total_ercc_reads.strip('\n'))  	

	ncount = 0 #counter for ercc transcript with at least 1 read with mapq>30
	with open(erccgenome, 'r') as f:
		for idx,line in enumerate(f):	
			#ercc transcript name
			ercc_name=line.split('\t')[0] 
			with open(ercc_conc,'r') as fc:
				next(fc)
				ercc_log2c=[line.split('\t')[col-1] for line in fc if line.split('\t')[0]==ercc_name]

			#count number of reads with mapQ >=30 corresponding to a ercc transcript
			#ercccount='awk \'$1=="%s" { ++count } END {print count}\' %s' %(ercc_name,'temp')
			
			ercccount = 'awk \'{if ($1=="%s" && int($2)>=%s) ++count} END {print count}\' %s' %(ercc_name,int(min_mapq),'temp')
			ercc_count=subprocess.check_output(ercccount, shell=True)
		
			#write ERCC name, counts, log2c for the pool
			if len(ercc_count.strip()) != 0:
				ncount += 1
				fo.write('\t'.join([ercc_name,ercc_count.strip(),ercc_log2c[0].strip('\n')])+'\n')
			else:
				fo.write('\t'.join([ercc_name,'0',ercc_log2c[0].strip('\n')])+'\n')
	fo.close()
	os.remove('temp')
	
	ercc_read_count = subprocess.check_output('cat %s | awk \'{ sum+=$2 } END {print sum}\'' %ercc_countfile, shell=True)
	ercclog.write("The total number of ERCC mapped reads with mapQ>=30 is %s" %ercc_read_count)
	ercclog.write("Total number of ERCC transcript detected with at least 1 read at MAPQ>30 is: %s\n" %ncount)




#========================Dose-Response Curve==========================
	#minimum read to consider for a ERCC transcript
	minread=3
	ercclog.write('Minimum number of MAPQ>=30 ERCC reads considered for Dose-Response analysis: %s\n' %minread)

	ercc_countfile='ercc.counts'
	fc=open(ercc_countfile,'r')
	log2_counts=[]
	log2_c=[]

	for line in fc:
        	counts=int(line.strip('\n').split('\t')[1])
        	if counts >= int(minread):
                	log2_counts.append(np.log2(counts))
                	log2_c.append(float(line.strip('\n').split('\t')[2]))
	fc.close()

	#sort by log2C
	idx,log2_c_sorted=zip(*sorted(enumerate(log2_c), key=itemgetter(1)))
	log2_counts_sorted=[log2_counts[i] for i in idx]

	#relative log2 concentrations and read counts
	rel_log2_counts=[log2_counts_sorted[i]-log2_counts_sorted[0] for i in range(len(log2_counts_sorted))]
	rel_log2_c=[log2_c_sorted[i]-log2_c_sorted[0] for i in range(len(log2_c_sorted))]
	#for row in zip(rel_log2_counts,rel_log2_c):
	#        print '\t'.join(map(str,row))

	print pearsonr(rel_log2_counts,rel_log2_c)[0]
	ercclog.write('The R^2 value for Dose-Response curve is %s\n' %pearsonr(rel_log2_counts,rel_log2_c)[0])
	

if __name__ == "__main__":
	projDir = sys.argv[1]
        sampleName = sys.argv[2]
        timePoint = sys.argv[3]
        runId = sys.argv[4]
	outlog = sys.argv[5]
	fastq = sys.argv[6]
	erccpool_id = sys.argv[7] #1 or 2
      
	ercc_analysis(projDir,sampleName,timePoint,runId,outlog,fastq,erccpool_id)

	
