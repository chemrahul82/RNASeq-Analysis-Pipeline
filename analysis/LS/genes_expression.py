#print fpkm expression values for candidate genes
#Rahul Das

import os, sys
import time
#<usage> python ls_genes_expression.py <samplename> <runid>

#list of genes that Tomo has provided for LS; includes housekeeping and genes of interest
#03/22/2016
def ls_genes():
        supportDir = '/rawdata/projects/RNA-seq/support_files'
        ls_genesList = []
        with open('%s/ls_genes_tomo.txt' %supportDir, 'rb') as ls:
                for line in ls:
                        ls_genesList.append(line.strip())
        return ls_genesList

def expression_genes_interest(samplename, Runid):
	genes_fpkm = []
	ls_genesList = ls_genes()
	rundir=os.path.join('/rawdata/projects/RNA-seq/LS',samplename,Runid)
	outfile = open(os.path.join(rundir,'candidate_genes_expression_%s_%s.txt' %(samplename,Runid)),'w')
	
	for file in os.listdir(rundir):	
		if file.endswith('.genes.fpkm_tracking'):
			genesfile = os.path.join(rundir,file)
			
	with open(genesfile, 'r') as genef:
		next(genef)
		genename =[line.split('\t')[4] for line in genef]

	with open(genesfile, 'r') as genef:
		next(genef)
		fpkm = [line.split('\t')[9] for line in genef]
	
	for lsgene in ls_genesList:
		for idx, genes in enumerate(genename):
			if lsgene == genes:
				#print('\t'.join([lsgene, fpkm[idx]]))	
				outfile.write('\t'.join([lsgene, fpkm[idx]])+'\n')
	outfile.close()
if __name__ == "__main__":
	samplename = sys.argv[1]
	runid = sys.argv[2]
	expression_genes_interest(samplename, runid)
			
