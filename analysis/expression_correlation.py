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


def expression_compare(inpList):
	#samples = ['LV4','LV5','LV6']
	#samples = ['LV6']
	#times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
	#times = ['T0-2','T1-80']
	#runs = ['Run1','Run2','Run3','Run4','Run5']
	projDir = '/rawdata/projects/RNA-seq/Liver'
	scriptDir = '/rawdata/projects/RNA-seq/scripts'
	prefix = 'RNA_Barcode_None_001_rawlib'

	fpkm_t_runs = [[] for i in range(2)]
	fpkm_g_runs = [[] for i in range(2)]
	
	for isam in range(2):
		if os.path.exists('%s/%s/%s/%s/%s.isoforms.fpkm_tracking' %(projDir, inpList[0+3*isam], inpList[1+3*isam], inpList[2+3*isam], prefix)):
			#print ('%s/%s/%s/%s/%s.isoforms.fpkm_tracking' %(projDir, inpList[0+3*isam], inpList[1+3*isam], inpList[2+3*isam], prefix))
			#lists for storing gene/isoform ids 
			trans = []
			genes = []
			fpkm_t = []
			fpkm_g = []
			#for a run extract the transcript id and FPKM value
			with open('%s/%s/%s/%s/%s.isoforms.fpkm_tracking' %(projDir, inpList[0+3*isam], inpList[1+3*isam], inpList[2+3*isam], prefix), 'rb') as f1:
				reader = csv.reader(f1,delimiter = '\t')
				next(reader)
				for line in reader:
					trans.append(line[0])
					fpkm_t.append(line[9])
				zipList1 = zip(trans, fpkm_t)
				#sort the list by the transcript id, this is required for comparing FPKM values across different runs
				sortedList1 = sorted(zipList1, key = lambda x: x[0])
				for i in range(len(sortedList1)):
					fpkm_t_runs[isam].append(float(sortedList1[i][1]))
					
			#for a run extract the gene id and FPKM value
			with open('%s/%s/%s/%s/%s.genes.fpkm_tracking' %(projDir, inpList[0+3*isam], inpList[1+3*isam], inpList[2+3*isam], prefix), 'rb') as f2:
				reader = csv.reader(f2,delimiter = '\t')
				next(reader)
				for line in reader:
					genes.append(line[0])
					fpkm_g.append(line[9])
				zipList2 = zip(genes, fpkm_g)
				#sort the list by the gene id, this is required for comparing FPKM values across different runs
				sortedList2 = sorted(zipList2, key = lambda x: x[0])
				for i in range(len(sortedList2)):
					fpkm_g_runs[isam].append(float(sortedList2[i][1]))
													

	return fpkm_t_runs, fpkm_g_runs


def intra_corr():
	#samples = ['LV4','LV5','LV6']
	samples = ['LV4','LV6']
	#times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
	times = ['T0-2','T1-80']
	runs = ['Run1','Run2','Run3','Run4','Run5']
	projDir = '/rawdata/projects/RNA-seq/Liver'

	
	for isample in samples:
		for jsample in samples:
			if isample == jsample:
				for itime in times:
					os.listdir('%s/%s/%s' %(projDir,isample)
					for jtime in times:
						if itime == jtime:
							v=fig = plt.figure()
							fig.text(0.5, 0.04, 'log2(FPKM+1)', ha='center', va='center', family='serif',size='medium', weight = 'bold')
							fig.text(0.06, 0.5, 'log2(FPKM+1)', ha='center', va='center', rotation='vertical', family='serif',size='medium', weight = 'bold')
							fig.suptitle('%s' %(isam+'-'+itim), family='serif',size='large', weight = 'bold')
							nc  = 0
							for irun in runs:
								for jrun in runs:
									if jrun > irun:
										inpList = []
										inpList.append(isample)
										inpList.append(itime)
										inpList.append(irun)
										inpList.append(jsample)
										inpList.append(jtime)
										inpList.append(jrun)
										isoexp, genesexp = expression_compare(inpList)
										if isoexp[0] and isoexp[1]:
											nc += 1
											print isample,itime,irun,jsample,jtime,jrun,np.corrcoef(isoexp[0], isoexp[1])[0][1]
											plt.subplot(nruns, nruns, nc)
											transCorr = np.corrcoef(fpkm_t_runs[ntimes-1][i], fpkm_t_runs[ntimes-1][j])[0][1]
											title = str(i+1)+'-'+str(j+1)+' (r = %4.3f)' %(transCorr)
											plt.title('%s' %title)
											plt.plot(np.log2((np.array(fpkm_t_runs[ntimes-1][i])) + 1), np.log2((np.array(fpkm_t_runs[ntimes-1][j])) + 1),'bo', markersize = 4)
											plt.subplots_adjust(hspace = .5)



if __name__ == '__main__':
	

