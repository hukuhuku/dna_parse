from Bio import SeqIO
from Bio import Entrez

from collections import defaultdict
import pandas as pd
import sys
import urllib

import time



def get_nuccore(orgn,r=100000,proxy = False):
    """
    種名,属名などを渡し,それに一致する全ゲノムデータを取得する
    """
    
    if proxy:
        username = input("Please Enter username: ")
        password = input("Please Enter password: ")


        proxy = urllib.request.ProxyHandler({"http": "http://"+username+"::"+password+"@cproxy.okinawa-ct.ac.jp:8080",
               "https":"https//"+username+"::"+password+"@cproxy.okinawa-ct.ac.jp:8080"})
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)


    #ncbiに連絡先としてメールアドレスを記述する必要がある。
    Entrez.email = "hukuhuku11111arm52@gmail.com"

    handle = Entrez.esearch(db="nuccore",term =str(orgn+"[Orgn]"),retmax = r)
    record = Entrez.read(handle)
    gi_list = record["IdList"]
    gi_str = ",".join(gi_list)


    handle = Entrez.efetch(db="nuccore", rettype="gb", retmode="gb", id=gi_str,retmax = r)

    return handle




def in_dic(name,feature,seq_slice,dic,s):
    
    if name != "note":
        gene = feature.qualifiers[name][0]
        dic[gene][s] = str(seq_slice)
            
    else:
        if "intergenic" in feature.qualifiers["note"][0]:
            gene = feature.qualifiers["note"][0]
            gene = gene.replace(" region","")
            """
            if len(gene.split(" ")) != 3:
                #hoge-hoge intergenic spacer とかの記述以外は整形して格納したい        
                for j in feature.qualifiers:
                    if j in s:
                        gene = cut_str(gene,[j,feature.qualifiers[j][0]])
                    else:
                        gene = cut_str(gene,list(feature.qualifiers[j][0].split(" ")))
                print(gene) 
            """
            dic[gene][s] = str(seq_slice)
        
    return dic



def cut_str(moji,lis):
    """
    文字列と単語のリストを与える
    文字列からその単語を取り除く
    """
    for i in lis:
        moji = moji.replace(i,"")
    return moji


def output_fasta(efetch_handle):
    """
    efetchによってとってきたgbデータから
    配列名ごとに分けてそれぞれfastaファイルに出力する
    """
    dic = defaultdict(dict)

    for seq_record in SeqIO.parse(handle,"genbank"):
        for feature in seq_record.features:

            if "organism" in feature.qualifiers:
                s = feature.qualifiers["organism"][0]
                s = cut_str(s,["Acer "])
            seq_slice = feature.location.extract(seq_record.seq)
            if "gene" in feature.qualifiers:
                dic = in_dic("gene",feature,seq_slice,dic,s)
             
            elif "product" in feature.qualifiers:
                dic= in_dic("product",feature,seq_slice,dic,s)
              
            elif "note" in feature.qualifiers:
                dic = in_dic("note",feature,seq_slice,dic,s) 

    for k, v in dic.items(): 
        name = cut_str(k,["/",";",","])
        name = name.replace(" ","_")
        file = open("output/"+str(name+".fasta"),"w")
    
        for m,n in v.items():
            file.write(">"+m+"\n")
            file.write(n+"\n")
        file.close()
    return dic

def output_csv(dic):
    """
    dic : dic["gene_name"] = {"species1":"AAAATTTGGG","species2":"TTTGGGTTT"}みたいな感じで配列ごとに種のDNAが入っている辞書形式データ
    dicからそれぞれどの種でどの遺伝子が存在していたかを表形式で出力
    """

    #dicに含まれるすべての種,配列名を取得
    species = []
    gene_name = []
    for k,v in dic.items():
        if k not in gene_name:
            gene_name.append(k)
        for m,n in v.items():
            if m not in species:
                 species.append(m)
    
    print("OK")
        
    df = pd.DataFrame(species)
    df = df.set_index(0)
    

    for f in gene_name:
        df[f] = 0
   
        for k,v in dic.items():
            df[k] = 0
            for m,n in v.items():
                df[k][m] = 1

    df.to_csv("test.csv")


if __name__ == "__main__":
    orgn = sys.argv[1]
    t1 = time.time()

    handle = get_nuccore(orgn,proxy=True)
    print("OK")
    dic = output_fasta(handle)
    print("OK")
    output_csv(dic)
    t2 =  time.time()
     