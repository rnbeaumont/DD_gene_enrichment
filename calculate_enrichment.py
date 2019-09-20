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
    nsnp=0
    fhash={}
    with open(snplist,"r") as f:
        for line in f:
            F=line.rstrip().split()
            G=F[-1].split(",")
            match=0
            for gene in G:
                if gene in ghash:
                    match=1
                    if gene in fhash:
                        fhash[gene]+=1
                    else:
                        fhash[gene]=1
            if match==1:
                nsnp+=1
    ngene=len(fhash)
    with open(samplenum,"r") as f:
        count=0
        countsnp=0
        F=f.readlines()
        for line in F:
            G=line.rstrip().split()
            if int(G[0])>=ngene:
                count+=1
            if int(G[1])>=nsnp:
                countsnp+=1
    p=float(count)/len(F)
    psnp=float(countsnp)/len(F)
    print "In "+snplist+" there are "+str(nsnp)+" SNPs with genes in the gene list. The P value for enrichment is p="+str(psnp)
    print "In "+snplist+" there are "+str(ngene)+" genes in the gene list. The P value for enrichment is p="+str(p)+"\n"
    print "Gene in "+snplist+" also in "+glist+":"
    for gene in fhash:
        print gene+"\t"+str(fhash[gene])
