#!/usr/bin/python
import getopt, sys

def readargs(inputfile,outputfile,glist,wsize):
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:g:w:",["ifile=","ofile=","glist=","window="])
    except getopt.GetoptError:
        print "annotate_snp_list.py -i <inputfile> -o <outputfile> -g <genelsit (optional)> -w <window_size (optional - set to 0 or leave out for nerest gene)> 1"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' :
            print "annotate_snp_list.py -i <inputfile> -o <outputfile> -g <genelsit (optional)> -w <window_size (optional - set to 0 or leave out for nerest gene)> 2"
            sys.exit()
        elif opt in ("-i","--ifile"):
            inputfile=arg
        elif opt in ("-o","--ofile"):
            outputfile=arg
        elif opt in ("-g","--glist"):
            glist=arg
        elif opt in ("-w","--window"):
            wsize=int(arg)
    return inputfile,outputfile,glist,wsize

def getdist(f,glist,o):
    for line in f:
        F=line.rstrip().split()
        dist=9999999999;
        with open(glist,"r") as g:
            g.readline()
            for gene in g:
                G=gene.rstrip().split()
                if F[1]==G[1]:
                    up=int(G[2])-int(F[2])
                    down=int(F[2])-int(G[3])
                    if up>0 and down>0:
                        if min(up,down)<dist:
                            dist=min(up,down)
                            near=G[0]
                    elif up<=0 and down<=0:
                        if dist==0:
                            near+=","+G[0]
                        else:
                            dist=0
                            near=G[0]
                    elif up>0 and down<0:
                        if up<dist:
                            dist=up
                            near=G[0]
                    elif up<0 and down>0:
                        if down<dist:
                            dist=down
                            near=G[0]
                    else:
                        print("ERROR\n")
        o.write(F[0]+"\t"+F[1]+"\t"+F[2]+"\t"+F[3]+"\t"+F[4]+"\t"+F[5]+"\t"+str(dist)+"\t"+near+"\n")

def getnumber(f,glist,wsize,o):
    for line in f:
        F=line.rstrip().split()
        num=0;
        with open(glist,"r") as g:
            near=''
            g.readline()
            for gene in g:
                G=gene.rstrip().split()
                if F[1]==G[1]:
                    if (int(G[2])-(int(F[2])-wsize))>0 and (int(F[2])+wsize)-int(G[3])>0:
                        if num==0:
                            near=G[0]
                        else:
                            near+=","+G[0]
                        num+=1
                    elif ((int(F[2])-wsize)-int(G[2]))>0 and int(G[3])-(int(F[2])-wsize)>0:
                        if num==0:
                            near=G[0]
                        else:
                            near+=","+G[0]
                        num+=1
                    elif int(G[3])-(int(F[2])+wsize)>0 and (int(F[2])+wsize)-int(G[2])>0:
                        if num==0:
                            near=G[0]
                        else:
                            near+=","+G[0]
                        num+=1
        o.write(F[0]+"\t"+F[1]+"\t"+F[2]+"\t"+F[3]+"\t"+F[4]+"\t"+F[5]+"\t"+str(num)+"\t"+near+"\n")

if __name__ == "__main__":
    inputfile=''
    outputfile=''
    glist="gene_list"
    wsize=0
    inputfile,outputfile,glist,wsize=readargs(inputfile,outputfile,glist,wsize)
    if inputfile=='' or outputfile=='':
        print "annotate_snp_list.py -i <inputfile> -o <outputfile> -g <genelsit (optional)> -w <window_size (optional - set to 0 or leave out for nerest gene)>"
        sys.exit(3)
    o=open(outputfile,"w")
    with open(inputfile,"r") as f:
        line=f.readline()
        line=line.rstrip()
        if wsize==0:
            o.write(line+"\tdistance_to_gene\tgene\n")
            getdist(f,glist,o)
        else:
            o.write(line+"\tnumber_genes\tgenes\n")
            getnumber(f,glist,wsize,o)
    o.close()
