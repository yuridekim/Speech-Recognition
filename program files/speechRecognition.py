# 1. Read in header and store the values into our variables
import hmm

a=dict()
weight=dict()
mean=dict()
var=dict()

for phone in range(0,21):
    ph=hmm.phones[phone][0] #the phone name(sound)
    a[ph]=[]
    weight[ph]=[]
    mean[ph]=[]
    var[ph]=[]

    states=hmm.N_STATE
    if hmm.phones[phone][0]=="sp":
        states=1

    for i in range(0,states+2):
        a[ph].append(hmm.phones[phone][1][i]) #transition probability

    for j in range(0,len(hmm.phones[phone][2])):
        for k in range(hmm.N_PDF):
            weight[ph].append(hmm.phones[phone][2][j][k][0]) #weights values
            mean[ph].append(hmm.phones[phone][2][j][k][1]) #mean values
            var[ph].append(hmm.phones[phone][2][j][k][2]) #variance values


# 2. Read in Dictionary text file
digits = open("dictionary.txt","r")
dictionary={}
for i in digits:
    line=i.split()
    if  line[0]=="zero" and line[2]=="ih": #because there are two zeros
        dictionary["zero1"]=line[1:]
    elif line[0]=="zero" and line[2]=="iy":
        dictionary["zero2"]=line[1:]
    else:
        dictionary[line[0]]=line[1:]
digits.close()

# 3. Construct Word HMMs
a_wordHMM=dict()
mean_wordHMM=dict()
var_wordHMM=dict()
weight_wordHMM=dict()

def join_HMMs(first,second):
        first.append(second)

def update_a(first,second):
    x=1

for i in dictionary.keys(): #i: <s>
    a_wordHMM[i] = []
    mean_wordHMM[i] = []
    var_wordHMM[i] = []
    weight_wordHMM[i] = []
    for phones in range(0,len(dictionary[i])): #dictionary[i][0]: sil
        update_a(a_wordHMM[phones],a[dictionary[i][phones]])
        join_HMMs(mean_wordHMM[i],mean[dictionary[i][phones]])
        join_HMMs(var_wordHMM[i],var[dictionary[i][phones]])
        join_HMMs(weight_wordHMM[i],weight[dictionary[i][phones]])

#print(mean_wordHMM["seven"][2][4])#eight 다음 첫 index: ey [0]은 첫번째 state 첫번째 mean, [2]는 두번째 state 첫번째 mean
#첫 index가 1일 때 "t"를 지칭, [5]는 세번째 state 두번째 mean
#첫 index가 2일 때 "sp"를 지칭 [1]은 첫번째 state 두번째 mean
#print(var_wordHMM["seven"][2][4])
#print(weight_wordHMM["seven"][5]) #seven 중 6번째(index로는 5) phone인 sp의 weight 두개.

# 4. Read Unigram & Bigram Text File
uni = open("unigram.txt","r") #read unigram file
unigram={}
for i in uni:
    line=i.split()
    line[1]=float(line[1])
    unigram[line[0]]=line[1]
uni.close()

bi = open("bigram.txt","r") #read unigram file
bigram={}
for i in bi:
    line=i.split()
    line[2]=float(line[2])
    bigram[line[0],line[1]]=line[2]
bi.close()