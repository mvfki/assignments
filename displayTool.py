import sys
import copy

class colorStr():
    '''
    String like object that can be displayed with color in command line 
    terminal. Supports many of the worthy str operation, see Methods.
    '''
    _RESET = '\033[0m'
    _WRAPPER = {'black': '\033[30m',
               'red': '\033[31m',
               'green': '\033[32m',
               'orange': '\033[33m',
               'blue': '\033[34m',
               'purple': '\033[35m',
               'cyan': '\033[36m',
               'lightgrey': '\033[37m',
               'darkgrey': '\033[90m',
               'lightred': '\033[91m',
               'lightgreen': '\033[92m',
               'yellow': '\033[93m',
               'lightblue': '\033[94m',
               'pink': '\033[95m',
               'lightcyan': '\033[96m', 
               'none': ''}
    _ALIAS = {'blk': 'black', 'kuro': 'black', 'hei': 'black', 
              'r': 'red', 'aka': 'red', 'hong': 'red', 
              'g': 'green', 'grn': 'green', 'midori': 'green', 'lv': 'green',
              'lu': 'green', 
              'o': 'orange', 'cheng': 'orange', 'ju': 'orange', 
              'jv': 'orange',
              'b': 'blue', 'ao': 'blue', 'lan': 'blue',
              'p': 'purple', 'murasaki': 'purple', 'zi': 'purple',
              'qing': 'cyan',
              'y': 'yellow', 'ki': 'yellow', 'huang': 'yellow',
              'momo': 'pink', 'fen': 'pink',
              'w': 'none', 'white': 'none', 'null': 'none', 
              'wu': 'none'}

    def __init__(self, s, color = None):
        '''
        Argument:
        ----------
        s - object
            The content of the string, will be transferred to str(s).
            If it is already a colorStr instance, will remain not changed.
        color - str, default None
                Name of the color that you want to display this string.
        '''
        if isinstance(s, colorStr):
            self = copy.copy(s)
        else:
            color = str(color).lower()
            if color not in self._WRAPPER:
                color = self._parseColor(color)
            if color != None:
                self.cName = color
                self.c = self._WRAPPER[color]
                self.s = str(s)

    def __str__(self):
        if self.cName == 'none':
            return self.s
        else:
            return self.c + self.s + self._RESET

    def __repr__(self):
        return(f'<colorStr: color = {self.cName}, s = {self.s}>')

    def _setColor(self, color):
        color = str(color).lower()
        if color not in self._WRAPPER:
            color = self._parseColor(color)
        self.cName = color
        self.c = self._WRAPPER[color]

    def _getColor(self):
        return self.cName

    _colorDoc = ('Get current color or reset the color.\n'
                 'Example:\n'
                 '>>> a = colorStr(\'hello world\', color = \'red\')\n'
                 '>>> a.color\n'
                 'red\n'
                 '>>> a.color = \'green\'\n'
                 '>>> a.color\n'
                 'green')
    color = property(_getColor, _setColor, doc = _colorDoc)

    def _parseColor(self, color):
        try:
            color = self._ALIAS[color]
        except KeyError:
            #if self.warn:
            #    raise ValueError(f'Input color {color} not understood. Reset'
            #                     'to \'none\'.\n')
            color = 'none'
        return color

    def toStr(self):
        return self.s

    def niceFormat(self, indentLen = 0, lenPerLine = 78, 
                   indentFirstLine = False, color = None):
        '''
        Format long colorStr to lines of text with fixed line length
        Arguments:
        ----------
        indentLen       - int, default 0
                          The number of spaces to add at the left of the text
                          block
        lenPerLine      - int, default 78
                          The character number limit for each line, not 
                          including the indentation.
        indentFirstLine - bool, default False
                          Whether the first line follows the same indentation
                          scheme.
        color           - str, default None.
                          New color to display in the returned colorStr. If 
                          NoneType, will follow the original color. If the 
                          coloring should be canceled, pass string "none".
        Return:
        ----------
        colorStr, with formatted string content and the same color
        ''' 
        if type(indentLen) != int:
            raise TypeError("indentLen should be an int.")
        if type(lenPerLine) != int:
            raise TypeError("lenPerLine should be an int.")
        wordList = self.s.split()
        wordLens = [len(i) for i in wordList]
        if lenPerLine < max(wordLens):
            raise ValueError("Max word length larger than line length.")
        lineLists = []
        line = ''
        nline = 0
        newWord = wordList.pop(0)
        while wordList:
            
            if line == '':
                # When come to a new line, check indentation.
                if nline == 0 and indentFirstLine:
                    line += ' ' * indentLen
                elif nline == 0 and not indentFirstLine:
                    pass
                else:
                    line += ' ' * indentLen
                line += newWord + ' '
            else:
                # Add word to to the line until it's out of limitation.
                newWord = wordList.pop(0)
                if nline == 0 and indentFirstLine and \
                   len(line) - indentLen + len(newWord) > lenPerLine:
                    lineLists.append(line)
                    line = ''
                    nline += 1
                elif nline == 0 and not indentFirstLine and \
                    len(line) + len(newWord) > lenPerLine:
                    lineLists.append(line)
                    line = ''
                    nline += 1
                elif nline > 0 and \
                     len(line) - indentLen + len(newWord) > lenPerLine:
                    lineLists.append(line)
                    line = ''
                    nline += 1
                else:
                    line += newWord + ' '

        toReturn = colorStr('\n'.join(lineLists), color = self.cName)
        if color != None:
            toReturn.color = color
        return toReturn

    def __len__(self):
        return len(self.s)

    def __getitem__(self, key):
        return colorStr(self.s[key], color = self.cName)

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
    
    def __contains__(self, key):
        return key in self.s

    def __iter__(self):
        self._iterI = -1
        return self

    def __next__(self):
        self._iterI += 1
        if self._iterI < len(self):
            return colorStr(self.s[self._iterI], color = self.cName)
        else:
            raise StopIteration

    def lower(self):
        return colorStr(self.s.lower(), color = self.cName)
    def upper(self):
        return colorStr(self.s.upper(), color = self.cName)

    def capitalize(self):
        return colorStr(self.s[0].upper(), color = self.cName) + \
               colorStr(self.s[1:].lower(), color = self.cName)

    def lstrip(self, chars = None):
        return colorStr(self.s.lstrip(chars), color = self.cName)

    def rstrip(self, chars = None):
        return colorStr(self.s.rstrip(chars), color = self.cName)

    def strip(self, chars = None):
        return colorStr(self.s.strip(chars), color = self.cName)

    def split(self, sep = None, maxsplit = -1):
        result = self.s.split(sep, maxsplit)
        result = [colorStr(i, color = self.cName) for i in result]
        return result

class progressBar():
    """
    Funny tool that enables you to display a progress bar with information
    Example:
    ----------
    iterableToHandle = list(range(10000))
    maxSteps = len(iterableToHandle
    PB = progressBar(maxSteps, 'Process Title', 
                     infoDone = 'Let you know that this is all set')
    for i in range(maxSteps):
        if i < maxSteps / 2:
            nStep = 1
            # doSomething(iterableToHandle[i])
        else:
            nStep = 2
            # doSomethingElse(iterableToHandle[i])
        PB.proceed(info = 'Step '+str(nStep))
    """
    def __init__(self, maxSteps, title = None, infoDone = 'Done', 
                 length = 50, titleColor = None, infoColor = None, 
                 infoDoneColor = None):
        '''
        Arguments:
        ----------
        maxSteps - int
                   The total steps of the iteration you want to display.
        title    - str, default None
        infoDone - str, default 'Done'
                   The info that will show up when the progress reaches the 
                   end
        length   - int, default 50
                   The length of the "bar"
        '''
        self.maxSteps = maxSteps
        self.i = 0
        self.title = title
        self.infoDone = infoDone
        self.currentInfo = ''
        self.length = length
        self.nDash = self.length
        self.nArrow = self.length - self.nDash
        self.percent = self.i * 100.0 / self.maxSteps
        self.processBar = f'[{"-"*self.nDash}]0.00%'

    def proceed(self, i = None, info = None):
        '''
        Move to the next step
        Arguments:
        ----------
        i    - int, default None
               Which step you want to jump to. If None, will move to the 
               "next" step.
        info - str, default None
               The specific task info for the current step. Can be changed
               during the period of a progress bar
        '''
        if i is not None:
            self.i = i
        else:
            self.i += 1
        if self.i == 1 and self.title != None:
            sys.stdout.write(self.title + '\n')

        self.nArrow = int(self.i * self.length / self.maxSteps)
        self.nDash = self.length - self.nArrow
        self.percent = self.i * 100.0 / self.maxSteps

        if info != None:
            self.currentInfo = info

        self._updateProcessBar()
    
    def _updateProcessBar(self):
        self.processBar = f'[{">" * self.nArrow}{"-" * self.nDash}]{self.percent:.2f}%\t{self.currentInfo}'
        if self.i >= self.maxSteps:
            self.processBar += f'\t{self.infoDone}'
        self.processBar += '\r'
        sys.stdout.write(self.processBar)
        sys.stdout.flush()
        if self.i >= self.maxSteps:
            print()
        
if __name__=='__main__':
    maxSteps = 20000

    info1 = "Processing f-strings simply breaks down into evaluating the expression (just like any other python expression) enclosed within the curly braces and then combining it with the string literal portion of the the f-string to return the value of the final string. There is no additional runtime processing required . This makes f-strings pretty fast and efficient."
    info1 = colorStr(info1, color = 'midori')
    process_bar = ShowProcess(maxSteps, 'Process 1', infoDone = info1.niceFormat(lenPerLine = 40, indentLen = 72))
    for i in range(maxSteps):
        if i < maxSteps / 2:
            nStep = 1
        else:
            nStep = 2
        process_bar.proceed(info = 'Step '+str(nStep))

    info2 = "Right off the bat, we don’t see the LOAD_ATTR and CALL_FUNCTION bytecode instructions — so %-string formatting avoids the overhead of global attribute lookup and python function invocation. This explains why it is faster than str.format(). But why %-string formatting is still slower than f-strings? One potential place where %-string formatting might be spending extra time is in the BINARY_MODULO bytecode instruction. I haven’t done thorough profiling of the BINARY_MODULO bytecode instruction but looking at the CPython source code, we can get a sense of why there might just be a tiny bit of overhead involved with invoking BINARY_MODULO:"
    info2 = colorStr(info2, color = 'midori')
    process_bar2 = ShowProcess(maxSteps, 'Process 2', infoDone = info2.niceFormat(lenPerLine = 40, indentLen = 72))
    for i in range(maxSteps):
        if i < maxSteps / 2:
            nStep = 1
        else:
            nStep = 2
        process_bar2.proceed(info = 'Step '+str(nStep))
