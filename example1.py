from manim import *
from StackVisualiser.CodeFrame import *

class TestCode(ThreeDScene):
    def construct(self):

        ###################################################################################
        ####### SETTING THE VALUES OF THE CODEBLOCK
        mainList = [
            ['int ', 'x ', '= ', '6', ';'],
            ['int ', 'y ', '= ', '9', ';'],
            ['std', '::', 'cout ', '<< ', ('swap', '420'), ('(', ''), ('x', ''), (', ', ''), ('y', ''), (')', ''), ';'],
            ['std', '::', 'cout ', '<< ', 'x ', '<< ', 'y', ';']
        ]
        mainVar1Nums = [[], [], [0, 0, 0, 0, 0, 0], []]
        mainVar2Nums = [[], [], [1, 1, 1, 1, 1, 1], []]
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
        mainGen = CodeBlock.from_list(mainList)
        ###################################################################################

        fnList = [
            ['int ', 'x ', '= ', '6', ';'],
            ['int ', 'y ', '= ', '9', ';'],
            ['int ', 'x ', '= ', '6', ';'],
            ['int ', 'y ', '= ', '9', ';'],
            ['int ', 'x ', '= ', '6', ';'],
            ['int ', 'y ', '= ', '9', ';'],
            ['int ', 'x ', '= ', '6', ';'],
            ['int ', 'y ', '= ', '9', ';'],
        ]
        fnVarNums = [[], [], [], [], [], [], [], []]
        fnGen = CodeBlock.from_list(fnList)
        
        #############################################################################
        #### THING HERE TO PREVENT BUGS IDK HOW TO FIX
        _base = CodeBlock.from_list(mainList).generate(mainVar1Nums)
        _base_window = CodeWindow([_base], 0)
        _base_window.AlignCodeTopLeft()
        #############################################################################
        
        # MY ACTUAL ENTITIES
        mainInst1Var1Para = mainGen.apply_color(mainInst1Var1Cols).generate(mainVar1Nums)
        mainInst1Var2Para = mainGen.apply_color(mainInst1Var2Cols).generate(mainVar2Nums)
        mainInst1Window = CodeWindow([mainInst1Var1Para, mainInst1Var2Para], _base_window)
        mainInst1Window.PositionLeft()

        mainInst2Var1Para = mainGen.apply_color(mainInst1Var1Cols).generate(mainVar1Nums)
        mainInst2Var2Para = mainGen.apply_color(mainInst1Var2Cols).generate(mainVar2Nums)
        mainInst2Window = CodeWindow([mainInst2Var1Para, mainInst2Var2Para], mainInst1Window)
        mainInst2Window.PositionLeft()

        fnPara = fnGen.generate(fnVarNums)
        fnWindow = CodeWindow([fnPara], mainInst2Window)
        fnWindow.PositionLeft()
        
        # BEGIN ANIMATIONS

        # PREPARE TO PUSH MAIN
        

        mainInst1Window.AlignCodeTopLeft()
        self.play(mainInst1Window.PushCodeFrame())

        self.move_camera(phi=60*DEGREES, theta=-135*DEGREES, focal_distance=40)

        self.play(CodeWindow.ShiftInMany([mainInst1Window]))
        self.play(mainInst2Window.PushCodeFrame())
        self.play(CodeWindow.ShiftInMany([mainInst1Window, mainInst2Window]))

        self.play(fnWindow.PushCodeFrame())

        self.wait(1)

        self.play(fnWindow.PopCodeFrame(2, 4))
        self.play(CodeWindow.ShiftOutMany([mainInst1Window, mainInst2Window]))

        self.play(mainInst2Window.UnwriteWords(2, [5,6,7,8,9]))
        self.play(mainInst2Window.NextVariant())
        self.play(mainInst2Window.PopCodeFrame(2, 4))

        # transform return value
        self.play(mainInst1Window.UnwriteWords(2, [5,6,7,8,9]))
        self.play(mainInst1Window.NextVariant())
        
        self.move_camera(phi=0*DEGREES, theta=-90*DEGREES, focal_distance=40)