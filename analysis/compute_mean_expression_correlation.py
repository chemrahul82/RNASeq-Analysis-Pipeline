import os, sys
import csv
import numpy as np

samples = ['LV4','LV5','LV6']
times = ['T0-1','T0-2','T1-80','T2-80','T1-LN2','T2-LN2']
runs = ['Run1','Run2','Run3','Run4','Run5']
with open('/rawdata/projects/RNA-seq/Liver/Analysis/ExpressionCorrelations/expression_correlation_longitud.txt', 'rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for line in reader:
		if line[0] == line[3]:
			#print line[0],line[3]
			
			for itime in times:
				
				for jtime in times:
					if jtime != itime:
						temp = []
						if line[1] == itime and line[4] == jtime:
							print line[0],line[1],line[4],line[6]
							temp.append(float(line[6]))
							print np.mean(temp)




		


