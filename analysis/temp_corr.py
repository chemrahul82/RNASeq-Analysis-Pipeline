import csv
import numpy as np
import collections

dict1= {}
with open('/rawdata/projects/RNA-seq/Liver/LV4/T0-1/Run1/RNA_Barcode_None_001_rawlib.isoforms.fpkm_tracking','rb') as f1:
	reader = csv.reader(f1,delimiter = '\t')
	next(reader)
	for line in reader:
		dict1[line[0]] = line[9]
	od1 = collections.OrderedDict(sorted(dict1.items()))	
list1 = [float(v) for k, v in od1.iteritems()]
	
dict2= {}
with open('/rawdata/projects/RNA-seq/Liver/LV6/T1-80/Run2/RNA_Barcode_None_001_rawlib.isoforms.fpkm_tracking','rb') as f2:
	reader = csv.reader(f2,delimiter = '\t')
	next(reader)
	for line in reader:
		dict2[line[0]] = line[9]
	od2 = collections.OrderedDict(sorted(dict2.items()))	
list2 = [float(v) for k, v in od2.iteritems()]
print np.corrcoef(list1, list2)[0][1]	
	



