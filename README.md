# geosolver
geosolver is an end-to-end system that solves high school geometry questions.
That is, its input is question text in natural language and diagram in raster graphics,
and its output is the answer to the question.

geosolver is divided into four parts: diagram praser, text parser, joint parser, and solver.
Text parser transforms the text in natural language into a logical form.
Diagram parser extracts information from the diagram.
Joint parser combines the results of the text parser and the diagram parser and outputs the final logical form.
Solver accepts the logical form from the joint parser and outputs the answer.
This tutorial will first walkthrough each part independently (the modules except the joint parser can be used independently),
and in the last section it will show how to connect them for an end-to-end system.

## Diagram parser

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

