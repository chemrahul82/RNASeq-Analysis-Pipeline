#this script copies the bam and index files for the liver RNA-seq from the archived reports of Pluto or Mercury
#Author: Rahul K. Das
#Date: 12/04/2015

import os, sys, glob
from datetime import datetime


#function that copies the bam and index files from the remote directory
def copybam(projDir,sampleName,timePoint,runId,remoteDir,remoteId,backedUp,outlog):
	
	
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
	#samples ehere different time points do not exist
	else:
		timeDir = sampleDir
	
	runDir = os.path.join(timeDir, runId)
	if not os.path.exists(runDir):
		os.mkdir(runDir)
	else:
		with open(outlog, 'a') as logfile:
			logfile.write('run directory already exists; not overwriting\n')
	
	#copy bam and index files if they don't already exist
	os.chdir(runDir)
	if len(glob.glob("*.bam")) == 0:
		with open(outlog, 'a') as logfile:
			logfile.write('copying bam file\n')
		#the sequencing data can be either in Pluto or in Mercury
		if remoteId == 'PLU':
			if backedUp == 'Yes':
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/mnt/Charon/archivedReports/%s/*.bam  %s' %('ionadmin',remoteDir,runDir)
				os.system(command)
			elif backedUp == 'No':
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/results/analysis/output/Home/%s/*.bam  %s' %('ionadmin',remoteDir,runDir)
				os.system(command)
		elif remoteId == 'MER':
			if backedUp == 'Yes':
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/mnt/Triton/archivedReports/%s/*.bam  %s' %('ionadmin',remoteDir,runDir)
				os.system(command)
			elif backedUp == 'No':	
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/results/analysis/output/Home/%s/*.bam  %s' %('ionadmin',remoteDir,runDir)
				os.system(command)
	else:
		with open(outlog, 'a') as logfile:
			logfile.write('bam file already exists, not copying\n')

	if len(glob.glob("*.bam.bai")) == 0:
		with open(outlog, 'a') as logfile:
			logfile.write('copying bam index file\n')
		if remoteId == 'PLU':
			if backedUp == 'Yes':
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/mnt/Charon/archivedReports/%s/*.bam.bai  %s' %('ionadmin',remoteDir,runDir)
				os.system(command)
			elif backedUp == 'No':
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.42:/results/analysis/output/Home/%s/*.bam.bai  %s' %('ionadmin',remoteDir,runDir)
				os.system(command)
		elif remoteId == 'MER':
			if backedUp == 'Yes':
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/mnt/Triton/archivedReports/%s/*.bam.bai  %s' %('ionadmin',remoteDir,runDir)
				os.system(command)
			elif backedUp == 'No':
				command = 'sshpass -p %s scp -r ionadmin@192.168.200.41:/results/analysis/output/Home/%s/*.bam.bai  %s' %('ionadmin',remoteDir,runDir)
				os.system(command)
	else:
		with open(outlog, 'a') as logfile:
			logfile.write('bam index file already exists, not copying\n')
	with open(outlog, 'a') as logfile:
		logfile.write('finished copying bam & index files from remote directory %s\n' %remoteDir)
	
	
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
	if timePoint != 'None':
		output_dir = os.path.join(projDir,sampleName,timePoint,runId)
	else:
		output_dir = os.path.join(projDir,sampleName,runId)
	command = 'python %s/run_rnaseqanalysis.py hg19 %s *.bam %s %s %s %s %s %s pluginlog' %(pluginDir,refFasta,basename,adapter,fracreads,fpkm_thres,output_dir,basename)
	with open(outlog, 'a') as logfile:
		logfile.write('running %s\n' %command)
	os.system(command)


if __name__ == "__main__":
	projDir = sys.argv[1]
	sampleName = sys.argv[2]
	timePoint = sys.argv[3]
	runId = sys.argv[4]
	remoteDir = sys.argv[5]
	remoteId = sys.argv[6]
	backedUp = sys.argv[7]
	
	if timePoint != 'None':
		outlog = os.path.join(projDir,'temp','runlog'+sampleName+'-'+timePoint+'-'+runId)
	else:
		outlog = os.path.join(projDir,'temp','runlog'+sampleName+'-'+runId)
	with open(outlog, 'a') as logfile:
		logfile.write('Execution started at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
		if backedUp == 'Yes':
			logfile.write('This run was archived\n')
		elif backedUp == 'No':
			logfile.write('This run was not yet archived\n')

	#copy the bam & index files
	copybam(projDir,sampleName,timePoint,runId,remoteDir,remoteId,backedUp,outlog)
	
	# run the RNASeqPlugin
	run_rnaseqPlugin(projDir,sampleName,timePoint,runId,outlog)
	
	with open(outlog, 'a') as logfile:
		logfile.write('finished RNASeqPlugin\n')
		logfile.write('Execution ended at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
	
	#move the runlog file to the run directory
	if timePoint != 'None':
		os.rename(outlog, os.path.join(projDir,sampleName,timePoint,runId,'runlog'))
	else:
		os.rename(outlog, os.path.join(projDir,sampleName,runId,'runlog'))
