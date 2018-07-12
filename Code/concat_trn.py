from nexus import NexusReader
from Bio import SeqIO
import sys

n = NexusReader()
n.read_file("Razafimandimbison_AppS1.txt")

for taxon,characters in n.data:
    print(">",taxon)
    print("".join(characters)[7865:10693])

fasta_in = "Psychotria_trn.fas" #fastaファイルを読みこみ

for record in SeqIO.parse(fasta_in, 'fasta'):
    id_part = record.id
    desc_part = record.description
    seq = record.seq

    print('>', id_part)
    print(seq)
