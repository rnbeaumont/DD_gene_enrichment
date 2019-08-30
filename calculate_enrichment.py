#!/usr/bin/python
import getopt,sys

def readargs():
    glist=''
    snplist=''
    samplenum=''
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hg:s:r:",["genelist=","snplist=","randomlist="])
    except getopt.getoptError:
        print "calculate_enrichment.py -g <list of genes> -s <SNP list> -r <randomly sampled gene enrichment>"
        sys.exit(2)
    for opt,arg in opts:
        if opt=='-h':
            print "calculate_enrichment.py -g <list of genes> -s <SNP list> -r <randomly sampled gene enrichment>"
            sys.exit()
        elif opt in ("-g","--genelist"):
            glist=arg
        elif opt in ("-s","--snplist"):
            snplist=arg
        elif opt in ("-r","--randomlist"):
            samplenum=arg
    return glist,snplist,samplenum

if __name__=="__main__":
    glist,snplist,samplenum=readargs()
    if glist=='' or snplist=='' or samplenum=='':
        print "calculate_enrichment.py -g <list of genes> -s <SNP list> -r <randomly sampled gene enrichment>"
        sys.exit(2)
    ghash={}
    with open(glist,"r") as f:
        for gene in f:
            G=gene.rstrip().split()
            ghash[G[0]]=1
    ngene=0
    fhash={}
    with open(snplist,"r") as f:
        for line in f:
            F=line.rstrip().split()
            G=F[-1].split(",")
            for gene in G:
                if gene in ghash:
                    ngene+=1
                    if gene in fhash:
                        fhash[gene]+=1
                    else:
                        fhash[gene]=1
    with open(samplenum,"r") as f:
        count=0
        F=f.readlines()
        for line in F:
            if int(line)>=ngene:
                count+=1
    p=float(count)/len(F)
    print "P value for enrichment of genes in "+snplist+" is p="+str(p)+"\n"
    print "Gene in "+snplist+" also in "+glist+":"
    for gene in fhash:
        print gene+"\t"+str(fhash[gene])
