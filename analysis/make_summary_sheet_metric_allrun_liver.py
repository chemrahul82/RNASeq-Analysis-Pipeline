""" This script will read the .stats.txt file for all runs to generate the summary spreadsheet with
all relevant metrics from analysis runs
Author: Rahul K. Das
Date: 12/14/2015                """

from __future__ import division
import os, sys
import xlsxwriter
from datetime import datetime
import csv
import time

def get_info_stat():
	samples = ['LV4','LV5','LV6']
	#samples = ['LV4']
	times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
	#times = ['T0-2']
	runs = ['Run1','Run2','Run3','Run4','Run5']
	#runs = ['Run1']
	projDir = '/rawdata/projects/RNA-seq/Liver'
	scriptDir = '/rawdata/projects/RNA-seq/scripts'
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	prefix = 'RNA_Barcode_None_001_rawlib'
	
	#Initialize the lists that will save stats for different metrics
	meanReadLen = []
	strBalan = []
	totReads = []
	percAlignReads = []
	percMapReadstoGenes = []
	totBases = []
	percAlignBases = []
	percUsableBases = []
	percmRNABases = []
	percCodBases = []
	percUTRBases = []
	percRiboBases = []
	percIntrBases = []
	percInterBases = []
	totGenes = []
	totGenes10Iso1 = []
	totIsoforms = []
	samID = []
	timID = []
	runID = []
	rin = []

    #ensemble gene id to gene name mapping; save into dictionary 
	# this file was obtained from ucsc website and using tables
	id2name = {}
	with open('%s/human_ensemble_gene_id_to_name.txt' %supportDir, 'rb') as mapf:
		reader = csv.reader(mapf)
		next(reader)
		for line in reader:
			id2name[line[0]] = line[1]
			
	
	#loop through the stats.txt file of all runs and grab relevent info and do additional downstream analyses
	for isam in samples:
		for itim in times:
			if os.path.exists('%s/%s/%s' %(projDir, isam, itim)):
				for irun in runs:
					if os.path.exists('%s/%s/%s/%s/%s.stats.txt' %(projDir, isam, itim, irun,prefix)):
						samID.append(isam)
						timID.append(itim)
						runID.append(irun)

						#RIN values
						with open('%s/Analysis/RIN_samples.txt' %projDir, 'rb') as rinf:
							reader = csv.reader(rinf,delimiter = '\t')
							for line in reader:
								if line[0] == isam and line[1] == itim:
									rin.append(line[2])

						#total genes detected with at least 10 reads; save those gene names into a list
						with open('%s/%s/%s/%s/%s.genereads.xls' %(projDir, isam, itim, irun,prefix), 'rb') as genef:	
							reader = csv.reader(genef,delimiter = '\t')
							ngenes = 0
							genes10 = []
							next(reader)
							for line in reader:
								if int(line[1]) >= 10:
									ngenes += 1
									genes10.append(line[0])
							totGenes.append(ngenes)

						#compute number of genes that have their exons covered by at least total 10 reads (cumulative),
						#as annotated by HTSeq and have at least one isoform expressed, as annotated by cufflinks
						genesIso1 = []
						with open('%s/%s/%s/%s/%s.geneisoexp.xls' %(projDir, isam, itim, irun,prefix), 'rb') as isof:
							reader = csv.reader(isof,delimiter = '\t')
							next(reader)
							for line in reader:
								#only look at the genes that have at least 1 transcript
								if int(line[2]) != 0:
									#map the ensemble id of the gene to its name (key) of the mapping dictionary
									# dictionary key finding makes it O(n) operation and faster
									# the latest ensemble id contains the version info after '.', biomart import
									#does not have that' so get rid of that
									if line[0].split('.')[0] in id2name:
										genesIso1.append(id2name[line[0].split('.')[0]])
						
						#get the length of the list of intersection of genes with at least 10 reads and at least one isoform
						totGenes10Iso1.append(len(list(set(genes10) & set(genesIso1))))
						#print list(set(genes10) -  set(genesIso1))[0:5]
										
											
						#get several metrics from .stats.txt file
						with open('%s/%s/%s/%s/%s.stats.txt' %(projDir, isam, itim, irun,prefix)) as statf:
							for line in statf:
								if 'Mean Read Length:' in line:
									meanReadLen.append(float(line.strip().split('\t')[0].split()[3]))
								if 'Strand Balance:' in line:
									strBalan.append(float(line.strip().split('\t')[0].split()[2]))
								if 'Total Reads' in line:
									tr = int(line.strip().split('\t')[0].split()[2])
									totReads.append(int(line.strip().split('\t')[0].split()[2]))
								if 'Pct Aligned:' in line:
									percAlignReads.append(float(line.strip().split('\t')[0].split()[2].split('%')[0]))
								if 'Reads Mapped to Genes:' in line:
									mapr = 100*float(line.strip().split('\t')[0].split()[4].split('%')[0])/tr
									percMapReadstoGenes.append('%5.2f' %mapr)
								if 'Total Base Reads:' in line:
									totBases.append(int(line.strip().split('\t')[0].split()[3]))
								if 'Pct Aligned Bases' in line:
									percAlignBases.append(float(line.strip().split('\t')[0].split()[3].split('%')[0]))
								if 'Pct Usable Bases' in line:
									percUsableBases.append(float(line.strip().split('\t')[0].split()[3].split('%')[0]))
								if 'Pct mRNA Bases:' in line:
									percmRNABases.append(float(line.strip().split('\t')[0].split()[3].split('%')[0]))
								if 'Pct Coding Bases:' in line:
									percCodBases.append(float(line.strip().split('\t')[0].split()[3].split('%')[0]))
								if 'Pct UTR Bases' in line:
									percUTRBases.append(float(line.strip().split('\t')[0].split()[3].split('%')[0]))
								if 'Pct Ribosomal Bases:' in line:
									percRiboBases.append(float(line.strip().split('\t')[0].split()[3].split('%')[0]))
								if 'Pct Intronic Bases:' in line:
									percIntrBases.append(float(line.strip().split('\t')[0].split()[3].split('%')[0]))
								if 'Pct Intergenic Bases:' in line:
									percInterBases.append(float(line.strip().split('\t')[0].split()[3].split('%')[0]))
								if 'Isoforms Detected:' in line:
									totIsoforms.append(int(line.strip().split('\t')[0].split()[2]))

									
	finalList = zip(samID, timID, runID, rin, totReads, percAlignReads, percMapReadstoGenes, meanReadLen, strBalan, totBases,\
			percAlignBases, percUsableBases, percmRNABases, percCodBases, percUTRBases, percRiboBases, percIntrBases, percInterBases,\
			totGenes, totIsoforms, totGenes10Iso1)

	#print to tab-delimited txt file
	#for row in finalList:
		#print('\t'.join(map(str,row))+'\n')

	#output everything into a excel spreadsheet
	currtime = datetime.now()
	wb = xlsxwriter.Workbook('Liver-RNA-Seq-Metric-Summary-Table-'+currtime.strftime('%Y-%m-%d-%H-%M-%S')+'.xlsx')
	ws = wb.add_worksheet('Metrics')
	ws.set_column('A:X', 25)
	ws.autofilter('A1:X1000')
	format1 = wb.add_format({'bold': True, 'font': 'Courier New', 'font_color': 'white', 'bg_color': 'black', 'align': 'center'})
	format2 = wb.add_format({'font': 'Courier New', 'font_color': 'black', 'align': 'center'})
	headerList = ['Sample', 'Time-Point', 'Run No.', 'Starting RIN', 'Total Reads', 'Aligned Reads (%)', 'Reads Mapped to Genes (%)', 'Mean Read Length', 'Strand Balance',\
			'Total Bases', 'Aligned Bases (%)', 'Usable Bases (%)', 'mRNA Bases (%)', 'Coding Bases (%)', 'UTR Bases (%)', 'Ribosomal RNA (%)',\
			'Intronic Bases (%)', 'Intergenic Bases (%)', 'Total Genes Detected', 'Total Isoforms Detected', 'Total Genes with >=1 Isoforms']

	for irow in range(len(finalList)):
		for icol in range(len(finalList[0])):
			ws.write(0, icol, headerList[icol], format1)
			ws.write(irow+1, icol, finalList[irow][icol], format2)
	wb.close()		

if __name__ == "__main__":
	get_info_stat()
