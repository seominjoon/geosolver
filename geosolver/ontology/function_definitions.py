import sympy
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.ontology.states import Truth
import itertools
# from bokeh._glyph_functions import line

__author__ = 'minjoon'

def and_(truth0, truth1):
    """
    TODO: include t.sigma
    """
    truth0.expression = sympy.sympify(truth0.expression)
    truth1.expression = sympy.sympify(truth1.expression)
    exp = sympy.Max(truth0.expression, truth1.expression)
    sig = sympy.Max(truth0.sigma, truth1.sigma)
    return Truth(exp, sig)

def or_(truth0, truth1):
    exp = sympy.Min(truth0.expression, truth1.expression)
    sig = sympy.Max(truth0.sigma, truth1.sigma)
    return Truth(exp, sig)

def not_(truth):
    return Truth(-truth.expression, truth.sigma)

def add(number0, number1):
    return number0 + number1


def sub(number0, number1):
    return number0 - number1


def mul(number0, number1):
    return number0 * number1


def div(number0, number1):
    return number0 / number1


def pow(number0, number1):
    return number0 ** number1


def equal(number0, number1):
    expr = abs(number0 - number1)
    sig = abs(number0 + number1) / 2
    return Truth(expr, sig)


def greater(number0, number1):
    expr = number1 - number0
    sig = abs(number0 + number1) / 2
    return Truth(expr, sig)


def less(number0, number1):
    expr = number0 - number1
    sig = abs(number0 + number1) / 2
    return Truth(expr, sig)


def lengthOf(line):
    return sympy.sqrt((line.a.x-line.b.x)**2 + (line.a.y-line.b.y)**2)


def angleOf_angle(angle):
    a = lengthOf(instantiators['line'](angle.b, angle.c))
    b = lengthOf(instantiators['line'](angle.c, angle.a))
    c = lengthOf(instantiators['line'](angle.a, angle.b))
    return sympy.acos((a**2 + c**2 - b**2) / (2*a*c))


def angleOf_arc(arc):
    angle = instantiators['angle'](arc.a, arc.circle.center, arc.b)
    return angleOf_angle(angle)


def radiusOf(circle):
    return circle.radius


def diameterOf(circle):
    return 2 * circle.radius


# Baiscally Bubble Sorting Values, but since they're equations it gets a little funky
# essentially the max and min get floated to the top and bottom respectively
# then we repeat this for the second most and so forth.
def sort(fs):
    fs = list(fs)
    for i in range(len(fs)-1,-1,-1):
        for j in range(i,-1,-1):
            Fi = fs[i]
            Fj = fs[j]
            fs[j] = sympy.Min(Fi,Fj)
            fs[i] = sympy.Max(Fi,Fj)
    return fs

#Sort then make a piecewise function where we test if the key is being used currently
#with that function, then when it is there map it to the value corresponding to that
#equation. It's pretty funky and gets slow when there are things that are unnknowable
#how they compare in advance (which should hopefully not be too big of a problem, since
#this only has to be generated once). Handles dealing with iterable objects dividing the
#equations into each individual value. 
#
def sortByKey(fsDict,cls=tuple):
    try:
        lenTot = len(fsDict[fsDict.keys()[0]])
    except:
        lenTot = None
    fs = sort(fsDict.keys())
    result = []
    if lenTot == None:
        for f in fs:
            pieces = []
            for (F,v) in fsDict.items():
                pieces.append((v, f == F))
            result.append(sympy.Piecewise(*pieces))
    else:
        for f in fs:
            pieces = []
            for i in range(lenTot):
                parts = []
                for (F,v) in fsDict.items():
                    parts.append((v[i], sympy.Abs(f - F) <= 0))
                pieces.append(sympy.Piecewise(*parts))
            result.append(cls(*pieces))
    return result

def sortPointsClockwise(poly):
    center = tuple(sum(x) for x in zip(*poly))
    centerX, centerY = (center[0]/len(poly), center[1]/len(poly))
    angle = lambda (x1,y1): sympy.atan2(y1 - centerY, x1 - centerX)
    angles = {angle(p) : p for p in poly}
    return sortByKey(angles,instantiators['point'])

def areaOf_polygon(poly):
    poly = sortPointsClockwise(poly)
    return 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in zip(poly, poly[1:] + poly[:1])))


def areaOf_circle(circle):
    return sympy.pi * circle.radius**2


def perimeterOf(polygon):
    lines = [instantiators['line'](polygon[idx-1], polygon[idx]) for idx in len(polygon)]
    return sum(lengthOf(line) for line in lines)


def circumferenceOf(circle):
    return 2 * sympy.pi * circle.radius


def intercept(line0,line1):
    s0 = slope(*line0)
    s1 = slope(*line1)
    xint = (s0*line0[0][0] - s1*line1[0][0] - line0[0][1] + line1[0][1]) / (s0 - s1)
    if xint == sympy.S("zoo") or xint == sympy.S("oo"):
        return False
    yint = (line0[0][0] - xint) * s0 + line0[0][1]
    return instantiators['point'](xint,yint)

def perpindicularIntercept(line, point):
    m = slope(*line)
    ox,oy = point
    (x1,y1),_ = line
    x = (m**2 * x1 + m*oy - m * y1 + ox)/(m**2 + 1)
    y = (-1/m) * (x - ox) + oy
    perpInt = instantiators['point'](x,y)
    return instantiators['line'](entity1.center, perpInt)

def intersects(entity0, entity1):
    if isinstance(entity0, instantiators['line']) and isinstance(entity1, instantiators['line']):
        p = intercept(entity0, entity1)
        if not p:
            return not_(equal(s0,s1))
        return and_(not_(equal(s0, s1)),
                    and_(isOn(p, entity0),
                         isOn(p, entity1)))
    elif isinstance(entity0, instantiators['circle']) and isinstance(entity1, instantiators['circle']):
        dist = lengthOf(instantiators['line'](entity0.center, entity1.center))
        return less(dist, entity0.radius + entity1.radius)
    elif isinstance(entity0, ['circle']):
        return intersects(entity1, entity0)
    perpLine = perpindicularIntercept(entity0, entity1.center)
    return less(lengthOf(perpLine), entity1.radius)
                         

def slope((x1,y1),(x2,y2)):
    return (x1 - x2)/(y1 - y2)

def isOn(point, entity):
    if isinstance(entity, instantiators['line']):
        ang = angleOf_angle(instantiators['angle'](entity[0],point,entity[1]))
        betweenX = or_(and_(less(entity[0].x, point.x), less(point.x, entity[1].x)),
                       and_(less(entity[1].x, point.x), less(point.x, entity[0].x)))
        betweenY = or_(and_(less(entity[0].y, point.y), less(point.y, entity[1].y)),
                       and_(less(entity[1].y, point.y), less(point.y, entity[0].y)))
        return and_(and_(equal(ang, 0), betweenX), betweenY)
    elif isinstance(entity, instantiators['circle']):
        return equal(lengthOf(instantiators['line'](entity.center, point)), entity.radius)


def isMidpointOf(point, line):
    a = lengthOf(instantiators['line'](line.a, point))
    b = lengthOf(instantiators['line'](point, line.b))
    return equal(a, b)

def isParallelWith(line0,line1):
    return equals(slope(*line0), slope(*line1))

def isPerpendicularTo(line0, line1):
    s0 = slope(*line0)
    perpSlope = 1 / (-s0)
    return equals(perpSlope, slope(*line1))

def bisects_line(line0, line1):
    int = intercept(line0, line1)
    if not int:
        #TODO: something real
        return Truth(-1000,0)
    subline0 = instantiators['line'](line0[0],int)
    subline1 = instantiators['line'](int,line0[1])
    return equal(lengthOf(subline0), lengthOf(subline1))
def bisects_angle(line, angle):
    pass
def isRightAngle(angle):
    ang = angleOf_angle(angle)
    return equal(sympy.re(angleOf_angle(angle)), sympy.pi / 2)
def nInARow(l,n):
    dl = list(itertools.chain(l,l))
    return [dl[i:i+n] for i in xrange(len(l))]
def isHypotenuseOf(line, triangle):
    pass
def isMedianOf(line, triangle):
    pass
def isAltitudeOf(line, triangle):
    pass
def isIsosceles(tri):
    lines = itertools.combinations(tri, 2)
    line_lengths = map(lambda l: lengthOf(instantiators['line'](l)), lines)
    line_length_pairs = itertools.combinations(line_lengths, 2)
    return reduce(lambda prior, n: n if not prior else or_(prior, n),
                  map(lambda lengths: equal(*lengths),line_length_pairs),
                  False)
    
def isRightTriangle(tri):
    angles = map(lambda order: isRightAngle(instantiators['angle'](*order)), nInARow(tri, 3))
    return reduce(lambda prev, n: n if not prev else or_(prev, n),
                  angles,
                  False)
    
def isEquilateral(tri):
    is60Deg = lambda ordering: equal(angleOf_angle(instantiators['angle'](ordering)), sympy.pi / 3)
    return reduce(lambda prev, n: n if not prev else and_(prev, n),
                  map(is60Deg, nInARow(tri, 3)),
                  False)
def isParallelogram(quad):
    quad = sortPointsClockwise(quad)
    lines = zip(quad, quad[1:] + quad[:1])
    lengths = map(lambda line: lengthOf(instantiators['line'](line)), lines)
    return and_(equal(lengths[0], lengths[2]),
                equal(lengths[1], lengths[3]))
def isRhombus(quad):
    quad = sortPointsClockwise(quad)
    lines = zip(quad, quad[1:] + quad[:1])
    lengths = map(lambda line: lengthOf(instantiators['line'](*line)), lines)
    return and_(equal(lengths[0], lengths[1]),
                and_(equal(lengths[0], lengths[2]),
                     equal(lengths[1], lengths[3])))
def isRectangle(quad):
    quad = sortPointsClockwise(quad)
    is90Deg = lambda ordering: isRightAngle(instantiators['angle'](*ordering))
    return reduce(lambda prev, n: n if not prev else and_(prev, n),
                  map(is90Deg, nInARow(quad, 3)),
                  False)
def isSquare(quad):
    return and_(isRectangle(quad), isRhombus(quad))

def isRadiusOf(line, circle):
    distFromCenterA = lengthOf(instantiators['line'](line[0], circle.center))
    distFromCenterB = lengthOf(instantiators['line'](line[1], circle.center))
    return and_(equal(lengthOf(line), circle.radius),
                or_(equal(distFromCenterA, 0),
                    equal(distFromCenterB, 0)))
def isDiameterOf(line, circle):
    return and_(isMidpointOf(circle.center, line),
                equal(diameterOf(circle), lengthOf(line)))
def isChordOf(line, circle):
    return and_(isOn(line[0], circle),
                isOn(line[1], circle))
                           
def isTangentOf(line, circle):
    line0 = instantiators['line'](line[0], circle.center)
    line1 = instantiators['line'](line[1], circle.center)
    return and_(equal(lengthOf(perpindicularIntercept(line, circle.center))),
                and_(greater(lengthOf(line0), circle.radius),
                     greater(lengthOf(line1), circle.radius)))
                       
def isSecantOf(line, circle):
    line0 = instantiators['line'](line[0], circle.center)
    line1 = instantiators['line'](line[1], circle.center)
    return and_(not_(equal(lengthOf(perpindicularIntercept(line, circle.center)),
                           circle.radius)),
                and_(intersects(line, circle),
                     and_(greater(lengthOf(line0), circle.radius),
                          greater(lengthOf(line1), circle.radius))))
                
# And so on...
#p = instantiators['point'](sympy.S('x+0.5'),sympy.S('y+0.6'))
#l = instantiators['line'](instantiators['point'](sympy.S('x'),sympy.S('y')), instantiators['point'](sympy.S('x+1'),sympy.S('y+1')))
#print((isOn(p,l).expression).evalf())
x = sympy.S('x')
y = sympy.S('y')
z = sympy.S('z')

a = instantiators['point'](x,y)
b = instantiators['point'](x+2,y+2)
c = instantiators['point'](x,y+2)
d = instantiators['point'](z,y)
# 
print(isSquare(instantiators['quadrilateral'](a,b,c,d)).expression.evalf())