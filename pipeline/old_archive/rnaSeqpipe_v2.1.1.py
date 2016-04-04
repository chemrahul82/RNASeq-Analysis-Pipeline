#this script copies the bam and index files for the liver RNA-seq from the archived reports of Pluto or Mercury
#Author: Rahul K. Das
#Date: 12/04/2015
# last updated 04/01/2016: empty_dummy bam check

import os, sys, glob
from datetime import datetime


#function that copies the bam and index files from the remote directory
def copybam(projDir,sampleName,timePoint,runId,remoteDir,remoteId,outlog,passwd):
	
	
	#create sample, timepoint, and run directories if they don't already exist
	sampleDir = os.path.join(projDir,sampleName)
	if not os.path.exists(sampleDir):
		os.mkdir(sampleDir)
	else:
		with open(outlog, 'a') as logfile:
			logfile.write('sample directory already exists; not overwriting\n')
	
	#for liver samples that have time-points
	if timePoint != 'None':
		timeDir = os.path.join(sampleDir, timePoint)
		if not os.path.exists(timeDir):
			os.mkdir(timeDir)
		else:
			with open(outlog, 'a') as logfile:
				logfile.write('time point directory already exists; not overwriting\n')
	#samples where different time points do not exist
	else:
		timeDir = sampleDir
	
	#run directory	
	runDir = os.path.join(timeDir, runId)
	if not os.path.exists(runDir):
		os.mkdir(runDir)
	else:
		with open(outlog, 'a') as logfile:
			logfile.write('run directory already exists; not overwriting\n')
	
	#copy bam and index files if they don't already exist
	os.chdir(runDir)
	BAMPREFX='RNA_Barcode_None_001_rawlib' #prefix of bam if no barcode

	#if empty_dummy bam present from previous transfer of a run where coverageanalysis failed and couldn't generate the mapped bam, delete everything
	if "empty_dummy.bam" in glob.glob("*.bam"):
		os.system('rm -r *')
	
	 
	if len(glob.glob("*.bam")) == 0:
		with open(outlog, 'a') as logfile:
			logfile.write('copying bam file\n')

		#the sequencing data can be either in Pluto or in Mercury
		if remoteId == 'PLU':
			#first look for the mapped bam file
			command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/results/analysis/output/Home/%s/%s.bam  %s' %(passwd,remoteDir,BAMPREFX,runDir)
			exitco = os.system(command)
			if exitco == 0:
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/results/analysis/output/Home/%s/%s.bam.bai  %s' %(passwd,remoteDir,BAMPREFX,runDir)
				os.system(command)
				with open(outlog, 'a') as logfile:
					logfile.write('successfully copied mapped bam and index files from remote directory %s\n' %remoteDir)
			else:
				#if mapped bam was not found, look for the unmapped bam file in the basecaller_results directory
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/results/analysis/output/Home/%s/basecaller_results/%s.basecaller.bam  %s' %(passwd,remoteDir,BAMPREFX,runDir)
				exitco = os.system(command)
				if exitco == 0:
					command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/results/analysis/output/Home/%s/basecaller_results/%s.basecaller.bam.bai  %s' %(passwd,remoteDir,BAMPREFX,runDir)
					os.system(command)
					with open(outlog, 'a') as logfile:
						logfile.write('successfully copied unmapped bam and index files from remote directory %s\n'%remoteDir)
				else:
					#the data probably have been archived; look in the archived reports
					command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/mnt/Charon/archivedReports/%s/%s.bam  %s' %(passwd,remoteDir,BAMPREFX,runDir)
					os.system(command)
					if exitco == 0:
						command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/mnt/Charon/archivedReports/%s/%s.bam.bai  %s' %(passwd,remoteDir,BAMPREFX,runDir)
						os.system(command)
						with open(outlog, 'a') as logfile:
							logfile.write('successfully copied mapped bam and index files from remote archivereport directory %s\n'%remoteDir)
					else:
						command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/mnt/Charon/archivedReports/%s/basecaller_results/%s.basecaller.bam  %s' %(passwd,remoteDir,BAMPREFX,runDir)
						os.system(command)
						if exitco == 0:
							command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/mnt/Charon/archivedReports/%s/basecaller_results/%s.basecaller.bam.bai  %s' %(passwd,remoteDir,BAMPREFX,runDir)
							os.system(command)
							with open(outlog, 'a') as logfile:
								logfile.write('successfully copied unmapped bam and index files from remote archivereport directory %s\n')	
						else:	
							with open(outlog, 'a') as logfile:
								logfile.write('Could not locate bam file in the remote server; exiting')
								os.system('exit 1')
		
		if remoteId == 'MER':
			#first look for the mapped bam file
			command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/results/analysis/output/Home/%s/%s.bam  %s' %(passwd,remoteDir,BAMPREFX,runDir)
			exitco = os.system(command)
			if exitco == 0:
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/results/analysis/output/Home/%s/%s.bam.bai  %s' %(passwd,remoteDir,BAMPREFX,runDir)
				os.system(command)
				with open(outlog, 'a') as logfile:
					logfile.write('successfully copied mapped bam and index files from remote directory %s\n' %remoteDir)
			else:
				#if mapped bam was not found, look for the unmapped bam file in the basecaller_results directory
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/results/analysis/output/Home/%s/basecaller_results/%s.basecaller.bam  %s' %(passwd,remoteDir,BAMPREFX,runDir)
				exitco = os.system(command)
				if exitco == 0:
					command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/results/analysis/output/Home/%s/basecaller_results/%s.basecaller.bam.bai  %s' %(passwd,remoteDir,BAMPREFX,runDir)
					os.system(command)
					with open(outlog, 'a') as logfile:
						logfile.write('successfully copied unmapped bam and index files from remote directory %s\n'%remoteDir)
				else:
					#the data probably have been archived; look in the archived reports
					command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/mnt/Charon/archivedReports/%s/%s.bam  %s' %(passwd,remoteDir,BAMPREFX,runDir)
					os.system(command)
					if exitco == 0:
						command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/mnt/Charon/archivedReports/%s/%s.bam.bai  %s' %(passwd,remoteDir,BAMPREFX,runDir)
						os.system(command)
						with open(outlog, 'a') as logfile:
							logfile.write('successfully copied mapped bam and index files from remote archivereport directory %s\n'%remoteDir)
					else:
						command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/mnt/Triton/archivedReports/%s/basecaller_results/%s.basecaller.bam  %s' %(passwd,remoteDir,BAMPREFX,runDir)
						os.system(command)
						if exitco == 0:
							command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/mnt/Triton/archivedReports/%s/basecaller_results/%s.basecaller.bam.bai  %s' %(passwd,remoteDir,BAMPREFX,runDir)
							os.system(command)
							with open(outlog, 'a') as logfile:
								logfile.write('successfully copied unmapped bam and index files from remote archivereport directory %s\n')	
						else:	
							with open(outlog, 'a') as logfile:
								logfile.write('Could not locate bam file in the remote server; exiting')
								os.system('exit 1')

	
def run_rnaseqPlugin(projDir,sampleName,timePoint,runId,outlog):
	with open(outlog, 'a') as logfile:
		logfile.write('Started RNASeqPlugin at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
	pluginDir = '/results/plugins/RNASeqAnalysis'
	refFasta = '/results/referenceLibrary/tmap-f3/hg19/hg19.fasta'
	#set output file basename to bamfile name
	basename = os.path.splitext(glob.glob("*.bam")[0])[0]
	adapter = 'None'
	fracreads = 1
	fpkm_thres = 0.3
	
	#set the output_directory
	if timePoint != 'None':
		output_dir = os.path.join(projDir,sampleName,timePoint,runId)
	else:
		output_dir = os.path.join(projDir,sampleName,runId)

	#run iontorrent RNASEQAnalysis plugin
	command = 'python %s/run_rnaseqanalysis.py hg19 %s *.bam %s %s %s %s %s %s pluginlog' %(pluginDir,refFasta,basename,adapter,fracreads,fpkm_thres,output_dir,basename)
	with open(outlog, 'a') as logfile:
		logfile.write('Started iontorrent RNASEQAnalysis plugin with command %s at ' %command + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
	os.system(command)

#function for merging bam files and running iontorrent RNAseqanalysis on the merged file
def merge_bam(projDir,sampleName,timePoint,runId):
	#make merged direcory
	if timePoint != 'None':
		mergedDir = os.path.join(projDir,sampleName,timePoint,runId)
		if not os.path.exists(mergedDir):
			os.mkdir(mergedDir)
		else:
			with open(outlog, 'a') as logfile:
				logfile.write('Merged directory already exists; not overwriting\n')
	else:
		mergedDir = os.path.join(projDir,sampleName,runId)	
		if not os.path.exists(mergedDir):
			os.mkdir(mergedDir)
		else:
			with open(outlog, 'a') as logfile:
				logfile.write('Merged directory already exists; not overwriting\n')
	
	#go to merged directory
	os.chdir(mergedDir)	
	#merge bam files
	sampleDir = os.path.join(projDir,sampleName)
	runDirs = sorted([d for d in os.listdir(sampleDir) if (os.path.isdir(os.path.join(sampleDir, d)) and "Run" in d)])
	
        #bams to be merged
	bamList = []
	for rdir in runDirs:
		bam=os.path.join(sampleDir,rdir,'RNA_Barcode_None_001_rawlib.bam')
		bamList.append(bam)
	
	with open(outlog, 'a') as logfile:
		 logfile.write('merging bams from %s started at ' %','.join(runDirs) + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')

	#run samtools merge
	os.system('samtools merge %s %s' %('merged_badHeader.bam',' '.join(bamList)))
	#fix header for merged bam
	os.system('samtools view -H %s > %s' %('merged_badHeader.bam','merged_header.sam'))	
	#check if the SM tags exist
	os.system('sed "s/SM:[a-zA-Z0-9_&/-]*/SM:%s/" %s > %s' %(sampleName, 'merged_header.sam', 'merged_header_corrected.sam'))
	#write the new header to the merged bam
	os.system('samtools reheader %s %s > %s' %('merged_header_corrected.sam','merged_badHeader.bam','merged_all.bam'))
	#clean up temp files
	os.system('rm %s %s %s' %('merged_badHeader.bam','merged_header.sam','merged_header_corrected.sam'))	
	
	with open(outlog, 'a') as logfile:
		logfile.write('merging bams from %s finished at ' %','.join(runDirs) + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
	


if __name__ == "__main__":
	projDir = sys.argv[1]
	sampleName = sys.argv[2]
	timePoint = sys.argv[3]
	runId = sys.argv[4]
	remoteDir = sys.argv[5]
	remoteId = sys.argv[6]
	#backedUp = sys.argv[7]
	merged_single = sys.argv[7]
	passwd = sys.argv[8]	
	
	#<usage> 
	#single run: nohup python -u rnaSeqpipe.py <projDir_path> <sample_name> <timepoint/None> <RUN_ID> <name_Dir_proton_server> <Proton_name (MER/PLU)> <single> <passwd> > /dev/null 2>&1&
	#merged run: nohup python -u rnaSeqpipe.py <projDir_path> <sample_name> <timepoint/None> <Merged> <NA> <NA> <merged> <NA> > /dev/null 2>&1&
	
	#create a separate runlog file that will be stored in a temp directory and moved to the run directory after the run is complete
	if timePoint != 'None':
		outlog = os.path.join(projDir,'temp','runlog'+sampleName+'-'+timePoint+'-'+runId+'-'+datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
	else:
		outlog = os.path.join(projDir,'temp','runlog'+sampleName+'-'+runId+'-'+datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
	with open(outlog, 'a') as logfile:
		logfile.write('Execution started at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
		#if backedUp == 'Yes':
		#	logfile.write('This run was archived\n')
		#elif backedUp == 'No':
		#	logfile.write('This run was not yet archived\n')
	
	#run analysis for a single run
	if merged_single == 'single':
		with open(outlog, 'a') as logfile:
			logfile.write('This is a single-run analysis of %s of sample %s\n' %(runId,sampleName))
		#copy the bam & index files
		copybam(projDir,sampleName,timePoint,runId,remoteDir,remoteId,outlog,passwd)
	
		# run the RNASeqPlugin inside the run directory
		os.chdir(os.path.join(projDir,sampleName,runId))
		run_rnaseqPlugin(projDir,sampleName,timePoint,runId,outlog)
		
		with open(outlog, 'a') as logfile:
			logfile.write('Execution ended at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
		
	#run analysis for merged runs
	elif merged_single == 'merged':
		with open(outlog, 'a') as logfile:
			logfile.write('This is a merged-run analysis of sample %s\n' %sampleName)

		#merge bams
		merge_bam(projDir,sampleName,timePoint,runId)
				
		#run the RNASeqPlugin inside the merged directory
                os.chdir(os.path.join(projDir,sampleName,runId))
		run_rnaseqPlugin(projDir,sampleName,timePoint,runId,outlog)
		
		with open(outlog, 'a') as logfile:
			logfile.write('Execution ended at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
		
	#move the runlog file to the run directory
	if timePoint != 'None':
		os.rename(outlog, os.path.join(projDir,sampleName,timePoint,runId,outlog))
	else:
		os.rename(outlog, os.path.join(projDir,sampleName,runId,outlog))

		
