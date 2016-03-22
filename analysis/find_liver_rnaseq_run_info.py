import os,sys
import re
def findruninfo():

	#com1 = '"cd /mnt/Charon/archivedReports; find -maxdepth 1 -type d -name \'*LV*\' > pluto_archived_list.txt;"'
	com1 = '"cd /mnt/Triton/archivedReports; find -maxdepth 1 -type d -name \'*LV*\' > mercury_archived_list.txt;"'
	#command = 'sshpass -p %s ssh ionadmin@192.168.200.42 %s' %('ionadmin',com1)
	command = 'sshpass -p %s ssh ionadmin@192.168.200.41 %s' %('ionadmin',com1)
	#print command
	os.system(command)

def sortdata():
	sampleList = ['LV4_T0-1','LV4_T0-2','LV4_T1_-80','LV4_T1-80','LV4_T2_-80','LV4_T2-80','LV4_T1-LN2','LV4_T1_LN2','LV4_T2-LN2','LV4_T2_LN2',\
			'LV5_T0-1','LV5_T0-2','LV5_T1_-80','LV5_T1-80','LV5_T2_-80','LV5_T2-80','LV5_T1-LN2','LV5_T2-LN2','LV5_T2_LN2',\
			'LV6_T0-2','LV6_T1_-80','LV6_T1-80','LV6_T2-LN2']
	

	with open('/rawdata/projects/RNA-seq/Liver/mercury_archived_list_120715.txt','r') as f:
		for line in f:
			#if sampleList[1] in line and 'tn' not in line:
			if sampleList[17] in line or sampleList[18] in line  and 'tn' not in line:	
				print line[12:][:-6]
				#print line[12:][:-6].replace('-'+sampleList[8]+'_',"")


	with open('/rawdata/projects/RNA-seq/Liver/pluto_archived_list_120715.txt','r') as f:	
		for line in f:
			#if sampleList[1] in line and 'tn' not in line:
			if sampleList[17] in line or sampleList[18] in line  and 'tn' not in line:	
				print line[12:][:-6]
				#print line[12:][:-6].replace('-'+sampleList[8]+'_',"")


if __name__ == "__main__":
	#findruninfo()
	sortdata()
