''' 
This script computes the intersection of genes across all the runs of a sample;
Next, it computes the intersection of the above set from a sample with other samples;
It computes intersection of the above set from a sample with several reference henes sets

Author: Rahul K. Das
Date: 12/15/2015

'''

import os, sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import cumfreq
import time

#ensemble gene id to gene name mapping; save into dictionary 
def ensemble2gene():
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	id2name = {}
	with open('%s/human_ensemble_gene_id_to_name.txt' %supportDir, 'rb') as mapf:
		reader = csv.reader(mapf)
		next(reader)
		for line in reader:
			id2name[line[0]] = line[1]
	return id2name		

#list of genes that are covered by at least 10 reads and have at least 1 isoform with FPKM >= 0.3
def genes_express(projDir, isam, itim, irun, prefix):
	id2name = ensemble2gene()
	genes_cov= []
	with open('%s/%s/%s/%s/%s.genereads.xls' %(projDir, isam, itim, irun,prefix), 'rb') as genef:
		reader = csv.reader(genef,delimiter = '\t')
		#ngenes = 0
		next(reader)
		for line in reader:
			if int(line[1]) >= 10:
				#ngenes += 1
				genes_cov.append(line[0])
	
	genesIso = []
	with open('%s/%s/%s/%s/%s.geneisoexp_fpkm_15.xls' %(projDir, isam, itim, irun,prefix), 'rb') as isof:
		reader = csv.reader(isof,delimiter = '\t')
		next(reader)
		for line in reader:
			if int(line[2]) != 0:
				if line[0].split('.')[0] in id2name:
					genesIso.append(id2name[line[0].split('.')[0]])
	geneIsoIntersect = (list(set(genes_cov) & set(genesIso)))
	
	return geneIsoIntersect

#human housekeeping genes
def hk_genes():
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	hk_genesList = []
	with open('%s/human_housekeeping_genes.txt' %supportDir, 'rb') as hk:
		reader = csv.reader(hk, delimiter = '\t')
		for line in reader:
			hk_genesList.append(line[0].strip())
	return hk_genesList

#human liver transcriptome(Yu et al., Genomics 2010)
def atlas_genes():
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	atlas_genesList = []
	with open('%s/human_liver_transcriptome.txt' %supportDir, 'rb') as tra:
		for line in tra:
			atlas_genesList.append(line.strip())
	return atlas_genesList

#human liver enriched genes (Yu et al., Genomics 2010)
def enrich_genes():
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	enrich_genesList = []
	with open('%s/human_liver_enriched_genes.txt' %supportDir, 'rb') as enr:
		for line in enr:
			enrich_genesList.append(line.strip())
	return enrich_genesList


#list of genes that Tomo has provided for LS; includes housekeeping and genes of interest
#03/22/2016
def ls_genes():
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	ls_genesList = []
	with open('%s/ls_genes_tomo.txt' %supportDir, 'rb') as ls:
		for line in ls:
			ls_genesList.append(line.strip())
	return ls_genesList


def transcript_express_compare():
	#samples = ['LV4','LV5','LV6']
	samples = ['LV5',]
	#times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
	times = ['T2-80']
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
	#existRuns = [[[] for i in range(len(times))] for j in range(len(samples))]

	hk_genesList = hk_genes()
	atlas_genesList = atlas_genes()
	enrich_genesList = enrich_genes()
	
	#print len(list(set(hk_genesList) & set(atlas_genesList)))
	#time.sleep(60)
	
	# Master list for storing overlapping genes/isoforms across runs for  different time points for all samples
	overlapList = [[[] for j in range(len(times))] for k in range(len(samples))]
	overlapNumber = [[[] for j in range(len(times))] for k in range(len(samples))]
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
				
				genes_runs = [[] for i in range(5)]
				#loop over existing runs
				for irun in runs:
					if os.path.exists('%s/%s/%s/%s/%s.isoforms.fpkm_tracking' %(projDir, isam, itim, irun,prefix)):
						nruns += 1
						stats = genes_express(projDir, isam, itim, irun, prefix)
						#print len(list(set(stats) & set(hk_genesList)))
						genes_runs[nruns-1] = stats
				overlapList[nsamples-1][ntimes-1] = list(set.intersection(*map(set, genes_runs[0:nruns])))
				#overlapNumber[nsamples-1][ntimes-1] = len(list(set.intersection(*map(set, genes_runs[0:nruns]))))
				print '\t'.join(map(str,[isam, itim, len(list(set.intersection(*map(set, genes_runs[0:nruns])))),\
						len(list(set.intersection(*map(set, genes_runs[0:nruns])) & set(hk_genesList))),\
						len(list(set.intersection(*map(set, genes_runs[0:nruns])) & set(atlas_genesList))),\
						len(list(set.intersection(*map(set, genes_runs[0:nruns])) & set(enrich_genesList))),\
						len(list((set.intersection(*map(set, genes_runs[0:nruns])) & set(atlas_genesList)) & set(hk_genesList)))]))

				#print (list(set(enrich_genesList) & set(hk_genesList)))

	time.sleep(60)
	#save length of intersection for longitudinal and inter 
	with open('total_genes_overlap_longitud.txt', 'w') as flong,\
			open('total_genes_overlap_inter.txt', 'w') as finter:
		flong.write('\t'.join(['Runi_sect_Runj','Runi_isect_Runj_isect_HK','Runi_isect_Runj_isect_Atlas', 'Runi_isect_Runj_isect_HK_isect_Atlas'])+'\n')
		finter.write('\t'.join(['Runi_sect_Runj','Runi_isect_Runj_isect_HK','Runi_isect_Runj_isect_Atlas', 'Runi_isect_Runj_isect_HK_isect_Atlas'])+'\n')
		for isample in range(len(samples)):
			for jsample in range(len(samples)):
				#Longitudinal & Intra
				if isample == jsample:
					for itime in range(len(existTimes[isample])):
						for jtime in range(len(existTimes[jsample])):
							#store the longitudinal correlation
							if jtime > itime:
								#intersection between two runs
								intersectList = list(set(overlapList[isample][itime]) & set(overlapList[jsample][jtime]))
								intersectLen = len(intersectList)
								#(Run1-intersect-Run2)-intersect-HKgenes
								inters_hk = list(set(intersectList) & set(hk_genesList))
								inters_hk_len = len(inters_hk)
								#(Run1-intersect-Run2)-intersect-Atlasgenes
								inters_at = list(set(intersectList) & set(atlas_genesList))
								inters_at_len = len(inters_at)
								#(Run1-intersect-Run2)-intersect-Atlasgenes-intersect-HKgenes
								inters_at_hk = list(set(inters_hk) & set(atlas_genesList))
								inters_at_hk_len = len(inters_at_hk)
								flong.write('\t'.join(map(str,[samples[isample], existTimes[isample][itime], samples[jsample],\
										existTimes[jsample][jtime], intersectLen, inters_hk_len, inters_at_len, inters_at_hk_len]))+'\n')
				#Inter
				elif jsample > isample:
					for itime in range(len(existTimes[isample])):
						for jtime in range(len(existTimes[jsample])):
							#intersection between two runs
							intersectList = list(set(overlapList[isample][itime]) & set(overlapList[jsample][jtime]))
							intersectLen = len(intersectList)
							#(Run1-intersect-Run2)-intersect-HKgenes
							inters_hk = list(set(intersectList) & set(hk_genesList))
							inters_hk_len = len(inters_hk)
							#(Run1-intersect-Run2)-intersect-Atlasgenes
							inters_at = list(set(intersectList) & set(atlas_genesList))
							inters_at_len = len(inters_at)
							#(Run1-intersect-Run2)-intersect-Atlasgenes-intersect-HKgenes
							inters_at_hk = list(set(inters_hk) & set(atlas_genesList))
							inters_at_hk_len = len(inters_at_hk)
							finter.write('\t'.join(map(str,[samples[isample], existTimes[isample][itime], samples[jsample],\
									existTimes[jsample][jtime], intersectLen, inters_hk_len, inters_at_len, inters_at_hk_len]))+'\n')

if __name__ == '__main__':
	transcript_express_compare()

