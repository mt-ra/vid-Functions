from manim import *
from StackVisualiser.CodeFrame import *

class TestCode(ThreeDScene):
    def construct(self):

        # DATA
        mainGen = CodeBlock.from_list([
            ['int ', 'x ', '= ', '6', ';'],
            ['int ', 'y ', '= ', '9', ';'],
            ['std', '::', 'cout ', '<< ', ('swap', '420'), ('(', ''), ('x', ''), (', ', ''), ('y', ''), (')', ''), ';'],
            ['std', '::', 'cout ', '<< ', 'x ', '<< ', 'y', ';']
        ])
        mainInst1Var1Cols = [
            [KWD, VAR, OPER, NUM, VAR],
            [KWD, VAR, OPER, NUM, VAR],
            [CLS, OPER, VAR, OPER, FUNC, BRA, VAR, OPER, VAR, BRA, VAR],
            [CLS, OPER, VAR, OPER, VAR, OPER, VAR, VAR]
        ]

        mainInst1Var2Cols = [
            [KWD, VAR, OPER, NUM, VAR],
            [KWD, VAR, OPER, NUM, VAR],
            [CLS, OPER, VAR, OPER, NUM, BRA, VAR, OPER, VAR, BRA, VAR],
            [CLS, OPER, VAR, OPER, VAR, OPER, VAR, VAR]
        ]
        
        # ENTITIES
        mainInst1Var1Para = mainGen.apply_color(mainInst1Var1Cols).generate([[], [], [0, 0, 0, 0, 0, 0], []])
        mainInst1Var2Para = mainGen.apply_color(mainInst1Var2Cols).generate([[], [], [1, 1, 1, 1, 1, 1], []])
        mainInst1Window = CodeWindow([mainInst1Var1Para, mainInst1Var2Para], None)

        mainInst2Var1Para = mainGen.apply_color(mainInst1Var1Cols).generate([[], [], [0, 0, 0, 0, 0, 0], []])
        mainInst2Var2Para = mainGen.apply_color(mainInst1Var2Cols).generate([[], [], [1, 1, 1, 1, 1, 1], []])
        mainInst2Window = CodeWindow([mainInst2Var1Para, mainInst2Var2Para], mainInst1Window)

        # BEGIN ANIMATIONS
        self.play(Write(mainInst1Window))
        self.move_camera(phi=60*DEGREES, theta=-135*DEGREES, focal_distance=40)

        self.play(mainInst1Window.animate.shift(IN))
        self.play(mainInst2Window.PrepareForPushCodeFrame(2, 4), run_time = 0)
        self.play(mainInst2Window.PushCodeFrame())

        self.play(mainInst2Window.PopCodeFrame(2, 4))

        # transform return value
        self.play(mainInst1Window.UnwriteWords(2, [5,6,7,8,9]))
        self.play(mainInst1Window.NextVariant())
        
        self.move_camera(phi=0*DEGREES, theta=-90*DEGREES, focal_distance=40)