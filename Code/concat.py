"""
Razaファイルと独自データを結合するスクリプト
"""

from Bio import SeqIO
import sys
from nexus import NexusReader

n = NexusReader()

n.read_file("Razafimandimbison_AppS1.txt")

#rubra_Amami230_trn => 種名_土地番号_遺伝子領域
rps16_dict = {}
trn_dict = {}
rbcL_dict = {}
sample_dict = {}

queue = []
count = 0

for w in ["Psychotria_rbcL.fas","Psychotria_rps16.fas","Psychotria_trn.fas"]:
    count += 1
    for record in SeqIO.parse(w, 'fasta'):

        seq = record.seq 
        id_part = record.id
        id_part = list(map(str,id_part.split("_")))
        
        species_name = id_part.pop(0)
        genome_name1 = id_part.pop(-1)
        sample_name = ''.join(id_part)
    
        seq = record.seq
        #とりあえず動けばいい
        if count == 1:
            sample_dict[sample_name] = species_name+"_"+sample_name
            rbcL_dict[sample_name] = seq
        elif count == 2:
            sample_dict[sample_name] = species_name+"_"+sample_name
            rps16_dict[sample_name] = seq
        else:
            sample_dict[sample_name] = species_name+"_"+sample_name
            trn_dict[sample_name] = seq
            

    
for sample in sample_dict.keys():
        
    if sample in list(rbcL_dict.keys()):
        rbcL = rbcL_dict[sample]
    else:
        rbcL = "-"*1248
    
    if sample in list(rps16_dict.keys()):
        rps16 = rps16_dict[sample]
    else:
        rps16 = "-"*929

    if sample in list(trn_dict.keys()):
        trn = trn_dict[sample]
    else:
        trn = "-"*1707

    
    print(">"+sample_dict[sample])
    print("-"*4104+rbcL+"-"*774+rps16+trn)


for taxon,characters in n.data:
    print(">",taxon)
    print("".join(characters))
