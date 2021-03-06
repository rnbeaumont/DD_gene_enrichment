#!/usr/bin/python
import getopt,sys,random

def readargs():
    genefile=''
    snpprefix=''
    outputfile=''
    nfiles=0
    niter=0
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hg:m:o:n:i:",["genelist=","matchprefix=","out=","nsnp=","niter="])
    except getopt.GetoptError:
        print "sample_matching_snps.py -g <gene list> -m <prefix of files containing matching SNPs> -o <output file> -n <number of SNPs> -i <number of random samples>"
        sys.exit(2)
    for opt,arg in opts:
        if opt=='-h':
            print "sample_matching_snps.py -g <gene list> -m <prefix of files containing matching SNPs> -o <output file> -n <number of SNPs> -i <number of random samples>"
            sys.exit()
        elif opt in ("-g","--genelist"):
            genefile=arg
        elif opt in ("-m","--matchprefix"):
            snpprefix=arg
        elif opt in ("-o","--out"):
            outputfile=arg
        elif opt in ("-n","--nsnp"):
            nfiles=int(arg)
        elif opt in ("-i","--niter"):
            niter=int(arg)
    return genefile,snpprefix,outputfile,nfiles,niter


if __name__ == "__main__":
    genefile,snpprefix,outputfile,nfiles,niter=readargs()
    if genefile=='' or snpprefix=='' or outputfile=='' or nfiles==0 or niter==0:
        print "sample_matching_snps.py -g <gene list> -m <prefix of files containing matching SNPs> -o <output file> -n <number of SNPs> -i <number of random samples>"
        sys.exit(3)
    ghash={}
    with open(genefile,"r") as f:
        for gene in f:
            G=gene.rstrip().split()
            ghash[G[0]]=1
    nline=[0]
    for i in range(1,nfiles+1):
        with open(snpprefix+str(i),"r") as f:
            F=f.readlines()
            nline.append(len(F))
    o=open(outputfile,"w")
    for k in range(niter):	# number of iterations
        ngene=0
        nsnp=0
        for i in range(1,nfiles+1):	# loop over the files
            fhash={}
            with open(snpprefix+str(i),"r") as f:
                for j in range(random.randint(1,nline[i]-1)):
                    f.readline()
                F=f.readline().rstrip().split()
                if len(F)==8:
                    G=F[-1].split(",")
                    match=0
                    for gene in G:
                        fhash[gene]=1
                        if gene in ghash:
                            match=1
                            if ghash[gene]==1:
                                ngene+=1
                            ghash[gene]+=1
                    if match==1:
                        nsnp+=1
        o.write(str(ngene)+"\t"+str(nsnp)+"\n")
    o.close()
