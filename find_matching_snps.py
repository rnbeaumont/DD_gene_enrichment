#!/usr/bin/python
import getopt,sys

def readargs():
    inputfile=''
    genome=''
    outputfile=''
    snp=0
    dist=None
    maf_tol=0.1
    dist_tol=0.1
    maf_limit=0.0001
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hi:o:w:s:m:d:l:g:",["ifile=","ofile=","window=","snp=","maf_tol=","dist_tol=","maf_limit=","genome="])
    except getopt.GetoptError:
        print "find_matching_snps.py -i <input SNP list file> -g <input genome wide SNP file> -o <outputfile> -w <nearest gene (0) or window (1)> -s <snp number> -m <maf tolerance %> -d <distance tolerance % (for nearest gene, optional)> -l <maf lower limit (optional)>"
        sys.exit(2)
    for opt,arg in opts:
        if opt=='-h':
            print "find_matching_snps.py -i <input SNP list file> -g <input genome wide SNP file> -o <outputfile> -w <nearest gene (0) or window (1)> -s <snp number> -m <maf tolerance % (optional)> -d <distance tolerance % (for nearest gene, optional)> -l <maf lower limit (optional)>"
            sys.exit()
        elif opt in("-i","--ifile"):
            inputfile=arg
        elif opt in("-o","--ofile"):
            outputfile=arg
        elif opt in("-w","--window"):
            dist=int(arg)
        elif opt in("-s","--snp"):
            snp=int(arg)
        elif opt in("-m","--maf_tol"):
            maf_tol=float(arg)
        elif opt in("-d","--dist_tol"):
            fist_tol=float(arg)
        elif opt in("-l","--maf_limit"):
            maf_limit=float(arg)
        elif opt in("-g","--genome"):
            genome=arg
    return inputfile,outputfile,genome,snp,dist,maf_tol,dist_tol,maf_limit

if __name__ == "__main__":
    inputfile,outputfile,genome,snp,dist,maf_tol,dist_tol,maf_limit=readargs()
    if inputfile=='' or outputfile=='' or snp==0 or dist==None or genome=='':
        print "find_matching_snps.py -i <input SNP list file> -g <input genome wide SNP file> -o <outputfile> -w <nearest gene (0) or window (1)> -s <snp number> -m <maf tolerance % (optional)> -d <distance tolerance % (for nearest gene, optional)> -l <maf lower limit (optional)>"
        sys.exit(2)
    o=open(outputfile,"w")
    o.write("rsid\tchr\tpos\ta1\ta2\tmaf\tdistance\tgene(s)\n")
    f=open(inputfile,"r")
    for i in range(snp):
        f.readline()
    line=f.readline().rstrip()
    F=line.split()
    s_maf=float(F[4])
    if s_maf>0.5:
        s_maf=1-s_maf
    s_dist=int(F[5])
    s_rsid=F[0]
    s_chr=F[1]
    s_pos=F[2]
    s_gene=""
    if len(F)==7:
        s_gene=F[6]
    found=0
    f.close
    with open(genome,"r") as f:
        f.readline()
        for line in f:
            F=line.rstrip().split()
            if s_rsid==F[0]:
                found=1
            if float(F[5])>0.5:
                F[5]=1-float(F[5])
            if float(F[5])>s_maf*(1-maf_tol) and float(F[5])<s_maf*(1+maf_tol) and float(F[6])>=s_dist*(1-(dist_tol*(1-dist))) and float(F[6])<=s_dist*(1+(dist_tol*(1-dist))) and float(F[5])>maf_limit:
                if len(F)==8:
                    o.write(F[0]+"\t"+F[1]+"\t"+F[2]+"\t"+F[3]+"\t"+F[4]+"\t"+F[5]+"\t"+F[6]+"\t"+F[7]+"\n")
                else:
                    o.write(F[0]+"\t"+F[1]+"\t"+F[2]+"\t"+F[3]+"\t"+F[4]+"\t"+F[5]+"\t"+F[6]+"\t\n")
    if found==0:
        if s_gene!="":
            o.write(s_rsid+"\t"+s_chr+"\t"+s_pos+"\t1\t2\t"+str(s_maf)+"\t"+str(s_dist)+"\t"+s_gene+"\n")
        else:
            o.write(s_rsid+"\t"+s_chr+"\t"+s_pos+"\t1\t2\t"+str(s_maf)+"\t"+str(s_dist)+"\t\n")
