from manim import *
from typing import List, Union, Tuple

#
CANVAS_WIDTH : int = 14
CANVAS_HEIGHT : int = 8

# FONTS
CODE_FONT : str = "Monospace"
CODE_FONT_SIZE : int = 16
CODE_LINE_SPACE : float = 1
CODE_LINE_HEIGHT : float = 0.7

# CODE MARKERj
CODE_MARKER_PAD: float = 0.3

# WINDOW SIZE
CODEWINDOW_WIDTH : int = 6
CODEWINDOW_HEIGHT : int = 7

CODEPAD_LEFT : int = 0.5
CODEPAD_TOP : int = 0.5
STACK_SPACING : int = 1

# COLORS
CODE_WINDOW_BG_FILL_COLOR : str = "#1e1e2e"
CODE_WINDOW_BG_FILL_OPACITY : float = 0.9

# SYNTAX COLORS
KWD : str = "#b4befe" # keyword
NUM : str = "#eba0ac" # literal number
VAR : str = "#cdd6f4" # variable + normal
FUNC : str = "#89b4fa" # function
OPER : str = "#cba6f7" # operator
STR : str = "#a6e3a1" # operator
BRA : str = "#dec573" # brackets
CLS : str = "#e8b961" # class
COM : str = "#505050" # comment

###############################################################################
### UHM JUST DONT TOUCH ANYTHING UP UNTIL CODEBLOCK ###########################
###############################################################################

class CodeWord:
    def __init__(self, text : str, color):
        self.text = text
        self.color = color
        self.nonspace_len = len(text) - text.count(' ') - text.count('\n')
        self.begin = 0
        self.end = self.begin + self.nonspace_len

class CodeWordVariant:
    def __init__(self, words):
        self.num_words = len(words)
        self.words = []

        # check valid arguments
        for word in words:
            if isinstance(word, CodeWord):
                self.words.append(word)
            else:
                raise Exception("Arg should be a list of Words")

class CodeLine:
    def __init__(self, words : List[Union[CodeWord, CodeWordVariant]]):
        self.words = []
        self.num_words = len(words)
        self.num_variants = 0

        for word in words:
            if isinstance(word, CodeWord):
                self.words.append(word)
            elif isinstance(word, CodeWordVariant):
                self.words.append(word)
                self.num_variants += 1
            else:
                raise Exception("Arg should be a list of Words / WordVariants")

    # alternative way of creating a CodeLine object
    @staticmethod
    def from_list(wordList : List[Union[str, Tuple[str]]]):
        result = CodeLine([])
        result.words = []
        result.num_words = len(wordList)
        result.num_variants = 0

        for word in wordList:
            if isinstance(word, str):
                result.words.append(CodeWord(word, WHITE))
            elif isinstance(word, tuple):
                outcomeList = []
                for outcome in word:
                    outcomeList.append(CodeWord(outcome, WHITE))
                result.words.append(CodeWordVariant(outcomeList))
                result.num_variants += 1
            else:
                raise Exception("Args should be list of str or tuples of str")
        return result

    def apply_color(self, colList : List[str]):
        #assert len(colList) == self.num_words

        for i in range(len(self.words)):
            word = self.words[i]
            color = colList[i]

            if isinstance(word, CodeWord):
                word.color = color
            elif isinstance(word, CodeWordVariant):
                for outcome in word.words:
                    outcome.color = color
        return self

    # converts CodeLine into a string
    # also indexes the CodeWords (sets their begin and end attributes)
    def generate(self, word_varnums: List[int]):
        assert len(word_varnums) == self.num_variants

        # generate the text and index CodeWords
        text = ""
        cur_nonspace_chars = 0
        cur_word_variant = 0
        for word in self.words:
            if isinstance(word, CodeWordVariant):
                word = word.words[word_varnums[cur_word_variant]]
                cur_word_variant += 1
            text += word.text

            # indexing
            word.begin = cur_nonspace_chars
            word.end = word.begin + word.nonspace_len
            cur_nonspace_chars = word.end

        return text

############################################################################
#### DONT TOUCH ANYTHING ABOVE #############################################
############################################################################

class CodeBlock:
    # you will rarely use this constructor
    def __init__(self, lines : List[CodeLine]):
        self.lines = []
        self.num_lines = len(lines)

        for line in lines:
            if isinstance(line, CodeLine):
                self.lines.append(line)
            else:
                raise Exception("Arg should be a list of CodeLines / CodeLineVariants")
    
    # alternative way of creating a codeblock
    @staticmethod
    def from_list(lineList : List[List[Union[str, Tuple[str]]]]):
        result = CodeBlock([])
        result.lines = []
        result.num_lines = len(lineList)

        for line in lineList:
            if isinstance(line, list):
                result.lines.append(CodeLine.from_list(line))
            else:
                raise Exception("Invalid Args") 
        return result

    # applies coloring to the paragraph
    def apply_color(self, colMatrix : List[List[str]]):
        for i in range(len(self.lines)):
            line = self.lines[i]
            colList = colMatrix[i]
            line.apply_color(colList)
        return self

    # THIS FUNCTION IS VERY FRAGILE
    def generate(self, word_varnums: List[List[int]]):
        assert len(word_varnums) == self.num_lines

        text = ""
        for i in range(len(self.lines)):
            line = self.lines[i]
            text += line.generate(word_varnums[i])
            text += '\n'
        
        para = Paragraph(
            text, 
            font=CODE_FONT,
            font_size=CODE_FONT_SIZE,
            line_spacing=CODE_LINE_SPACE
        )

        # NOW DO GROUPING AND COLORING
        for i in range((len(self.lines))):
            line = self.lines[i]

            # shorthand for the submobjects of the current line
            paraline = para.submobjects[i].submobjects
            
            newparaline = []
            cur_word_variant = 0
            for j in range(len(line.words)):
                word = line.words[j]

                if isinstance(word, CodeWordVariant):
                    word = word.words[word_varnums[i][cur_word_variant]]
                    cur_word_variant += 1

                # fill a group with certain characters
                group = VGroup()
                for k in range(word.begin, word.end):
                    group += paraline[k]
                
                group.fill_color = word.color
                newparaline.append(group)

            # Replaces the current line with a single Text mobject
            # Use Text rather than VGroup
            paralineAsText = Text("")
            paralineAsText.submobjects = newparaline
            para.submobjects[i] = paralineAsText
        
        return para

# CODE WINDOW CLASS.

class CodeWindow(VGroup):
    
    def __init__(self, variants : List[Paragraph], caller):
        # The paragraph
        self.variants = variants
        self.activeParagraph = self.variants[0]

        # THE WINDOW
        self.window = RoundedRectangle(
            width=CODEWINDOW_WIDTH,  
            height=CODEWINDOW_HEIGHT, 
            fill_color=CODE_WINDOW_BG_FILL_COLOR, 
            fill_opacity=CODE_WINDOW_BG_FILL_OPACITY
        )

        self.caller = caller
        self.currentVariant = 0

        # FINALLY ADDING EVERYTHING TOGETHER
        super().__init__(self.window, self.activeParagraph)
        
            
    ### ENTITY SETUP FUNCTIONS ################################################################

    def AlignCodeTopLeft(self):
        # TODO: make variants move with the window
        def align_with_window(paragraph : Paragraph):
            paragraph.move_to(self.window.get_center())
            paragraph.shift(LEFT * CODEWINDOW_WIDTH / 2 + UP * CODEWINDOW_HEIGHT / 2)
            paragraph.shift(RIGHT * paragraph.get_width() / 2 + DOWN * paragraph.get_height() / 2)
            paragraph.shift(RIGHT * CODEPAD_LEFT + DOWN * CODEPAD_TOP)
            
        for paragraph in self.variants:
            align_with_window(paragraph)
            paragraph.add_updater(align_with_window)

    ### ANIMATION METHODS & INTERFACE ###################################################
    
    # use scene.play
    # WARNING: UNWRITE ALL WORDS THAT SIMPLY DISAPPEAR
    def NextVariant(self):
        self.currentVariant += 1
        return AnimationGroup(
            Transform(self.activeParagraph, self.variants[self.currentVariant])
        )
        
    def ShiftIn(self):
        return AnimationGroup(self.animate.shift(IN * STACK_SPACING))
    
    @staticmethod
    def ShiftInMany(windows):
        return AnimationGroup(*[x.ShiftIn() for x in windows])
        
    # WARNING: move everything else downwards before manually
    def PushCodeFrame(self):
        self.AlignCodeTopLeft()
        return Succession(
            Write(self.window),
            Write(self.activeParagraph)
        )
        
    # use scene.play
    def UnwriteWords(self, line_number : int, word_numbers : List[int]):
        return AnimationGroup(*[Unwrite(self.activeParagraph.submobjects[line_number].submobjects[i]) for i in word_numbers])

    # use scene.play
    def PopCodeFrame(self, line_number : int, word_number : int):
        return Succession(
            AnimationGroup(
                Unwrite(self.window), 
                ReplacementTransform(
                    self.activeParagraph,
                    self.caller.activeParagraph.submobjects[line_number].submobjects[word_number]
                )
            )
        )