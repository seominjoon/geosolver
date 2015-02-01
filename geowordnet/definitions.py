"""
Definitions of GeoWordNet.

GeoWordNet package attempts to imitate the well-known WordNet.
We cannot use WordNet directly because WordNet doesn't have most keywords appearing in geometry questions,
and here the domain is more specific that we can encode more domain-specific information this way.


How to encode definitions:
(% denotes optional parameter)
Ex. {'lemma': 'radius', 'pos': 'noun', 'lexemes': ['isRadiusOf', 'radiusOf'], %'forms': {'adj': 'radial'}%}

By adding forms, you are copying lexemes and lemma and just replacing 'pos'.
If you don't want this, you have to define a separate entry for that form.

Although geowordnet is self-contained, you can specify lexeme to equal to symbol in ontology.
That is, you are inferring the meaning of lemma from the ontology.

In order to induce synonyms, you have to create an entry for that synonym.
For instance, if we want 'equal' and 'same' as synonyms,
then encode:

{'lemma': 'equal', 'pos': 'adj', 'lexemes': ['isEqualTo']}
{'lemma': 'same', 'pos': 'adj', 'lexemes': ['isEqualTo']}

The geowordnet object will automatically induce synset between 'equal' and 'same' when loading.
If you do not define a lemma for any symbol in definitions, the symbol cannot be reached by text.
"""
__author__ = 'minjoon'

attributes = ['lemma', 'pos', 'lexemes']
pos_types = ['noun', 'adj', 'verb', 'noun:plural', 'verb:3rd', 'preposition']

entries = [
    # operators
    {'lemma': 'add', 'pos': 'verb', 'lexemes': ['add']},
    {'lemma': 'subtract', 'pos': 'verb', 'lexemes': ['sub']},
    {'lemma': 'multiply', 'pos': 'verb', 'lexemes': ['mul']},
    {'lemma': 'divide', 'pos': 'verb', 'lexemes': ['div']},
    {'lemma': 'power', 'pos': 'noun', 'lexemes': ['pow']},
    {'lemma': 'equal', 'pos': 'adj', 'lexemes': ['equal'],
     'forms': {'verb': 'equal'}},
    {'lemma': 'greater', 'pos': 'adj', 'lexemes': ['greater']},
    {'lemma': 'less', 'pos': 'adj', 'lexemes': ['less']},

    # functions mapping to number
    {'lemma': 'length', 'pos': 'noun', 'lexemes': ['lengthOf']},
    {'lemma': 'angle', 'pos': 'noun', 'lexemes': ['angleOf_angle', 'angleOf_arc', 'angle']},
    {'lemma': 'radius', 'pos': 'noun', 'lexemes': ['isRadiusOf', 'radiusOf'],
     'forms': {'noun:plural': 'radii', 'adj': 'radial'}},
    {'lemma': 'diameter', 'pos': 'noun', 'lexemes': ['isDiameterOf', 'diameterOf']},
    {'lemma': 'area', 'pos': 'noun', 'lexemes': ['areaOf_polygon', 'areaOf_circle']},
    {'lemma': 'perimeter', 'pos': 'noun', 'lexemes': ['perimeterOf']},
    {'lemma': 'circumference', 'pos': 'noun', 'lexemes': ['circumferenceOf']},

    # functions mapping to entities
    {'lemma': 'point', 'pos': 'noun', 'lexemes': ['point']},
    {'lemma': 'line', 'pos': 'noun', 'lexemes': ['line']},
    {'lemma': 'arc', 'pos': 'noun', 'lexemes': ['arc']},
    {'lemma': 'circle', 'pos': 'noun', 'lexemes': ['circle']},
    {'lemma': 'triangle', 'pos': 'noun', 'lexemes': ['triangle']},
    {'lemma': 'quadrilateral', 'pos': 'noun', 'lexemes': ['quadrilateral']},

    # functions mapping to truth values (predicates)
    {'lemma': 'intersect', 'pos': 'verb', 'lexemes': ['intersects']},
    {'lemma': 'on', 'pos': 'preposition', 'lexemes': ['isOn']},
    {'lemma': 'midpoint', 'pos': 'noun', 'lexemes': ['isMidpointOf']},
    {'lemma': 'parallel', 'pos': 'adj', 'lexemes': ['isParallelWith']},
    {'lemma': 'perpendicular', 'pos': 'adj', 'lexemes': ['isPerpendicularTo']},
    {'lemma': 'bisect', 'pos': 'verb', 'lexemes': ['bisects_line', 'bisects_angle'],
     'forms': {'noun': 'bisector'}},
    {'lemma': 'right', 'pos': 'adj', 'lexemes': ['isRightAngle', 'isRightTriangle']},
    {'lemma': 'hypotenuse', 'pos': 'noun', 'lexemes': ['isHypotenuseOf']},
    {'lemma': 'median', 'pos': 'noun', 'lexemes': ['isMedianOf']},
    {'lemma': 'altitude', 'pos': 'noun', 'lexemes': ['isAltitudeOf']},
    {'lemma': 'isosceles', 'pos': 'adj', 'lexemes': ['isIsosceles']},
    {'lemma': 'equilateral', 'pos': 'adj', 'lexemes': ['isEquilateral']},
    {'lemma': 'parallelogram', 'pos': 'noun', 'lexemes': ['isParallelogram']},
    {'lemma': 'rhombus', 'pos': 'noun', 'lexemes': ['isRhombus']},
    {'lemma': 'rectangle', 'pos': 'noun', 'lexemes': ['isRectangle']},
    {'lemma': 'square', 'pos': 'noun', 'lexemes': ['isSquare']},
    {'lemma': 'chord', 'pos': 'noun', 'lexemes': ['isChordOf']},
    {'lemma': 'tangent', 'pos': 'noun', 'lexemes': ['isTangentOf']},
    {'lemma': 'secant', 'pos': 'noun', 'lexemes': ['isSecantOf']},

    # unknown mapping
    {'lemma': 'what', 'pos': 'noun', 'lexemes': ['uNumber']},
    {'lemma': 'find', 'pos': 'verb', 'lexemes': ['uNumber']},
    {'lemma': 'which', 'pos': 'noun', 'lexemes': ['uNumber', 'uTruth']},
]

# enumerate different forms
new_entries = []
for entry in entries:
    if 'forms' in entry:
        for pos, lemma in entry['forms'].iteritems():
            new_entry = {'lemma': lemma, 'pos': pos, 'lexemes': entry['lexemes']}
            new_entries.append(new_entry)
    new_entries.append(entry)

entries = new_entries