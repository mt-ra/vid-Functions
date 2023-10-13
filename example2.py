from manim import *

from StackVisualiser.CodeFrame import *

class TestCode(ThreeDScene):
	def construct(self):
		mainGen1 = CodeBlock([]).from_list([
			['#include ', '<iostream>'],
			[],
			['int ', 'main', '()', '{'],
			['    ', ('', 'std::'), 'cout ', '<< ', '"Hello World!\\n"', ';'],
			['    ', ('', 'std::'), 'cout ', '<< ', ('add', ''), ('(', ''), ('2', ''), (', ', ''), ('3', '5'), (')', ''), ';'],
			['}']
		]).apply_color([
			[KWD, NUM],
			[VAR],
			[KWD, FUNC, BRA, BRA],
			[VAR, CLS, VAR, OPER, STR, VAR],
			[VAR, CLS, VAR, OPER, FUNC, BRA, NUM, VAR, NUM, BRA, VAR],
			[BRA]
		])

		mainGen2 = CodeBlock([]).from_list([
			['#include ', '<iostream>'],
			['using namespace ', 'std', ';'],
			[''],
			['int ', 'main', '()', '{'],
			['    ', ('', 'std::'), 'cout ', '<< ', '"Hello World!\\n"', ';'],
			['    ', ('', 'std::'), 'cout ', '<< ', ('add', ''), ('(', ''), ('2', ''), (', ', ''), ('3', '5'), (')', ''), ';'],
			['}']
		]).apply_color([
			[KWD, NUM],
			[KWD, CLS, VAR],
			[VAR],
			[KWD, FUNC, BRA, BRA],
			[VAR, CLS, VAR, OPER, STR, VAR],
			[VAR, CLS, VAR, OPER, FUNC, BRA, NUM, VAR, NUM, BRA, VAR],
			[BRA]
		])

		mainGen3 = CodeBlock([]).from_list([
			['#include ', '<iostream>'],
			['using namespace ', 'std', ';'],
			[''],
			['int ', 'main', '()', '{'],
			['    ', ('', 'std::'), 'cout ', '<< ', '"Hello World!\\n"', ';'],
			['    ', ('', 'std::'), 'cout ', '<< ', ('add', ''), ('(', ''), ('2', ''), (', ', ''), ('3', '5'), (')', ''), ';'],
			['}']
		]).apply_color([
			[KWD, NUM],
			[KWD, CLS, VAR],
			[VAR],
			[KWD, FUNC, BRA, BRA],
			[VAR, CLS, VAR, OPER, STR, VAR],
			[VAR, CLS, VAR, OPER, FUNC, BRA, NUM, VAR, NUM, BRA, VAR],
			[BRA]
		])

		addGen1 = CodeBlock([]).from_list([
			['int ', 'add', '(', 'int ', 'a, ', 'int ', 'b', ') ', '{'],
			['    ', '// ', ('', 'a = 2; b = 3;')],
			['    ', 'return ', 'a ', '+ ', 'b', ';'],
			['}']
		]).apply_color([
			[KWD, FUNC, BRA, KWD, VAR, KWD, VAR, BRA, BRA],
			[VAR, COM, COM],
			[VAR, KWD, VAR, OPER, VAR, VAR],
			[BRA]
		])

		main1 = mainGen1.generate([[], [], [], [1], [1, 0, 0, 0, 0, 0, 0], []])
		main2 = mainGen1.generate([[], [], [], [0], [0, 0, 0, 0, 0, 0, 0], []])
		main3 = mainGen2.generate([[], [], [], [], [0], [0, 0, 0, 0, 0, 0, 0], []])
		main4 = mainGen3.generate([[], [], [], [], [0], [0, 0, 0, 0, 0, 0, 0], []])
		main5 = mainGen3.generate([[], [], [], [], [0], [0, 1, 1, 1, 1, 1, 1], []])
		main5.shift(IN)

		add1 = addGen1.generate([[], [0], [], []])
		add2 = addGen1.generate([[], [1], [], []])


		mainSF = CodeWindow(main1)

		addSF = CodeWindow(add1)

		## ANIMATIONS
		self.play(Write(mainSF))
		marker1 = CodeMarker(main1, 0)
		marker2 = CodeMarker(main1, 4)
		marker3 = CodeMarker(main2, 4)
		
		self.play(Write(marker1))

		marker1.transform_marker(self, marker2)

		self.play(
			*mainSF.unwrite_words(3, [1]), 
			*mainSF.unwrite_words(4, [1]) 
		)
		self.play(Transform(main1, main2), Transform(marker1, marker3))

		self.play(Transform(main1, main3))

		self.play(Unwrite(marker1))

		self.move_camera(phi=60*DEGREES, theta=-135*DEGREES, focal_distance=40)

		self.play(Transform(main1, main4))
		self.play(mainSF.animate.shift(IN))
		self.play(Write(addSF))
		self.wait(1)
		self.play(Transform(add1, add2))
		self.wait(2)

		# unwrite window and transform paragraph
		self.play(Unwrite(addSF.window), Transform(addSF.paragraph, mainSF.paragraph.submobjects[5].submobjects[4]))
		self.remove(addSF.paragraph)
		self.remove(addSF)

		self.play(*mainSF.unwrite_words(5, [4,5,6,7,9]))

		self.play(Transform(main1, main5))
		self.play(mainSF.animate.shift(OUT))

		self.move_camera(phi=0*DEGREES, theta=-90*DEGREES, focal_distance=40)

		

