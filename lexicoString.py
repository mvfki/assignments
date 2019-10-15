'''http://rosalind.info/problems/lexv/
In this practice I also tried some implementation of class methods
'''

from itertools import permutations

class lexv():
    """Somehow like building a comination with replacement.

    alphabet - a list of element with ordering
    n        - an int of the maximum output length"""
    def __init__(self, alphabet, n):
        '''Initialize the input and run the iterations'''
        self.alphabet = alphabet
        self.alphabet.insert(0, '')
        self.n = n
        self.out = []
        self.iter = 0
        for i in range(n):
            self.iterate()

    def iterate(self):
        '''Run an iteration to extend the list in place'''
        if self.out == []:
            self.out = self.alphabet.copy()
        else:
            self.tmp = []
            for e in self.out:
                if e:
                    if len(e) < self.iter:
                        self.tmp.append(e)
                        continue
                    for i in self.alphabet:
                        self.tmp.append(e + i)
            self.out = self.tmp.copy()
        self.iter += 1

    def __len__(self):
        '''Returns the number of generated strings'''
        return len(self.out)

    def __getitem__(self, start, stop = None, step = None):
        '''Allow using slicing syntax to get items from output'''
        if stop == None:
            return self.out[start]
        else:
            end = stop
        if step == None:
            stride = 1
        else:
            stride = step
        return self.out[start:end:stride]

    def __iter__(self):
        '''Generates an iterator that go through each string generated in 
        lexicographical order'''
        self._pointer = -1
        return self

    def __next__(self):
        self._pointer += 1
        if self._pointer == len(self):
            raise StopIteration
        return self.out[self._pointer]

    def __repr__(self):
        '''Returns some text about the summary'''
        content = 'lexv build from alphabet ' + str(self.alphabet[1:]) + ', with maximum length ' + str(self.n) + '\n'
        if len(self) > 10:
            for i in range(5):
                content += self.out[i] + '\n'
            content += '.' * max(self.n, 3) + '\n'
            for i in range(5):
                content += self.out[-5 + i] + '\n'
        else:
            for i in range(len(self)):
                content += self.out[i] + '\n'
        content += 'Totally %d elements' % len(self)
        return content

if __name__ == '__main__':
    In = 'D N'.split(' ')
    n = 3
    l = lexv(In, n)
    print('__repr__ test')
    print(l)
    print('Iterator test')
    print('for i in l:\n    print(i)')
    for i in l:
        print(i)
    print('__getitem__ test', 'l[::-1] =>', l[::-1])
