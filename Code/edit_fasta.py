from Bio import SeqIO
import sys
import re

def match_extraction(description,s_match,pre=1):
    """
    description :str
    s_match :str
    pre : 1 or 0 
    -------------
    descriptionの文字列内にs_matchがあればマッチした部分の前後を取り出す
    """

    try:
        r = re.search(s_match,description)
        if pre == 1:
            return r.string[:r.start()]
        else:
            return r.string[r.end():]
    except:
        return description

def main():
    """
    fasta_inに渡したファイルを何らかの処理をしてoutputのファイルに渡す
    """
    
    fasta_in = sys.argv[1]
    fasta_out = "../output/result.fasta"
    match_str = ""

    file = open(fasta_out,"w")
    for record in SeqIO.parse(fasta_in, 'fasta'):
        seq_part = record.seq 
        desc_part = record.description
        
        desc_part = match_extraction(desc_part,match_str)

        file.write(">"+desc_part+"\n")
        file.write(str(seq_part)+"\n")
    file.close()

if __name__ == "__main__":
    main()
