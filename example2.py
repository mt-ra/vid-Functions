from manim import *
from StackVisualiser.CodeFrame import *

class TestCode(ThreeDScene):
    def construct(self):
        mainGen1 = CodeBlock([]).from_list([
            ['int ', 'x ', '= ', '6', ';'],
            ['int ', 'y ', '= ', '9', ';'],
            ['std', '::', 'cout ', '<< ', ('swap', '420'), ('(', ''), ('x', ''), (', ', ''), ('y', ''), (')', ''), ';'],
            ['std', '::', 'cout ', '<< ', 'x ', '<< ', 'y', ';']
        ])
        mainPreReturnCol = [
            [KWD, VAR, OPER, NUM, VAR],
            [KWD, VAR, OPER, NUM, VAR],
            [CLS, OPER, VAR, OPER, FUNC, BRA, VAR, OPER, VAR, BRA, VAR],
            [CLS, OPER, VAR, OPER, VAR, OPER, VAR, VAR]
        ]

        mainPostReturnCol = [
            [KWD, VAR, OPER, NUM, VAR],
            [KWD, VAR, OPER, NUM, VAR],
            [CLS, OPER, VAR, OPER, NUM, BRA, VAR, OPER, VAR, BRA, VAR],
            [CLS, OPER, VAR, OPER, VAR, OPER, VAR, VAR]
        ]
        
        # remember to unwrite before transforming

        addGen1 = CodeBlock([]).from_list([
            ['int ', 'temp ', '= ', 'y'],
            ['y ', '= ', 'x', ';'],
            ['x ', '= ', 'temp', ';'],
            ['return ', '420', ';']
        ])
        
        addCol = [
            [KWD, VAR, OPER, VAR],
            [VAR, OPER, VAR, VAR],
            [VAR, OPER, VAR, VAR],
            [KWD, NUM, VAR]
        ]
        
        mainPreReturn = mainGen1.apply_color(mainPreReturnCol).generate([[], [], [0, 0, 0, 0, 0, 0], []])
        mainPostReturn = mainGen1.apply_color(mainPostReturnCol).generate([[], [], [1, 1, 1, 1, 1, 1], []])

        addPreCall = addGen1.apply_color(addCol).generate([[], [], [], []])
        addFinal = addGen1.apply_color(addCol).generate([[], [], [], []])

        mainWindow = CodeWindow(mainPreReturn)
        mainWindow.add(mainPostReturn)
        addWindow = CodeWindow(addFinal) # wtf i have to fix this


        # BEGIN ANIMATIONS
        self.play(Write(mainWindow.window), Write(mainWindow.paragraph))
        self.move_camera(phi=60*DEGREES, theta=-135*DEGREES, focal_distance=40)

        #another marker
        theMarker = CodeMarker(mainPreReturn, 0)
        mcp1 = CodeMarker(mainPreReturn, 1)
        mcp2 = CodeMarker(mainPreReturn, 2)
        mcp3 = CodeMarker(mainPostReturn, 2)
        mcp4 = CodeMarker(mainPostReturn, 3)

        self.play(Write(theMarker))
        theMarker.transform_marker(self, mcp1)
        theMarker.transform_marker(self, mcp2)

        # create add code frame
        mainPostReturn.set_opacity(0)
        self.play(mainWindow.animate.shift(IN))
        self.remove(mainPostReturn)
        mainPostReturn.set_opacity(1)


        # hide the called function in the function call
        self.play(FadeOut(addWindow.window), run_time = 0)
        self.add(addWindow.window)
        self.play(Transform(addPreCall, mainPreReturn.submobjects[2].submobjects[4]), run_time=0)
        self.add(addPreCall)
        self.play(FadeIn(addWindow.window), Transform(addPreCall, addFinal))

        # wait a bit
        self.wait(1)
        # pop the frame
        self.play(Unwrite(addWindow.window), Transform(addPreCall, mainPreReturn.submobjects[2].submobjects[4]))
        self.remove(addPreCall)
        
        # transform return value
        self.play(*mainWindow.unwrite_words(2, [5,6,7,8,9]))
        self.play(Unwrite(theMarker))
        self.play(ReplacementTransform(mainPreReturn, mainPostReturn))
        self.play(Create(theMarker))
        theMarker.transform_marker(self, mcp3)
        theMarker.transform_marker(self, mcp4)

        self.play(mainWindow.animate.shift(OUT))
        
        self.move_camera(phi=0*DEGREES, theta=-90*DEGREES, focal_distance=40)