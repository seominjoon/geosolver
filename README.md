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

