'''http://rosalind.info/problems/trie/'''

class Trie(object):

    def __init__(self, seqCollection = None):
        '''Initialize a Trie, can be empty.'''
        self.allSeqs = seqCollection
        self.trie = {(1, 'Root'): set()}
        self.done = False
        self.autoIncrement = 1

    def buildTrie(self, seqCollection = None):
        '''Build the trie with given list of sequences. Can be run multiple times.'''
        if self.allSeqs == None:
            self.allSeqs = seqCollection
        else:
            if seqCollection != None:
                self.allSeqs.extend(seqCollection)

        assert self.allSeqs != None, 'Please give a list of strings'

        for seq in self.allSeqs:
            self._mergeOneSeq(seq)

        self.done = True

    def _mergeOneSeq(self, seq):
        currentNode = (1, 'Root')
        for n in seq:
            foundMatch = False
            nodeID = None

            for follower in self.trie[currentNode]:
                if follower[1] == n:
                    foundMatch = True
                    nodeID = follower[0]
                    currentNode = follower
                    break

            if not foundMatch:
                self.autoIncrement += 1
                self.trie[currentNode].add((self.autoIncrement, n))
                self.trie[(self.autoIncrement, n)] = set()
                currentNode = (self.autoIncrement, n)

    def rosalindOutput(self):
        assert self.done, 'Please run all calculation first.'
        for node, followers in self.trie.items():
            for f in followers:
                print(node[0], f[0], f[1])


def main():
    seqText = open('rosalind_trie.txt', 'r').read()
    seqCollection = seqText.splitlines()
    trie = Trie()
    trie.buildTrie(seqCollection)
    '''
    # Test for run Trie.buildTrie() multiple times
    a = ['QQQB', 'QQQA']
    trie.buildTrie(a)
    '''
    trie.rosalindOutput()

if __name__ == '__main__':
    main()
