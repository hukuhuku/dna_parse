"""
fastaファイルのDNAの方向を揃えるスクリプト
先頭のDNAを基準にし同じ向きになるように揃える
"""
import sys
from Bio import SeqIO
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import sys 

fasta_in = sys.argv[1] #fastaファイルを読みこみ
count = 0

for record in SeqIO.parse(fasta_in, 'fasta'):
    desc = record.description
    seq = record.seq
    
    if count == 0:
        hoge = seq
        print(desc)
        print(hoge)
    else:
        a = (pairwise2.align.globalms(seq, hoge, 2, -1, -0.5, -0.1)[0][2])
        b = (pairwise2.align.globalms(seq[::-1], hoge, 2, -1, -0.5, -0.1)[0][2])
        print(">",desc)
        if a < b:
            print(seq[::-1])
        else:
            print(seq)

        
    count += 1