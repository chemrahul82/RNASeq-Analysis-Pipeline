''' 
This script reads the fpkm_tracking output files for genes and transcripts, sorts them by the names of
the genes or transcripts, and then compare correlations among pairs of runs from same sample (intra),
or across different runs from different samples (inter and longitudinal) 
Author: Rahul K. Das
Date: 12/15/2015

'''

import os, sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import cumfreq


def transcript_express_compare():
	samples = ['LV4','LV5','LV6']
	#samples = ['LV4','LV6']
	times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
	#times = ['T0-2','T1-80']
	runs = ['Run1','Run2','Run3','Run4','Run5']
	#runs = ['Run2','Run3']
	projDir = '/rawdata/projects/RNA-seq/Liver'
	scriptDir = '/rawdata/projects/RNA-seq/scripts'
	prefix = 'RNA_Barcode_None_001_rawlib'
	
	#list for storing existing time points for all samples 
	existTimes = [[] for j in range(len(samples))]
	#list for storing total runs for different time points for all samples
	nruns_times = [[] for j in range(len(samples))]
	#list for storing existing Run ids for different time points for all samples
	existRuns = [[[] for i in range(len(times))] for j in range(len(samples))]

	
	#4D Master list for storing fpkm values for genes/isoforms for different runs at different time points for all samples
	fpkm_t_runs = [[[[] for i in range(len(runs))] for j in range(len(times))] for k in range(len(samples))]
	fpkm_g_runs = [[[[] for i in range(len(runs))] for j in range(len(times))] for k in range(len(samples))]
	nsamples = 0

	for isam in samples:
		nsamples += 1
		#counter for existing time point
		ntimes = 0
		#loop over existing time points
		for itim in times:
			if os.path.exists('%s/%s/%s' %(projDir, isam, itim)):
				#print 'working on %s and %s' %(isam, itim)
				existTimes[nsamples-1].append(itim)
				ntimes += 1 
				#counter for total existing runs for a time point
				nruns = 0
				
				#loop over existing runs
				for irun in runs:
					if os.path.exists('%s/%s/%s/%s/%s.isoforms.fpkm_tracking' %(projDir, isam, itim, irun,prefix)):
						nruns += 1
						existRuns[nsamples-1][ntimes-1].append(irun)
						#lists for storing gene/isoform ids and fpkm values for runs
						trans = []
						genes = []
						fpkm_t = []
						fpkm_g = []
						#for a run extract the transcript id and FPKM value
						with open('%s/%s/%s/%s/%s.isoforms.fpkm_tracking' %(projDir, isam, itim, irun,prefix), 'rb') as f:
							reader = csv.reader(f,delimiter = '\t')
							next(reader)
							for line in reader:
								trans.append(line[0])
								fpkm_t.append(line[9])
						zipList1 = zip(trans, fpkm_t)
						#sort the list by the transcript id, this is required for comparing FPKM values across different runs
						sortedList1 = sorted(zipList1, key = lambda x: x[0])
						for i in range(len(sortedList1)):
							fpkm_t_runs[nsamples-1][ntimes-1][nruns-1].append(float(sortedList1[i][1]))
					
						#for a run extract the gene id and FPKM value
						with open('%s/%s/%s/%s/%s.genes.fpkm_tracking' %(projDir, isam, itim, irun,prefix), 'rb') as f:
							reader = csv.reader(f,delimiter = '\t')
							next(reader)
							for line in reader:
								genes.append(line[0])
								fpkm_g.append(line[9])
						zipList2 = zip(genes, fpkm_g)
						#sort the list by the gene id, this is required for comparing FPKM values across different runs
						sortedList2 = sorted(zipList2, key = lambda x: x[0])
						for i in range(len(sortedList2)):
							fpkm_g_runs[nsamples-1][ntimes-1][nruns-1].append(float(sortedList2[i][1]))

					
				#make intra-run-scatter correlation plots for a given time point of a sample
				fig = plt.figure()
				fig.text(0.5, 0.04, 'log2(FPKM+1)', ha='center', va='center', family='serif',size='medium', weight = 'bold')
				fig.text(0.06, 0.5, 'log2(FPKM+1)', ha='center', va='center', rotation='vertical', family='serif',size='medium', weight = 'bold')
				fig.suptitle('%s' %(isam+'-'+itim), family='serif',size='large', weight = 'bold')
				nc  = 0
				for i in range(nruns):
					for j in range(nruns):
						nc += 1
						#plot the pair correlation plots for the transcript expression in the upper triangle
						if j > i:
							plt.subplot(nruns, nruns, nc)
							transCorr = np.corrcoef(fpkm_t_runs[nsamples-1][ntimes-1][i], fpkm_t_runs[nsamples-1][ntimes-1][j])[0][1]
							title = str(i+1)+'-'+str(j+1)+' (r = %4.3f)' %(transCorr)
							plt.title('%s' %title)
							plt.plot(np.log2((np.array(fpkm_t_runs[nsamples-1][ntimes-1][i])) + 1), np.log2((np.array(fpkm_t_runs[nsamples-1][ntimes-1][j])) + 1),'bo', markersize = 4)
							plt.subplots_adjust(hspace = .5)
						#plot the pair correlation plots for the transcript expression in the lower triangle	
						elif j < i:
							plt.subplot(nruns, nruns, nc)
							genesCorr = np.corrcoef(fpkm_g_runs[nsamples-1][ntimes-1][i], fpkm_g_runs[nsamples-1][ntimes-1][j])[0][1]
							title = str(i+1)+'-'+str(j+1)+' (r = %4.3f)' %(genesCorr)
							plt.title('%s' %title)
							plt.plot(np.log2((np.array(fpkm_g_runs[nsamples-1][ntimes-1][i])) + 1), np.log2((np.array(fpkm_g_runs[nsamples-1][ntimes-1][j])) + 1),'ro', markersize = 4)
							plt.subplots_adjust(hspace = .5)

				matplotlib.rcParams.update({'font.size': 6})
				matplotlib.rcParams.update({'font.family': 'serif'})
				plt.savefig("%s.png" %(isam+'-'+itim+'-'+'ExpressCorr'), dpi = 300)
				plt.close(fig)
				
				nruns_times[nsamples-1].append(nruns)
	
	#save intra, longitudinal, and inter correlation coefficients
	with open('expression_correlation_intra.txt', 'w') as fintra, open('expression_correlation_longitud.txt', 'w') as flong,\
			open('expression_correlation_inter.txt', 'w') as finter:
		for isample in range(len(samples)):
			for jsample in range(len(samples)):
				#Longitudinal & Intra
				if isample == jsample:
					for itime in range(len(existTimes[isample])):
						for jtime in range(len(existTimes[jsample])):
							#store the longitudinal correlation
							if jtime > itime:
								for irun in range(nruns_times[isample][itime]):
									for jrun in range(nruns_times[jsample][jtime]):
										long_t_r = np.corrcoef(fpkm_t_runs[isample][itime][irun], fpkm_t_runs[jsample][jtime][jrun])[0][1]
										long_g_r = np.corrcoef(fpkm_g_runs[isample][itime][irun], fpkm_g_runs[jsample][jtime][jrun])[0][1]
										flong.write('\t'.join(map(str,[samples[isample], existTimes[isample][itime], existRuns[isample][itime][irun],\
												samples[jsample], existTimes[jsample][jtime], existRuns[jsample][jtime][jrun], long_g_r, long_t_r]))+'\n')
							#store the intra correlation coeff. across differenr runs for same time point
							elif itime == jtime:
								for irun in range(nruns_times[isample][itime]):
									for jrun in range(nruns_times[jsample][jtime]):
										if jrun > irun:
											intra_t_r = np.corrcoef(fpkm_t_runs[isample][itime][irun], fpkm_t_runs[jsample][jtime][jrun])[0][1]
											intra_g_r = np.corrcoef(fpkm_g_runs[isample][itime][irun], fpkm_g_runs[jsample][jtime][jrun])[0][1]
											fintra.write('\t'.join(map(str,[samples[isample], existTimes[isample][itime], existRuns[isample][itime][irun],\
													samples[jsample], existTimes[jsample][jtime], existRuns[jsample][jtime][jrun], intra_g_r, intra_t_r]))+'\n')
				#Inter
				elif jsample > isample:
					for itime in range(len(existTimes[isample])):
						for jtime in range(len(existTimes[jsample])):
							for irun in range(nruns_times[isample][itime]):
								for jrun in range(nruns_times[jsample][jtime]):
									inter_t_r = np.corrcoef(fpkm_t_runs[isample][itime][irun], fpkm_t_runs[jsample][jtime][jrun])[0][1]
									inter_g_r = np.corrcoef(fpkm_g_runs[isample][itime][irun], fpkm_g_runs[jsample][jtime][jrun])[0][1]
									finter.write('\t'.join(map(str,[samples[isample], existTimes[isample][itime], existRuns[isample][itime][irun],\
											samples[jsample], existTimes[jsample][jtime], existRuns[jsample][jtime][jrun], inter_g_r, inter_t_r]))+'\n')
						

if __name__ == '__main__':
	transcript_express_compare()

