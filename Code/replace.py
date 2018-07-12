def cut_n(lis):
    """
    末端の改行文字がめんどくさいため
    リストに含まれる文字の改行文字をすべて取り除く
    """

    for i in range(len(lis)):
        lis[i] = lis[i].replace("\n","")

    return lis

def to_str(path):
    """
    txtファイルを開き
    リストで返す
    """

    f = open(path)
    s = f.readlines()
    f.close()
    return s

def replace_write(path,dic,lis):
    
    f = open(path)
    s = f.read()
    for i in range(len(lis)):
        s = s.replace(lis[i],dic[lis[i]])
    
    f.close()
    path2 = path.replace("1","2")
    f = open(path2,"w")
    f.write(s)
    f.close()


if __name__ == "__main__":
    s1 = to_str("Label1.txt")
    s2 = to_str("Label2.txt")
    s1 = cut_n(s1)
    s2 = cut_n(s2)

    l = len(s1)
    dic = {}
    for i in range(l):
        dic[s1[i]] = s2[i]
    

    seq_in = ["Fasta1.txt","Nexus1.txt","Newick1.txt"]
    for p in seq_in:
        replace_write(p,dic,s1)
