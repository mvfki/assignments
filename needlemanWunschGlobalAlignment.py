'''An implementation of Needleman-Wunsch algorithm, 
not sure if any mistake for now :D'''
# First define the constants
# Scoring matrix, diagonal is for matching
S = [[2, 0, 0, 0],
     [0, 2, 0, 0],
     [0, 0, 2, 0],
     [0, 0, 0, 2]]

# A dictionary for looking up the matrix
ntIdx = {'A': 0, 'T': 1, 'C': 2, 'G': 3}

# Gap penalty
gapP = -1

def printMatrix(m):
    '''
    print the matrix with each line for better visualization when debugging
    '''
    for i in range(len(m)):
        print(i, m[i])

class align():
    """Needleman-Wunsch algorithm"""
    def __init__(self, seq1, seq2, S = S, gapP = gapP):
        assert len(seq1) > 0, 'Input sequence is empty'
        assert len(seq2) > 0, 'Input sequence is empty'
        self.seq1 = seq1.upper()
        self.seq2 = seq2.upper()
        self.S = S
        self.gapP = gapP
        self.aln = 'NOT ALIGNED YET'
        self.score = None
        self.run()
    
    def run(self):
        '''Run all the processes'''
        self.initializeMatrix()
        self.DP()
        self.traceback()

    def initializeMatrix(self):
        '''Initialize the scoring matrix and traceback matrix'''
        # First inititalize the scoring matrix, so that it has len(seq1) rows 
        # and len(seq2) columns. 
        self.M = [[0 for j in range(len(self.seq2) + 1)] 
                    for i in range(len(self.seq1) + 1)]
        
        # And a matrix for recording the trace back path, with the same size. 
        self.TB = [[0 for j in range(len(self.seq2) + 1)] 
                    for i in range(len(self.seq1) + 1)]

        # Initialize the gap scores of the first row and the first column.
        for j in range(1, len(self.seq2) + 1):
            self.M[0][j] = self.M[0][j - 1] + self.gapP
        for i in range(1, len(self.seq1) + 1):
            self.M[i][0] = self.M[i - 1][0] + self.gapP

        for j in range(1, len(self.seq2) + 1):
            self.TB[0][j] = 1 # for gap in seq1
        for i in range(1, len(self.seq1) + 1):
            self.TB[i][0] = 2 # for gap in seq2

    def DP(self):
        '''The DP step for filling in the matrix'''
        for i in range(1, len(self.seq1) + 1):
            for j in range(1, len(self.seq2) + 1):
                # Note that here i - 1 is the i'th index in self.seq1
                # get the scores from three directions
                g1 = self.M[i][j - 1] + gapP
                g2 = self.M[i - 1][j] + gapP
                m = self.M[i - 1][j - 1] + \
                S[ntIdx[self.seq1[i - 1]]][ntIdx[self.seq2[j - 1]]]

                if m == max(g1, g2, m):
                    self.M[i][j] = m
                    self.TB[i][j] = 3 # for matching
                elif g1 == max(g1, g2, m):
                    self.M[i][j] = g1
                    self.TB[i][j] = 1 # for gap in seq1
                elif g2 == max(g1, g2, m):
                    self.M[i][j] = g2
                    self.TB[i][j] = 2 # for gap in seq2

        self.score = self.M[i][j]
        printMatrix(self.M)

    def traceback(self):
        '''The traceback step'''
        Pos = (len(self.seq1), len(self.seq2))
        Dir = self.TB[Pos[0]][Pos[1]]
        seq1out = []
        seq2out = []
        matching = []
        while Dir != 0:

            if Dir == 3 and self.seq1[Pos[0] - 1] == self.seq2[Pos[1] - 1]:
                matching.insert(0, '|')
            else:
                matching.insert(0, ' ')

            if Dir == 3:
                seq1out.insert(0, self.seq1[Pos[0] - 1])
                seq2out.insert(0, self.seq2[Pos[1] - 1])
                Pos = (Pos[0] - 1, Pos[1] - 1)
            elif Dir == 1:
                seq1out.insert(0, '-')
                seq2out.insert(0, self.seq2[Pos[1] - 1])
                Pos = (Pos[0], Pos[1] - 1)
            elif Dir == 2:
                seq1out.insert(0, self.seq1[Pos[0] - 1])
                seq2out.insert(0, '-')
                Pos = (Pos[0] - 1, Pos[1])
            
            Dir = self.TB[Pos[0]][Pos[1]]

        assert len(seq1out) == len(seq2out)
        seq1out = ''.join(seq1out)
        seq2out = ''.join(seq2out)
        matching = ''.join(matching)
        self.aln = seq1out + '\n' + matching + '\n' + seq2out

    def __str__(self):
        string = 'original input sequences:\nseq1 - %s\nseq2 - %s\
        \nFinal alignment: \n%s\nAlignment score: \n%d'\
        % (self.seq1, self.seq2, self.aln, self.score)
        return string

def main():
    seq1 = 'caggt'
    seq2 = 'gatggct'

    a = align(seq1, seq2)
    print(a)

if __name__ == '__main__':
    main()
