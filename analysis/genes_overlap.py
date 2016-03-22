import os, sys
import csv

def genes_overlap():
	#samples = ['LV4','LV5','LV6']
	samples = ['LV4']
	#times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
	times = ['T0-1','T2-LN2']
	runs = ['Run1','Run2','Run3','Run4','Run5']
	projDir = '/rawdata/projects/RNA-seq/Liver'
	scriptDir = '/rawdata/projects/RNA-seq/scripts'
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	prefix = 'RNA_Barcode_None_001_rawlib'

	control_list = []
	with open('%s/liver_human_transcriptome_atlas.txt' %supportDir, 'r') as tra:
		for line in tra:
			control_list.append(line.strip())
		
	
	for isample in samples:
		for itime in times:
			if os.path.exists('%s/%s/%s' %(projDir, isample, itime)):
				for irun in runs:
					if os.path.exists('%s/%s/%s/%s/%s.genereads.xls' %(projDir, isample, itime, irun,prefix)):
						run_list = []
						with open('%s/%s/%s/%s/%s.genereads.xls' %(projDir, isample, itime, irun,prefix), 'rb') as f:
							reader = csv.reader(f,delimiter = '\t')
							next(reader)
							for line in reader:
								if int(line[1]) >= 1500:
									run_list.append(line[0])
						print isample, itime			
						print len(run_list)		
						print len(list(set(control_list) & set(run_list)))		

if __name__ == '__main__':
	genes_overlap()

