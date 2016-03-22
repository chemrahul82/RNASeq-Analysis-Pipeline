"""
compute median and mean of read coverage and abundance (FPKM)for different reference genes sets
(e.g. house-keeping genes, liver-enriched genes) expressed in our RNA-Seq
Author:Rahul Das

"""
import os, sys
import csv
import numpy as np

#human housekeeping genes
def hk_genes():
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	hk_genesList = []
	with open('%s/human_housekeeping_genes.txt' %supportDir, 'rb') as hk:
		reader = csv.reader(hk, delimiter = '\t')
		for line in reader:
			hk_genesList.append(line[0].strip())
	return hk_genesList

#liver enriched genes
def le_genes():
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	le_genesList = []
	with open('%s/human_liver_enriched_genes.txt' %supportDir, 'rb') as le:
		reader = csv.reader(le, delimiter = '\t')
		for line in reader:
			le_genesList.append(line[0].strip())
	return le_genesList

#PNET fusion genes
def fus_genes():
	supportDir = '/rawdata/projects/RNA-seq/support_files'
	fus_genesList = []
	with open('%s/PNET_fusion_genes.txt' %supportDir, 'rb') as fus:
		reader = csv.reader(fus, delimiter = '\t')
		for line in reader:
			fus_genesList.append(line[0].strip())
	return fus_genesList



def ref_genes_coverage():
	#Liver samples
	#samples = ['LV4','LV5','LV6']
	#samples = ['LV5']
	#times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
	#times  = ['T2-80']
	#runs = ['Run1']
	#runs = ['Run1','Run2','Run3','Run4','Run5']
	#projDir = '/rawdata/projects/RNA-seq/Liver'
	
	#PNET samples
	samples = ['RNA_483','RNA_487','RNA_489']
	times=['']
	runs = ['Run1','Run2','Run3']
	projDir = '/rawdata/projects/RNA-seq/PNET'


	prefix = 'RNA_Barcode_None_001_rawlib'
	fout = open('hk_genes_cov_median_mean.txt','wb')
	fout.write('\t'.join(['Median','Mean'])+'\n')
	f2out = open('le_genes_cov_median_mean.txt','wb')
	f2out.write('\t'.join(['Median','Mean'])+'\n')
	f6out = open('fus_genes_cov_median_mean.txt','wb')
	f6out.write('\t'.join(['Median','Mean'])+'\n')
	#f1out = open('all_genes_cov_median_mean.txt','wb')
	#f1out.write('\t'.join(['Median','Mean'])+'\n')
	f3out = open('hk_genes_fpkm_nedian_mean.txt','wb')
	f3out.write('\t'.join(['Median','Mean'])+'\n')
	f4out = open('le_genes_fpkm_nedian_mean.txt','wb')
	f4out.write('\t'.join(['Median','Mean'])+'\n')
	f5out = open('fus_genes_fpkm_nedian_mean.txt','wb')
	f5out.write('\t'.join(['Median','Mean'])+'\n')

	hk_genesList = hk_genes()
	le_genesList = le_genes()
	fus_genesList = fus_genes()

	for isam in samples:
		for itim in times:
			if os.path.exists('%s/%s/%s' %(projDir, isam, itim)):
				for irun in runs:
					#read depth of coverage for genes present in the reference sets
					#genes_cov = []
					le_cov = []
					hk_cov = []
					fus_cov = []

					if os.path.exists('%s/%s/%s/%s/%s.genereads.xls' %(projDir, isam, itim, irun,prefix)):
						with open('%s/%s/%s/%s/%s.genereads.xls' %(projDir, isam, itim, irun,prefix)) as cov:
							reader = csv.reader(cov, delimiter = '\t')
							next(reader)
							for line in reader:
								#genes_cov.append(int(line[1]))
								if line[0] in hk_genesList:
									hk_cov.append(int(line[1]))
								if line[0] in le_genesList:	
									le_cov.append(int(line[1]))
								if line[0] in fus_genesList:
									fus_cov.append(int(line[1]))

						#f1out.write('\t'.join(map(str,[np.median(genes_cov), np.mean(genes_cov)]))+'\n')
						fout.write('\t'.join(map(str,[np.median(hk_cov), np.mean(hk_cov)]))+'\n')
						f2out.write('\t'.join(map(str,[np.median(le_cov), np.mean(le_cov)]))+'\n')
						f6out.write('\t'.join(map(str,[np.median(fus_cov), np.mean(fus_cov)]))+'\n')			
			

					#get fpkm of the genes present in the reference sets	
					genes_fpkm = {}
					hk_genes_fpkm = []
					le_genes_fpkm = []
					fus_genes_fpkm = []

					if os.path.exists('%s/%s/%s/%s/%s.genes.fpkm_tracking' %(projDir, isam, itim, irun,prefix)):
						with open('%s/%s/%s/%s/%s.genes.fpkm_tracking' %(projDir, isam, itim, irun,prefix)) as gf:
							reader = csv.reader(gf, delimiter = '\t')
							next(reader)
							for line in reader:
								genes_fpkm[line[4]] = line[9]
													
						for genes in hk_genesList:
							if genes in genes_fpkm:
								hk_genes_fpkm.append(float(genes_fpkm[genes]))
						for genes in le_genesList:
							if genes in genes_fpkm:
								le_genes_fpkm.append(float(genes_fpkm[genes]))
						for genes in fus_genesList:
							if genes in genes_fpkm:
								fus_genes_fpkm.append(float(genes_fpkm[genes]))
						
					
						f3out.write('\t'.join(map(str,[np.median(hk_genes_fpkm), np.mean(hk_genes_fpkm)]))+'\n')
						f4out.write('\t'.join(map(str,[np.median(le_genes_fpkm), np.mean(le_genes_fpkm)]))+'\n')
						f5out.write('\t'.join(map(str,[np.median(fus_genes_fpkm), np.mean(fus_genes_fpkm)]))+'\n')

	fout.close()	
	#f1out.close()
	f2out.close()
	f3out.close()
	f4out.close()
	f5out.close()
	f6out.close()
if __name__ == '__main__':
	ref_genes_coverage()



