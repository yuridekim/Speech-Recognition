import math
import os

# 1. Read in header and store the values into our variables
import hmm

MUL_BIGRAM=0.01
LOGZERO = -100000000.0

def exp(x):
    if x == LOGZERO:
        return 0
    else:
        return math.exp(x)


def log(x):
    if x == 0:
        return LOGZERO
    elif x > 0:
        return math.log(x)


def logproduct(x, y):
    if x == LOGZERO or y == LOGZERO:
        return LOGZERO
    else:
        return x + y


def logsum(x, y):
    if x == LOGZERO or y == LOGZERO:
        if x == LOGZERO:
            return y
        else:
            return x
    else:
        if x > y:
            return x + log(1 + math.exp(y - x))
        else:
            return y + log(1 + math.exp(x - y))

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

# join the means/variables/weights for the joined phones
def join_HMMs(first,second):
        first.append(second)

# calculate and update the transition probability
def update_a(first,second):
    result=[]
    firstLen=len(first)
    secondLen=len(second)
    if(firstLen==0):
        for i in range(0,len(second)):
            result=second
    else:
        newALen=firstLen+secondLen-2
        for row in range(0,newALen):
            temp=[]
            for col in range(0,newALen):
                if row<firstLen-1 and col<firstLen-1:
                    temp.append(first[row][col])
                elif row==firstLen-2:
                    temp.append(first[firstLen-2][firstLen-1]*second[0][col-firstLen+2])
                elif row>=firstLen-2 and col>=firstLen-1:
                    temp.append(second[row-firstLen+2][col-firstLen+2])
                else:
                    temp.append(0)
            result.append(temp)
    return result

for i in dictionary.keys(): #i: <s>
    a_wordHMM[i] = []
    mean_wordHMM[i] = []
    var_wordHMM[i] = []
    weight_wordHMM[i] = []
    for phones in range(0,len(dictionary[i])): #dictionary[i][0]: sil
        a_wordHMM[i]=update_a(a_wordHMM[i],a[dictionary[i][phones]])
        join_HMMs(mean_wordHMM[i],mean[dictionary[i][phones]])
        join_HMMs(var_wordHMM[i],var[dictionary[i][phones]])
        join_HMMs(weight_wordHMM[i],weight[dictionary[i][phones]])

# 4. Read Unigram & Bigram Text File
uni = open("unigram.txt","r") #read unigram file
unigram={}
for i in uni:
    line=i.split()
    line[1]=float(line[1])
    unigram[line[0]]=line[1]
uni.close()

#zero1와 zero2 처리해주기
unigram["zero1"]=unigram["zero"]
unigram["zero2"]=unigram["zero"]

bi = open("bigram.txt","r") #read unigram file
bigram={}
for i in bi:
    line=i.split()
    line[2]=float(line[2])
    bigram[line[0],line[1]]=line[2]
bi.close()
bigram["zero","oh"]=0.000
bigram["oh","zero"]=0.000
bigram["<s>","<s>"]=0.000
for i in dictionary.keys():
    if i=="zero1" or i=="zero2":
        continue
    bigram["zero1",i]=bigram["zero",i]
    bigram["zero2",i] = bigram["zero",i]
    bigram[i,"zero1"]=bigram[i,"zero"]
    bigram[i,"zero2"] = bigram[i,"zero"]
bigram["zero1","zero2"]=bigram["zero","zero"]
bigram["zero1","zero1"]=bigram["zero","zero"]
bigram["zero2","zero1"]=bigram["zero","zero"]
bigram["zero2","zero2"]=bigram["zero","zero"]

#5. Construct a universal utterance
a_univUtterance=dict()
mean_univUtterance=dict()
var_univUtterance=dict()
weight_univUtterance=dict()
wordIndexes=dict()

totalStates=1
for i in dictionary.keys():  # i: <s>
    wordIndexes[i]=[]
    wordIndexes[i].append(totalStates)
    mean_univUtterance[i] = []
    var_univUtterance[i] = []
    weight_univUtterance[i] = []
    totalStates+=(len(a_wordHMM[i])-2)
    wordIndexes[i].append(totalStates-1)
    a_univUtterance = update_a(a_univUtterance, a_wordHMM[i])
    join_HMMs(mean_univUtterance[i], mean_wordHMM[i])
    join_HMMs(var_univUtterance[i], var_wordHMM[i])
    join_HMMs(weight_univUtterance[i], weight_wordHMM[i])

#뒤돌아가는 경로 만들기
for fromWord in dictionary.keys():
    rowStart=wordIndexes[fromWord][0]
    rowEnd=wordIndexes[fromWord][1]

    for toWord in dictionary.keys():
        colStart=wordIndexes[toWord][0]
        colEnd=wordIndexes[toWord][1]
        lengthOfFromWord=len(a_wordHMM[fromWord])

        #Transmission probability: before sp to next word
        a_univUtterance[rowEnd - 1][colStart] = bigram[fromWord, toWord] * a_wordHMM[fromWord][lengthOfFromWord - 3][
            lengthOfFromWord-1]*MUL_BIGRAM
        #Transmission probability: from sp to next word
        a_univUtterance[rowEnd][colStart] = bigram[fromWord, toWord] * a_wordHMM[fromWord][lengthOfFromWord - 2][
            lengthOfFromWord-1]*MUL_BIGRAM

for fromWord in dictionary.keys():
    lengthOfFromWord = len(a_wordHMM[fromWord])
    rowStart = wordIndexes[fromWord][0]
    rowEnd = wordIndexes[fromWord][1]

    a_univUtterance[rowEnd - 1][totalStates-1] = a_wordHMM[fromWord][lengthOfFromWord - 2][lengthOfFromWord - 1]
    a_univUtterance[rowEnd][totalStates-1] = a_wordHMM[fromWord][lengthOfFromWord - 1][lengthOfFromWord - 1]

#unigram 행렬 첫 행에 넣어주기
for i in dictionary.keys():
     start=wordIndexes[i][0]
     end=wordIndexes[i][1]
     a_univUtterance[0][start]=unigram[i]

print("done")

#6. Implement the Viterbi Algorithm for the universal utterance HMM
#calculate the observation probability
resultValues = dict()
numState=1
for word in dictionary.keys():  # <s>
    for ph in range(len(dictionary[word])):
        nstate=3
        if dictionary[word][ph]=="sp":
            nstate=1
        for state in range(0,nstate):  # 1번째 state
            for pdf in range(0, 2):  # 1번째 pdf
                resultValues[numState,pdf+1] = 1.0
                for var in var_univUtterance[word][0][ph][2*state+pdf]:
                    resultValues[numState,pdf+1] *= math.sqrt(var)
                resultValues[numState,pdf+1]= 1.0 / math.sqrt(2 * math.pi) * resultValues[numState,pdf+1]
            numState+=1

def b(state, x):
    result = {}
    if state==0:
        output = LOGZERO
        for x in result:
            output = logsum(output, result[x])
        return output

    for i in dictionary.keys():
        if state >= wordIndexes[i][0] and state<=wordIndexes[i][1]:
            w=i #word
            ph=int((state-wordIndexes[i][0])/3+1) #0,1,2 는 1번째 phone
            st=(state-wordIndexes[i][0])%3+1
        else:
            continue

    for b in range (1,3):
        result[b] = 0.0
        for index in range(hmm.N_DIMENSION):  # iterate i
            result[b] += math.pow(x[index] - mean_univUtterance[w][0][ph-1][2*st+b-3][index], 2) / var_univUtterance[w][0][ph-1][2*st+b-3][index]
        result[b] = log(weight_univUtterance[w][0][ph-1][2*st+b-3] * resultValues[state,b] * exp((-1.0 / 2.0) * result[b]))
    output = LOGZERO
    for x in result:
        output = logsum(output, result[x])
    return output

# find the path sequence with viterbi
def viterbi(hmm, x):
    delta = {}
    psi = {}
    for j in range(totalStates):
        delta[1, j] = logproduct(log(a_univUtterance[0][j]), b(j, x[1]))
        psi[1, j] = 0
    for t in range(2, len(x) + 1):
        for j in range(totalStates):
            delta[t, j] = LOGZERO
            psi[t, j] = 0
            for i in range(totalStates):
                if delta[t, j] < logproduct(delta[t - 1, i], log(a_univUtterance[i][j])):
                    delta[t, j] = logproduct(delta[t - 1, i], log(a_univUtterance[i][j]))
                    psi[t, j] = i
            if j == totalStates - 1:
                delta[t, j] = LOGZERO
            else:
                delta[t, j] = logproduct(delta[t, j], b(j, x[t]))

    delta[len(x), totalStates - 1] = LOGZERO
    for j in range(totalStates):
        if delta[len(x), totalStates - 1] < logproduct(delta[len(x), j], log(a_univUtterance[j][totalStates - 1])):
            delta[len(x), totalStates - 1] = logproduct(delta[len(x), j], log(a_univUtterance[j][totalStates - 1]))
            psi[len(x), totalStates - 1] = j

    q = [0 for i in range(len(x))]
    q[len(x) - 1] = psi[len(x), totalStates - 1]
    for t in range(len(x) - 2, -1, -1):
        q[t] = psi[t + 1, q[t + 1]]
    return q

# 7. For each test data file, run the Viterbi algorithm and find the most likely sequence
answer_word = []
result = open("recognized.txt", "w")
result.write("#!MLF!#\n")
cnt = 0
for root, dirs, files in os.walk("tst", topdown=False):
    root = root.replace("\\", "/")
    for name in files:
        result.write("\"" + root + "/" + name[0:-3] + "rec\"\n")
        test_file = open(os.path.join(root, name))
        length = int(test_file.readline().split()[0]);
        x = {}
        for i in range(1, length + 1):
            x[i] = list(map(float, test_file.readline().split()))
        cnt += 1
        answer = viterbi(hmm, x)

        # Convert our sequences to word digits
        answer_word = []
        cur_word = ""
        for i in range(len(answer) - 1):
            for word in wordIndexes:
                (a, b) = wordIndexes[word]
                if answer[i] <= b and answer[i] >= a + 3 and cur_word != word:
                    cur_word = word

                    if cur_word == "zero2" or cur_word=="zero1":
                        answer_word.append("zero")
                    else:
                        answer_word.append(cur_word)
                    # write words to file
        for i in range(len(answer_word)):
            result.write(answer_word[i])
            result.write("\n")
        result.write(".\n")