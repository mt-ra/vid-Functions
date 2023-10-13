from manim import *
from typing import List, Union, Tuple

# FONTS
CODE_FONT : str = "Monospace"
CODE_FONT_SIZE : int = 30
CODE_LINE_SPACE : float = 1
CODE_LINE_HEIGHT : float = 0.7

CODE_PAD_X: float = 1
CODE_PAD_Y: float = 1

CODE_MARKER_PAD: float = 0.3

# COLORS
CODE_WINDOW_BG_FILL_COLOR : str = "#1e1e2e"
CODE_WINDOW_BG_FILL_OPACITY : float = 1

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
	def from_list(self, wordList : List[Union[str, Tuple[str]]]):
		self.words = []
		self.num_words = len(wordList)
		self.num_variants = 0

		for word in wordList:
			if isinstance(word, str):
				self.words.append(CodeWord(word, WHITE))
			elif isinstance(word, tuple):
				outcomeList = []
				for outcome in word:
					outcomeList.append(CodeWord(outcome, WHITE))
				self.words.append(CodeWordVariant(outcomeList))
				self.num_variants += 1
			else:
				raise Exception("Args should be list of str or tuples of str")
		return self

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

class CodeBlock:
	def __init__(self, lines : List[CodeLine]):
		self.lines = []
		self.num_lines = len(lines)

		for line in lines:
			if isinstance(line, CodeLine):
				self.lines.append(line)
			else:
				raise Exception("Arg should be a list of CodeLines / CodeLineVariants")
	
	def from_list(
			self, 
			lineList : List[List[Union[str, Tuple[str]]]], 
			):
		self.lines = []
		self.num_lines = len(lineList)

		for line in lineList:
			if isinstance(line, list):
				lineObj = CodeLine([])
				lineObj.from_list(line)
				self.lines.append(lineObj)
			else:
				raise Exception("Invalid Args")	
		return self

	def apply_color(self, colMatrix : List[List[str]]):
		#assert len(colMatrix) == self.num_lines

		for i in range(len(self.lines)):
			line = self.lines[i]
			colList = colMatrix[i]
			line.apply_color(colList)
		return self

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

class CodeWindow(VGroup):
	def __init__(self, paragraph : Paragraph):
		self.paragraph = paragraph
		
		# THE WINDOW
		self.window = RoundedRectangle(
			width=self.paragraph.width + CODE_PAD_X,	 
			height=self.paragraph.height + CODE_PAD_Y, 
			fill_color=CODE_WINDOW_BG_FILL_COLOR, 
			fill_opacity=CODE_WINDOW_BG_FILL_OPACITY
		)
		def update_window_dimensions(w):
			w.stretch_to_fit_width(self.paragraph.width + CODE_PAD_X)
			w.stretch_to_fit_height(self.paragraph.height + CODE_PAD_Y)
		self.window.add_updater(update_window_dimensions)

		# FINALLY ADDING EVERYTHING TOGETHER
		super().__init__(self.window, self.paragraph)

	def unwrite_words(self, line_number : int, word_numbers : List[int]):
		return [Unwrite(self.paragraph.submobjects[line_number].submobjects[i]) for i in word_numbers]
	
class CodeMarker(RoundedRectangle):
	# MARKER TO SHOW WHERE WE ARE UP TO IN THE CODE
	def __init__(self, paragraph : Paragraph, line_number : int):
		self.paragraph = paragraph
		super().__init__(
			width=self.paragraph.width + CODE_MARKER_PAD, # CONST FOR PADDING
			height=CODE_LINE_HEIGHT,
			fill_color=WHITE,
			fill_opacity=0.3,
			stroke_color=WHITE,
			stroke_opacity=0.3,
			corner_radius=0.1
		)
		self.line_number = line_number
		self.line_marked = self.paragraph.submobjects[self.line_number]

		self.move_to(self.paragraph.submobjects[line_number].get_center())
		def update_marker_dimensions(m):
			m.move_to(self.line_marked.get_center())
			m.stretch_to_fit_width(self.line_marked.get_width() + CODE_MARKER_PAD)
		self.add_updater(update_marker_dimensions)

	def transform_marker(self, scene : Scene, other):
		self.suspend_updating()
		self.line_number = other.line_number
		self.line_marked = other.line_marked
		scene.play(Transform(self, other))
		self.resume_updating()
