#!/usr/bin/python

o=open("BW_SNP_list_full_distance_to_nearest_gene","w");
with open("BW_SNP_list_full","r") as f:
    line=f.readline()
    line=line.rstrip()
    print o.write(line+"\tdistance\tgene\n")
    
o.close();
