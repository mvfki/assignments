'''An implementation of longest-in/decreasing-subsequence, can work for 
rosalind problem. Test input and output can be found at 'examples'.'''
#a = [int(i) for i in open('rosalind_lgis.txt', 'r').read().split('\n')[1].split()]
a = [1, 10, 2, 3, 9, 8, 7, 6, 11]
def printMatrix(m):
    for i in m:
        print(i)
def printIntList(l):
    l = [str(i) for i in l]
    print(' '.join(l))

def getLDS(a):
    '''Initialize the matrix for recording the steps taken. Probably a DP method'''
    stepMatrix = [[0 for i in range(len(a))] for j in range(len(a))]
    TB = {}
    maxStepDic = {i: 0 for i in a}

    lastStep = None
    maxStep = 0

    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                if maxStepDic[a[i]] + 1 > maxStepDic[a[j]]:
                    stepMatrix[i][j] = maxStepDic[a[i]] + 1
                    maxStepDic[a[j]] += 1
                    TB[a[j]] = a[i]
                    if maxStepDic[a[j]] > maxStep:
                        maxStep = maxStepDic[a[j]]
                        lastStep = a[j]

    # From TB, get the path
    path = [lastStep]
    while True:
        try:
            path.insert(0, TB[lastStep])
            lastStep = TB[lastStep]
        except KeyError:
            break
    return path

def getLIS(a):
    '''Initialize the matrix for recording the steps taken. Probably a DP method'''
    stepMatrix = [[0 for i in range(len(a))] for j in range(len(a))]
    TB = {}
    maxStepDic = {i: 0 for i in a}

    lastStep = None
    maxStep = 0

    for i in range(len(a)):
        for j in range(i+1, len(a)):
            if a[i] < a[j]:
                if maxStepDic[a[i]] + 1 > maxStepDic[a[j]]:
                    stepMatrix[i][j] = maxStepDic[a[i]] + 1
                    maxStepDic[a[j]] += 1
                    TB[a[j]] = a[i]
                    if maxStepDic[a[j]] > maxStep:
                        maxStep = maxStepDic[a[j]]
                        lastStep = a[j]

    # From TB, get the path
    path = [lastStep]
    while True:
        try:
            path.insert(0, TB[lastStep])
            lastStep = TB[lastStep]
        except KeyError:
            break
    return path

LIS = getLIS(a)
LDS = getLDS(a)
print('Longest Increasing Subsequence:')
printIntList(LIS)
print('Longest Decreasing Subsequence:')
printIntList(LDS)
