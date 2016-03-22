""" This script will read the .stats.txt file for all runs to generate the summary spreadsheet with
all relevant metrics from analysis runs
Author: Rahul K. Das
Date: 12/14/2015                """

from __future__ import division
import os, sys
import xlsxwriter
from datetime import datetime

def get_info_stat():
	samples = ['LV4','LV5','LV6']
	times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
	runs = ['Run1','Run2','Run3','Run4','Run5']
	projDir = '/rawdata/projects/RNA-seq/Liver'
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
	samID = []
	timID = []
	runID = []
	rin = []

	#loop through the stats.txt file of all runs and grab relevent info
	for isam in samples:
		for itim in times:
			if os.path.exists('%s/%s/%s' %(projDir, isam, itim)):
				for irun in runs:
					if os.path.exists('%s/%s/%s/%s/%s.stats.txt' %(projDir, isam, itim, irun,prefix)):
						samID.append(isam)
						timID.append(itim)
						runID.append(irun)
						#RIN values
						with open('%s/Analysis/RIN_samples.txt' %projDir, 'r') as rinf:
							for line in rinf:
								if line.split().strip('\t')[0] == isam and line.split().strip('\t')[1] == itim:
									rin.append(line.split().strip('\t')[2])
						#metrics
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
									percMapReadstoGenes.append(100*float(line.strip().split('\t')[0].split()[4].split('%')[0])/tr)
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

	
	finalList = zip(samID, timID, runID, rin, meanReadLen, strBalan, totReads, percAlignReads, percMapReadstoGenes, totBases,\
			percAlignBases, percUsableBases, percmRNABases, percCodBases, percUTRBases, percRiboBases, percIntrBases, percInterBases)

	#print to tab-delimited txt file
	#for row in finalList:
	#	print('\t'.join(map(str,row))+'\n')

	#output everything into a excel spreadsheet
	currtime = datetime.now()
	wb = xlsxwriter.Workbook('Liver-RNA-Seq-Metric-Summary-Table-'+currtime.strftime('%Y-%m-%d-%H-%M-%S')+'.xlsx')
	ws = wb.add_worksheet('Metrics')
	ws.set_column('A:X', 30)
	ws.autofilter('A1:X1000')
	format1 = wb.add_format({'bold': True, 'font': 'Courier New', 'font_color': 'white', 'bg_color': 'black', 'align': 'center'})
	format2 = wb.add_format({'font': 'Courier New', 'font_color': 'black', 'align': 'center'})
	headerList = ['Sample', 'Time-Point', 'Run No.', 'Starting RIN', 'Mean Read Length', 'Strand Balance', 'Total Reads', 'Aligned Reads (%)', 'Reads Mapped to Genes (%)',\
			'Total Bases', 'Aligned Bases (%)', 'Usable Bases (%)', 'mRNA Bases (%)', 'Coding Bases (%)', 'UTR Bases (%)', 'Ribosomal RNA (%)',\
			'Intronic Bases (%)', 'Intergenic Bases (%)']

	for irow in range(len(finalList)):
		for icol in range(len(finalList[0])):
			ws.write(0, icol, headerList[icol], format1)
			ws.write(irow+1, icol, finalList[irow][icol], format2)
	wb.close()		

if __name__ == "__main__":
	get_info_stat()
