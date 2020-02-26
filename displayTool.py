import sys
import copy

class progressBar():
    """
    Funny tool that enables you to display a progress bar with information
    Example:
    ----------
    ```
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
    ```
    """
    def __init__(self, maxSteps, title = None, infoDone = 'Done', 
                 length = 50, barStyle = '>-', titleColor = None, 
                 stepInfoColor = None, doneInfoColor = None):
        '''
        Arguments:
        ----------
        maxSteps      - `int`
                        The total steps of the iteration you want to display.
        title         - `str`, default `None`
        infoDone      - `str`, default `'Done'`
                        The info that will show up when the progress reaches 
                        the end
        length        - `int`, default `50`
                        The length of the "bar"
        barStyle      - `str`, default `'>-'`
                        For customized progress bar. 
                        `assert len(barStyle) == 2`
                        Examples:
                        When default '>-', the bar looks like: [>>>>---]
                        When  given  '= ', the bar looks like: [====   ]
        titleColor    - `str`, default `None`
                        See `cstrColor._ALIAS` for choices
        stepInfoColor - `str`, default `None`
                        See `cstrColor._ALIAS` for choices
        doneInfoColor - `str`, default `None`
                        See `cstrColor._ALIAS` for choices
        Returns:
        ----------
        `progressBar` object
        '''
        self.maxSteps = maxSteps
        self.i = 0
        if titleColor == None:
            self.title = title
        else:
            self.title = cstr(title, titleColor)
        if doneInfoColor == None:
            self.infoDone =  infoDone
        else:
            self.infoDone = cstr(infoDone, doneInfoColor)
        self.stepInfo = ''
        self.stepInfoColor = stepInfoColor
        self.length = length
        self.nDash = self.length
        self.nArrow = self.length - self.nDash
        self.percent = self.i * 100.0 / self.maxSteps
        assert len(barStyle) == 2 and isinstance(barStyle, str)
        self.ARROW, self.DASH = barStyle[0], barStyle[1]
        self.processBar = f'[{self.DASH * self.nDash}]0.00%'

    def proceed(self, i = None, info = None, infoColor = None):
        '''
        Move to the next step
        Arguments:
        ----------
        i    - `int`, default `None`
               Which step you want to jump to. If None, will move to the 
               "next" step.
        info - `str`, default `None`
               The specific task info for the current step. Can be changed
               during the period of a progress bar
        infoColor - `str`, default `None`
                    See `cstrColor._ALIAS` for choice. If None, follow the 
                    `stepInfoColor` at initialization, if given and valid, 
                    overwrite for current step.
        '''
        if i is not None:
            self.i = i
        else:
            self.i += 1
        if self.i == 1 and self.title != None:
            print(self.title)

        self.nArrow = int(self.i * self.length / self.maxSteps)
        self.nDash = self.length - self.nArrow
        self.percent = self.i * 100.0 / self.maxSteps

        if info != None:
            if infoColor != None:
                self.stepInfo = cstr(info, infoColor)
            else:
                self.stepInfo = cstr(info, self.stepInfoColor)
        else:
            self.stepInfo = ''

        self._updateProcessBar()
    
    def _updateProcessBar(self):
        self.processBar = (f'[{self.ARROW * self.nArrow}{self.DASH * self.nDash}]'
                           f'{self.percent:.2f}%\t{self.stepInfo}')
        if self.i >= self.maxSteps:
            self.processBar += f'\t{self.infoDone}'
        self.processBar += '\r'
        sys.stdout.write(self.processBar)
        sys.stdout.flush()
        if self.i >= self.maxSteps:
            print()

class cstrColor(object):
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
               'none': '\033[0m'}
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
              'wu': 'none', 'n': 'none'}
    _ALIAS.update({i: i for i in _WRAPPER})

    def __init__(self, length, colors = None):
        if colors is None:
            self.names = ['none'] * length
            self.codes = [''] * length
        if isinstance(colors, cstrColor):
            colors = colors.names
        if isinstance(colors, str):
            if colors not in self._ALIAS:
                if len(colors) == length:
                    colors = list(colors)
                    self.names = [self._ALIAS[i] for i in colors]
                    self.codes = [self._WRAPPER[i] for i in self.names]
                else:
                    raise ValueError("Given color is not supported.")
            else:
                self.names = [self._ALIAS[colors]] * length
                self.codes = [self._WRAPPER[i] for i in self.names]
        elif isinstance(colors, list):
            if length != len(colors):
                raise ValueError("Given color list length does not match "
                                 "string length")
            self.names = [self._ALIAS[i] for i in colors]
            self.codes = [self._WRAPPER[i] for i in self.names]

    def __str__(self):
        return f'<cstrColor names: {str(self.names)}>'

    def __repr__(self):
        return self.__str__()

    def __setitem__(self, key, value):
        if isinstance(value, str):
            if value not in self._ALIAS:
                raise ValueError("Given color is not supported.")
            nSub = len(self.names[key])
            value = self._ALIAS[value]
            self.names[key] = [value] * nSub
        elif isinstance(value, list):
            if len(self.names[key]) != len(value):
                raise ValueError("Given color list length does not match "
                                 "slice selection.")
            value = [self._ALIAS[i] for i in value]
            self.names[key] = value
        self.codes = [self._WRAPPER[i] for i in self.names]

    def __getitem__(self, key):
        newNames = self.names[key]
        return cstrColor(len(newNames), newNames)

    def tolist(self):
        return self.names

class cstr(str):
    '''
    str inherited object that can be displayed with color in command line 
    terminal.
    Arguments:
    ----------
    content - `object` with `.__str__()` method
    colors  - `str` or `list` of `str`, default `None`.
              1. If `list`, each element states the color of each character in 
              `str(content)`. 
                  `assert len(colors) == len(str(content))`
              2. If `str`, can be one of the keys of `cstrColor._ALIAS`, that 
              states all the color of the `cstr`
              3. If `str`, can also be a string sequence where each character
              states a color, e.g. `'rrgb'` states for `['red', 'red', 
              'green', 'blue']`. Note that choices for single-character key 
              word are limited.
                  `assert len(colors) == len(str(content))`
    Returns:
    ----------
    `cstr` object.
    '''
    _RESET = '\033[0m'

    def __new__(cls, content = None, colors = None):
        if isinstance(content, cstr):
            return cstr(content.str, colors = colors)
        elif content == None:
            obj = str.__new__(cls, '')
            obj.colorRecord = cstrColor(0, [])
            return obj
        else:
            obj = str.__new__(cls, content)
            obj.colorRecord = cstrColor(len(str(content)), colors)
            return obj

    def _getColor(self):
        return self.colorRecord

    def _setColor(self, color):
        self.colorRecord = cstrColor(len(str.__str__(self)), color)

    color = property(_getColor, _setColor)

    @property
    def str(self):
        '''
        Return the raw str content without color
        '''
        return str.__str__(self)

    def blockFormat(self, indentLen = 0, blockWidth = 78, 
                   indentFirstLine = False, color = None):
        '''
        Format long cstr to lines of text with fixed line length.
        Arguments:
        ----------
        indentLen       - `int`, default `0`
                          The number of spaces to add at the left of the text
                          block
        lenPerLine      - `int`, default `78`
                          The character number limit for each line, not 
                          including the indentation.
        indentFirstLine - `bool`, default `False`
                          Whether the first line follows the same indentation
                          scheme.
        color           - `str`, default `None`.
                          New color to display in the returned `cstr`. If 
                          NoneType, will follow the original color. If the 
                          coloring should be canceled, pass string `"none"`.
        Return:
        ----------
        `cstr`, with formatted string content and the same color
        ''' 
        if type(indentLen) != int:
            raise TypeError("indentLen should be an int.")
        if type(blockWidth) != int:
            raise TypeError("blockWidth should be an int.")
        wordList = self.split()
        wordLens = [len(i) for i in wordList]
        if blockWidth < max(wordLens):
            raise ValueError("Max word length larger than line length.")
        textBlock = ''
        lineLen = 0
        nLine = 0
        if indentFirstLine:
            textBlock = ' ' * indentLen
        while wordList:
            newWord = wordList.pop(0)
            if lineLen + len(newWord) > blockWidth:
                textBlock += '\n' + ' ' * indentLen + newWord + ' '
                lineLen = len(newWord) + 1
            else:
                textBlock += newWord + ' '
                lineLen += len(newWord) + 1
        return textBlock

    def __str__(self):
        output = ''
        lastColor = '\033[0m' # For no color
        if self.str == '':
            return ''
        for i in range(len(self)):
            if self.color.codes[i] != lastColor:
                output += self.color.codes[i]
            output += self.str[i]
            lastColor = self.color.codes[i]
        if lastColor != '\033[0m':
            output += self._RESET
        return output

    def __repr__(self):
        return(f'<cstr: str = {self.str.__repr__()}, '
               f'color = {self.color.names}>')

    def __add__(self, other):
        if not isinstance(other, cstr):
            if other.split() == []:
                otherColor = [self.color.names[-1]]
            else:
                otherColor = ['n']
            return cstr(self.str + str(other), 
                        self.color.names + otherColor * len(str(other)))
        else:
            return cstr(self.str + other.str, 
                        self.color.names + other.color.names)
    def __radd__(self, other):
        if not isinstance(other, cstr):
            if other.split() == []:
                otherColor = [self.color.names[0]]
            else:
                otherColor = ['n']
            return cstr(str(other) + self.str, 
                        otherColor * len(str(other)) + self.color.names)
        else:
            return cstr(other.str + self.str, 
                        other.color.names + self.color.names)

    def __iter__(self):
        self._iterI = -1
        return self

    def __next__(self):
        self._iterI += 1
        if self._iterI < len(self):
            return cstr(self.str[self._iterI], self.color.names[self._iterI])
        else:
            raise StopIteration

    def __getitem__(self, key):
        return cstr(self.str[key], self.color[key])

    def lower(self):
        return cstr(self.str.lower(), self.color.names)
    def upper(self):
        return cstr(self.str.upper(), self.color.names)

    def capitalize(self):
        return cstr(self.str[0].upper(), self.color.names[0]) + \
               cstr(self.str[1:].lower(), self.color.names[1:])

    def lstrip(self, chars = None):
        remainingContent = self.str.lstrip(chars)
        remainingLen = len(remainingContent)
        return cstr(remainingContent, self.color.names[-remainingLen:])

    def rstrip(self, chars = None):
        remainingContent = self.str.rstrip(chars)
        remainingLen = len(remainingContent)
        return cstr(remainingContent, self.color.names[remainingLen:])

    def split(self, sep = None, maxsplit = -1):
        outList = []
        if sep == None:
            seps = {' ', '\t', '\r', '\n'} #TODO check if anymore default sep
            step = 1
        else:
            seps = {sep}
            step = len(sep)
        lastSplit = 0
        inDefaultGap = False
        wait = 0
        for i in range(len(self.str)):
            if wait > 0:
                wait -= 1
                continue
            if self.str[i:i+step] in seps:
                if not inDefaultGap:
                    outList.append(cstr(self.str[lastSplit:i], 
                                        self.color[lastSplit:i]))
                    wait += step - 1
                if sep == None:
                    inDefaultGap = True
                lastSplit = i + step
            else:
                inDefaultGap = False
        if lastSplit < len(self.str):
            outList.append(cstr(self.str[lastSplit:len(self.str)], 
                                self.color[lastSplit:len(self.str)]))
        return outList

    def __contains__(self, key):
        return key in str.__str__(self)




if __name__=='__main__':
    maxSteps = 5000

    info1 = "Usually when writing an article, I have some type of theme. Something like politics, college life, or just some information about myself. There's always a theme. This time, however, will be a little different. I don't have a topic or theme this week. Not due to a lack of interesting things happening in the world, but more because I'm just not feeling it right now. So instead of some concise article dealing with a topic with some humor thrown in, I'm just going to wing it this week and see what happens."
    info1 = cstr(info1, 'midori')
    process_bar = progressBar(maxSteps, 'Process 1', infoDone = info1.blockFormat(blockWidth = 40, indentLen = 72))
    for i in range(maxSteps):
        if i < maxSteps / 2:
            nStep = 1
        else:
            nStep = 2
        process_bar.proceed(info = 'Step '+str(nStep))
    
    info2 = "To my knowledge, no Olympians have contracted the Zika virus or any super bacteria so far during the Rio Olympics. Which is good seeing as to how Rio was being compared to hell just weeks before the Olympics began. People were being robbed, babies were born with defects, and the ocean was being referred to as a toilet. With comments like these circling around the media, Hell was starting to look like a better alternative. At least Rio is turning out to be less of an apocalyptic place than we all thought. Although, it was reported that an athlete was kidnapped. On the other hand, he did know jiu jitsu, so that was more of his fault for letting it happen."
    info2 = cstr(info2, 'midori')
    process_bar2 = progressBar(maxSteps, 'Process 2', infoDone = info2.blockFormat(blockWidth = 40, indentLen = 72), barStyle = '= ', titleColor = 'g')
    for i in range(maxSteps):
        if i < maxSteps / 2:
            nStep = 1
        else:
            nStep = 2
        process_bar2.proceed(info = 'Step '+str(nStep), infoColor = 'red')