# geosolver
geosolver is an end-to-end system that solves high school geometry questions.
That is, its input is question text in natural language and diagram in raster graphics,
and its output is the answer to the question.

geosolver is divided into four core parts: diagram praser, text parser, joint parser, and solver.
Text parser transforms the text in natural language into a logical form.
Diagram parser extracts information from the diagram.
Joint parser combines the results of the text parser and the diagram parser and outputs the final logical form.
Solver accepts the logical form from the joint parser and outputs the answer.
This tutorial will first walkthrough each part independently (the modules except the joint parser can be used independently),
and in the last section it will show how to connect them for an end-to-end system.

## Accessing questions via GeoServer
Location: `geosolver.database`

Required 3rd-party packages: requests

Every question is a tuple of key, text, words, diagram path, and choices (see `geosolver.database.states.Question`).
You can either define it yourself, or more easily, you can download it via GeoServer, a web interface for managing and displaying geosolver database. Please refer to the GeoServer repository to see how to set it up.

1. Make sure that `geosolver.settings.GEOSERVER_URL` has a correct URL. Note that by default this is pointing to a local server, because I am hosting a local server myself.
2. Import the geoserver interface (an instance of `geosolver.database.geoserver_interface.GeoServerInterface`):
```python
from geosolver import geoserver_interface
```
3. To download all questions tagged 'test' and print the text of each, type:
```python
questions = geoserver_interface.download_questions('test')
for id_, question in questions.iteritems():
  print(question.text)
```
Note that the object returned by `geoserver_interface.download_questions` is a `dict` object.
4. To download a single question with specific id (e.g. 1037), type:
```python
questions = geoserver_interface.download_questions(1037)
print(questions.values()[0].text)
```
Note that, regardless of the number of questions returned by `geoserver_interface.download_questions`, the returned object is always a `dict` object (with possibly single element, like above).
5. You can access other properties of the question by `question.words`, `question.diagram_path`, and `question.choices`. See Diagram parser section to learn how to use `question.diagram_path`, and see Text parser section to learn how to use `question.words` and `question.choices`.


## Diagram parser
Location: `geosolver.diagram`

Required 3rd-party packages: numpy, OpenCV 3.0.0 or higher (cv2)

Diagram parsing consists of five finer steps: image segment parsing, primitive paring, primitive selecting, core parsing, and graph parsing. We will explain each of them in detail below. You can also refer to `geosolver.diagram.run_diagram` module to see full examples corresponding to these.

### Parsing image segments
Image segment parsing is the task of obtaining the diagram segment (and label segments) from the original image.
For instance, given an original image

![original image]
(https://github.com/seominjoon/geosolver/blob/master/images/original.png)

we obtain the diagram segment

![diagram segment]
(https://github.com/seominjoon/geosolver/blob/master/images/diagram.png)

To do so, obtain a `Question` object (`question`) and run the following:
```python
image_segment_parse = parse_image_segments(open_image(question.diagram_path))
image_segment_parse.diagram_image_segment.display_binarized_segmented_image()
for idx, label_image_segment in image_segment_parse.label_image_segments.iteritems():
  label_image_segment.display_segmented_image()
```
This is equivalent to `geosolver.diagram.run_diagram.test_parse_image_segments`.

### Parsing primitives from the diagram segment
Primitive parsing is the task of obtaining over-gernerated, noisy primitives from the diagram segment.
For instance, given the diagram segment above, we want to obtain

![primitive parse]
(https://github.com/seominjoon/geosolver/blob/master/images/primitives.png)

To do so:
```python
image_segment_parse = parse_image_segments(open_image(question.diagram_path))
primitive_parse = parse_primitives(image_segment_parse)
selected = select_primitives(primitive_parse)
selected.display_primitives()
```
This is equivalent to `geosolver.diagram.run_diagram.test_parse_primitives`.

## Text parser

## Solver
Location: `geosolver.solver`

Required 3rd-party packages: numpy, scipy

For all the examples, see `geosolver.solver.run_solver`. We will go through its first example here.

### Example 0
*"In triangle ABC, AB = x, BC = 3, CA = 4. Which of the following is a possible value for x? (A) 5  (B) 8"*

To solve this question, we first need to define `geosolver.solver.variable_handler.VariableHandler`:
```python
from geosolver.solver.variable_handler import VariableHandler
vh = VariableHandler()
```

The variable handler allows us to define variables in the (first sentence):
```python
x = vh.number('x')
A = vh.point('A')
B = vh.point('B')
C = vh.point('C')
AB = vh.line(A, B)
BC = vh.line(B, C)
CA = vh.line(C, A)
```
Use `vh.number` to define a numeric variable (with name as argument), `vh.point` to define a point (with name as argument), and `vh.line` to define a line (with two end points as arguments).

Next, we define the relations (information) mentioned in the question (AB = x, BC = 3, CA = 4):
```python
c = vh.apply('LengthOf', AB)
a = vh.apply('LengthOf', BC)
b = vh.apply('LengthOf', CA)
p1 = vh.apply('Equals', a, 3)
p2 = vh.apply('Equals', b, 4)
p3 = vh.apply('Equals', c, x)
```
`p1`, `p2`, and `p3` are the three prior relations in the text.

`geosolver.solver.numeric_solver.NumericSolver` allows us to *reconstruct* the geometry according to the given information:
```python
from geosolver.solver.numeric_solver import NumericSolver
ns = NumericSolver(vh, [p1, p2, p3])
```

`NumericSolver` can analyze whether an input relation is simultaneously satisfiable with the prior relations via `find_assignment` method. It returns a satisfying assignment if they are simultaneously satisfiable, and it returns `None` if not. That is,
```python
q1 = vh.apply('Equals', x, 5)
print(ns.find_assignment(q1))
```
will print out an assignment, and
```python
q2 = vh.apply('Equals', x, 8)
print(ns.find_assignment(q2))
```
will print out `None`.

Note that you can use `q1 = x == 5` instead of `vh.apply('Equals', x, 5)`. Other operators such as <, >, +, *, -, /, ** (power) are supported as well.
Geometric relations, such as *Perpendicular*, *Tangent*, etc., require `vh.apply` to be used. For a complete list of usable relations, refer to `geosolver.ontology.ontology_semantics` (To be updated soon!).

