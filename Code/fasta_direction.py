
import sys
from Bio import SeqIO
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import sys 



def allign_direction(fasta_in):
    """
    fastaファイルのDNAの方向を揃えるスクリプト  
    先頭のDNAを基準にし同じ向きになるように揃える
    """
    count = 0
    name = fasta_in.replace(".fasta","")
    file = open(name+"_allign.fasta","w")
    for record in SeqIO.parse(fasta_in, 'fasta'):
        desc = record.description
        seq = record.seq
    
        if count == 0:
            hoge = seq
            file.write(">",desc)
            file.write(hoge)
        else:
            a = (pairwise2.align.globalms(seq, hoge, 2, -1, -0.5, -0.1)[0][2])
            b = (pairwise2.align.globalms(seq[::-1], hoge, 2, -1, -0.5, -0.1)[0][2])
            file.write(">",desc)
            if a < b:
                file.write(seq[::-1])
            else:
                file.write(seq)
    count += 1
    file.close()
    return

if __name__ == "__main__":
    fasta_in = sys.argv[1] #fastaファイルを読みこみ
    allign_direction(fasta_in)
