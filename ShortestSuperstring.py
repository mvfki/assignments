'''A solution to Rosalind problem: Genome Assembly as Shortest Superstring
Mainly use k-mer to find corresponding overlapping sequence pairs and then fix
the overlap relation ship to build the assembly. This solution is based on the 
assumptions that there is no error in the sequences, that the overlapping 
length would always be more than half of each sequence that is in a pair, and 
that there is no reverse complement alignment. Therefore, it is not useful in 
practice at all :D'''

from collections import defaultdict
from Bio import SeqIO

class Assemble(object):
    """Very naive assmbler, with the assumption stated above. Note that when
    the variable name says 'seq' it means the sequence with nucleotides, when
    it says node, it means the 0-based index in the sequence collection. """
    def __init__(self, seqCollection):
        self.seqCollection = seqCollection
        self.asm = ''
        self.run()

    def run(self):
        self.buildIndex()
        self.getGraph()
        self.concatenate()

    def buildIndex(self):
        '''
        Build the k-mer index of the prefix and suffix for all sequences
        '''
        # Because the overlapping length would always be more than half of 
        # each sequence that is in a pair. So here k = min([half_sequence])
        k = round(min([len(s) / 2 for s in self.seqCollection]))
        self.kmer2seq = defaultdict(set)
        self.seq2kmer = defaultdict(set)
        for i in range(len(self.seqCollection)):
            for pos in range(len(self.seqCollection[i]) - k + 1):
                k_mer = self.seqCollection[i][pos:pos + k]
                assert len(k_mer) == k
                self.kmer2seq[k_mer].add((i, pos))
                self.seq2kmer[i].add((k_mer, pos))
    
    def getCandidates(self, node):
        kmers = self.seq2kmer[node]
        candidates = set()
        for kmer, pos in kmers:
            for node2, pos in self.kmer2seq[kmer]:
                candidates.add(node2)
        assert len(candidates) <= 3 and len(candidates) >= 2
        return candidates.difference({node})

    def getGraph(self):
        '''From the precomputed index, extend them to build the correct 
        odering of each sequence, and return the overlapping information. '''
        # I'm wondering if it is really necessary to have two graph 
        # information variables. The directedGraph actually serves for 
        # restricting the ordering in each edge so that the script raises an 
        # error when there are loops in the sequence, but it seems that the 
        # problem just won't give us such a case. 
        self.directedGraph = {}
        self.undirectedGraph = defaultdict(set)
        for node in range(len(self.seqCollection)):
            candidates = self.getCandidates(node)
            for node2 in candidates:
                ovlp = self.fixOverlap(node, node2)
                if ovlp and ovlp[2] >= len(self.seqCollection[node])/2 and ovlp[2] >= len(self.seqCollection[node2])/2:
                    if ovlp[0] == 1:
                        assert (node2, node) not in self.directedGraph
                        self.directedGraph[(node, node2)] = ovlp[2]
                        self.undirectedGraph[node].add(node2)
                        self.undirectedGraph[node2].add(node)
                    elif ovlp[0] == 2:
                        assert (node, node2) not in self.directedGraph
                        self.directedGraph[(node2, node)] = ovlp[2]
                        self.undirectedGraph[node].add(node2)
                        self.undirectedGraph[node2].add(node)
        # Here find the end of the graph by searching for the nodes that has 
        # only one neighbor node.
        ends = []
        for src, tgt in self.undirectedGraph.items():
            if len(tgt) == 1:
                ends.append(src)
        assert len(ends) == 2
        # Here from the two ends determine the starting end, based on the 
        # assumptions above.
        read1 = ends[0]
        candidates = self.getCandidates(read1)
        read1Next = list(candidates)[0]
        if (read1, read1Next) in self.directedGraph:
            self.start = read1
        else:
            self.start = ends[1]

    def fixOverlap(self, node1, node2):
        '''Find all the shared k-mers and from the positions in the original 
        sequences to infer the prefix-suffix relationship'''
        seq1Kmers = set([i[0] for i in self.seq2kmer[node1]])
        seq2Kmers = set([i[0] for i in self.seq2kmer[node2]])
        seq1Pref = sorted(list(self.seq2kmer[node1]), key = lambda x: x[1])[0]
        seq1Suff = sorted(list(self.seq2kmer[node1]), key = lambda x: x[1])[-1]
        if seq1Pref[0] in seq2Kmers:
            for n, pos in self.kmer2seq[seq1Pref[0]]:
                if n == node2:
                    return (2, 1, len(self.seqCollection[node2]) - pos)
        elif seq1Suff[0] in seq2Kmers:
            for n, pos in self.kmer2seq[seq1Suff[0]]:
                if n == node2:
                    return (1, 2, pos + len(seq1Suff[0]))
        else:
            print('Didn\'t find matching k-mer in', node1, node2)
            exit(233)

    def concatenate(self):
        '''Here mainly use the undirected graph to traverse everything in the 
        correct order, which is kind of like BFS'''
        passed = {self.start}
        node = self.start
        while True:
            try:
                passed.add(node)
                nextNode = list(self.undirectedGraph[node].difference(passed))[0]
                ovlpLen = self.directedGraph[(node, nextNode)]
                self.asm += self.seqCollection[node][:len(self.seqCollection[node]) - ovlpLen]
                node = nextNode
            except IndexError:
                self.asm += self.seqCollection[node]
                break

    def __repr__(self):
        return self.asm
    def __str__(self):
        return self.asm

def main():
    # These are test small cases given on the Rosalind problem page
    X = "ATTAGACCTG"
    Y = "CCTGCCGGAA"
    Z = 'AGACCTGCCG'
    W = 'GCCGGAATAC'
    readlist = [W, X, Y, Z]
    # rosalind_long.fasta is at example/ folder
    #readlist = [str(record.seq) for record in SeqIO.parse("rosalind_long.fasta", "fasta")]
    asm = Assemble(readlist)
    print(asm)
    
if __name__ == '__main__':
    main()
