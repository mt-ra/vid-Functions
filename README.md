# Function Video
Beginner python / manim project.
Visualising functions in C.

## Stack Visualiser
The main feature of this project is the Stack Visualiser
In the StackVisualiser directory is a couple manim classes.
This is to assist with visualising code, control flow and memory usage.

### CodeFrame.py**
This will be one of the most convoluted, unreadable piles of garbage you have ever seen.

Contains the following classes:
- CodeWord
- CodeLine
- CodeBlock
- CodeWindow
- CodeMarker (currently broken)

This class was created to enable aesthetic transformations of the displayed code.

The method was inspired by Logan Smith @_noisecode.

In the words of the man himself (on the Manim Discord Server):

```
howdy! basically I do some trickery where I use a Text and then afterward "reorganize" its submobjects
two key realizations:
1) Texts just have all their characters as individual submobjects,
2) manim tries to 'align' data, including submobjects, for transform animations

so if I want a specific part of some code to animate to become some specific other code, I just have to make sure manim thinks those two groups of characters are "the same" submobject of the parent Text
basically if I have [some code like this] and I want to animate/stretch code so that it becomes [some longer_code like this]:

I "nest" [code] under a child submobject. so the root object becomes [some [] like this], where [] is a nested group that contains code. then I animate it to a new Text, which still says [some [] like this], but where the [] is now a nested group that says [longer_code] then when you Transform between those two root objects, it looks exactly how you'd want
```

#### How the hell does this module work?

CodeWord, CodeLine, CodeBlock and CodeWindow are not classes that contain MObjects themselves. These only contain data, like the text in the code block, and all the colors.
You can generate an actual Paragraph MObject from a CodeBlock instance using the `.generate()` method.

The generate method takes in an array of arrays of variant numbers (i cbs to explain this rn), and returns a Paragraph MObject.

Variants are used for animating transformation of certain words into other words.
A variant contains several outcomes, each given by a variant number.

### StackFrame.py**
Not complete.
The goal is to visualise how data is stored in memory.

Contains the following classes:

## How I use my Stack Visualiser
A few of my aesthetic choices.

**3d Camera Movements**
I like moving my camera to an oblique position to capture the 3D movements.

**When variant outcomes are empty**
Funky stuff happens when one of the outcomes in a variant is empty, and you try to transform from nonempty to empty or viceversa.
The stuff travels to the coordinates (0,0,0) which often looks ugly / confusing.
Unwrite the stuff before transforming.

**Popping from the stack**
Unwrite the window and transform the return value into the function call.
Then unwrite the function call, and replace it with the return value.

```py
# unwrite window and transform paragraph
# SF stands for stack frame

# make the function appear to get sucked into the function call
self.play(Unwrite(addSF.window), Transform(addSF.paragraph, mainSF.paragraph.submobjects[5].submobjects[4]))
self.remove(addSF.paragraph) # remove to prevent funky behavior
self.remove(addSF) # remove to prevent funky behavior

# transform the function call into the result of the function
self.play(*mainSF.unwrite_words(5, [4,5,6,7,9]))
self.play(Transform(main1, main5))

# the lower stack frame rises to fill the void
self.play(mainSF.animate.shift(OUT))
```