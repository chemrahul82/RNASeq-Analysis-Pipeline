#single run
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_484 None Run1 Auto_user_Pluto-873-Lung_Squamous_RNA_LS0484_Run1_A_946_1819 PLU No > /rawdata/projects/RNA-seq/temp/temp1 &
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_549 None Run1 Auto_user_Pluto-875-Lung_Squamous_RNA_LS0549_Run1_A_948_1823 PLU No > /rawdata/projects/RNA-seq/temp/temp2 &
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_484 None Run2 Auto_user_Pluto-882-Lung_Squamous_RNA_LS0484_Run1_A_956_1837 PLU No > /rawdata/projects/RNA-seq/temp/temp3 &
#sleep 10
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_549 None Run2 Auto_user_Mercury-507-Lung_Squamous_RNA_LS549_Run1_B_911_1776 MER No > /rawdata/projects/RNA-seq/temp/temp4 &
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_543 None Run1 Auto_user_Mercury-499-Lung_Squamous_RNA_LS543_Run1_B_902_1760 MER No > /rawdata/projects/RNA-seq/temp/temp5 &
#sleep 10
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_543 None Run2 Auto_user_Pluto-883-Lung_Squamous_RNA_LS0543_Run1_A_957_1839 PLU No > /rawdata/projects/RNA-seq/temp/temp6 &
#sleep 10
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_559 None Run1 Auto_user_Pluto-874-Lung_Squamous_RNA_LS0559_Run1_A_947_1821 PLU No > /rawdata/projects/RNA-seq/temp/temp7 &
#sleep 10
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_559 None Run2 Auto_user_Mercury-506-Lung_Squamous_RNA_LS559_Run2_B_910_1774 MER No > /rawdata/projects/RNA-seq/temp/temp8 &
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_621 None Run1 Auto_user_Pluto-881-Lung_Squamous_RNA_LS0621_Run1_B_955_1835 PLU No > /rawdata/projects/RNA-seq/temp/temp9 &
#sleep 5m
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_462 None Run1 Auto_user_Pluto-885-Lung_Squamous_RNA_LS0462_Run1_A_959_1843 PLU No > /rawdata/projects/RNA-seq/temp/temp10 &
#sleep 5m
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_576 None Run1 Auto_user_Mercury-505-Lung_Squamous_RNA_LS576_Run2_A_909_1772 MER No > /rawdata/projects/RNA-seq/temp/temp11 &
#sleep 5m
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_485 None Run1 Auto_user_Mercury-509-Lung_Squamous_RNA_LS0485_Run1_B_914_1780 MER No > /rawdata/projects/RNA-seq/temp/temp12 &
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_445 None Run1 Auto_user_Mercury-511-Lung_Squamous_RNA_LS0445_Run1_A_916_1784 MER No > /rawdata/projects/RNA-seq/temp/temp13 &
#nohup python -u rnaSeqpipe_032316.py /rawdata/projects/RNA-seq/LS LS_621 None Run2 Auto_user_Mercury-513-Lung_Squamous_RNA_LS0621_Run2_B_921_1788 MER No > /dev/null 2>&1& #bam file was missing
#sleep 5m
#nohup python -u rnaSeqpipe_032316.py /rawdata/projects/RNA-seq/LS LS_485 None Run2 Auto_user_Mercury-512-Lung_Squamous_RNA_LS0485_Run2_B_920_1786 MER No > /dev/null 2>&1& # bam file was missing
#sleep 5m
#nohup python -u rnaSeqpipe_032316.py /rawdata/projects/RNA-seq/LS LS_564 None Run1 Auto_user_Pluto-888-Lung_Squamous_RNA_LS0564_Run2_A_962_1849 PLU No > /dev/null 2>&1&
#sleep 5m
#nohup python -u rnaSeqpipe_032316.py /rawdata/projects/RNA-seq/LS LS_576 None Run2 Auto_user_Pluto-889-Lung_Squamous_RNA_LS0576_Run2_A_963_1851 PLU No > /dev/null 2>&1&





#merge runs
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_484 None Merged NA NA NA merged > nohup.out 2>&1&
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_576 None Merged NA NA NA merged > /dev/null 2>&1&
#nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_549 None Merged NA NA NA merged > /dev/null 2>&1& 
nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_543 None Merged NA NA NA merged > /dev/null 2>&1&
nohup python -u rnaSeqpipe.py /rawdata/projects/RNA-seq/LS LS_559 None Merged NA NA NA merged > /dev/null 2>&1&
