from Bio import SeqIO
from Bio import Entrez
import MySQLdb

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

def get_name(name,feature):
    gene = feature.qualifiers[name][0]
    if name == "note":
        if "intergenic" in feature.qualifiers["note"][0]:
            gene = gene.replace(" region","")
    return gene


def cut_str(moji,lis):
    """
    文字列と単語のリストを与える
    文字列からその単語を取り除く
    """
    for i in lis:
        moji = moji.replace(i,"")
    return moji


def in_db(efetch_handle):
    """
    efetchによってとってきたgbデータから
    配列名ごとに分けてそれぞれfastaファイルに出力する
    """
    connect = MySQLdb.connect(host="localhost", port=3307, db="myseq", user="root", passwd="aaaa", charset="utf8")
    cursor  = connect.cursor()

    cursor.execute("DROP TABLE IF EXISTS `sample`")
    cursor.execute("""CREATE TABLE `sample` (
        `id` varchar(128) NOT NULL,
        `seq` varchar(2048) COLLATE utf8mb4_unicode_ci NOT NULL,
        `gene_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
        `species` varchar(128) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")

    for seq_record in SeqIO.parse(handle,"genbank"):
        seq_id = seq_record.id
        for feature in seq_record.features:
            if "organism" in feature.qualifiers:
                s = feature.qualifiers["organism"][0]
                s = cut_str(s,["Acer "])

            seq_slice = feature.location.extract(seq_record.seq)
            if "gene" in feature.qualifiers:
                gene_name = get_name("gene",feature)
                cursor.execute("INSERT INTO sample VALUES (%s,%s,%s,%s)",(seq_id,seq_slice,gene_name,s))

            elif "product" in feature.qualifiers:
                gene_name = get_name("product",feature)
                cursor.execute("INSERT INTO sample VALUES (%s,%s,%s,%s)",(seq_id,seq_slice,gene_name,s))
              
            elif "note" in feature.qualifiers:
                gene_name = get_name("note",feature)
                cursor.execute("INSERT INTO sample VALUES (%s,%s,%s,%s)",(seq_id,seq_slice,gene_name,s))

    connect.commit()
    return 


if __name__ == "__main__":
    orgn = sys.argv[1]
    t1 = time.time()

    handle = get_nuccore(orgn,proxy=True)
    print("OK")
    in_db(handle)
    print("OK")
    t2 =  time.time()
    print("Elasped time",t2-t1)
     