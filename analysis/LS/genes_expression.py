#print fpkm expression values for candidate genes
#Rahul Das

import os, sys
import time
#<usage> python ls_genes_expression.py <samplename> <runid>

#list of genes that Tomo has provided for LS; includes housekeeping and genes of interest
#03/22/2016
def ls_genes(ref_genes):
        supportDir = '/rawdata/projects/RNA-seq/support_files'
        ls_genesList = []
        with open(os.path.join(supportDir,ref_genes),'rb') as ls:
	#with open('%s/ls_genes_tomo.txt' %supportDir, 'rb') as ls:
                for line in ls:
                        ls_genesList.append(line.strip())
        return ls_genesList

def expression_genes_interest(samplename, Runid,ref_genes):
	genes_fpkm = []
	ls_genesList = ls_genes(ref_genes)
	rundir=os.path.join('/rawdata/projects/RNA-seq/LS',samplename,Runid)
	#outfile = open(os.path.join(rundir,'candidate_genes_expression_%s_%s.txt' %(samplename,Runid)),'w')
	
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
				print('\t'.join([lsgene, fpkm[idx]]))	
				#outfile.write('\t'.join([lsgene, fpkm[idx]])+'\n')
	#outfile.close()
if __name__ == "__main__":
	samplename = sys.argv[1]
	runid = sys.argv[2]
	ref_genes = sys.argv[3]
	expression_genes_interest(samplename, runid, ref_genes)

			
