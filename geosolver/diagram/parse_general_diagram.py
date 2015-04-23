import sympy
from geosolver.diagram.states import GeneralDiagramParse
from geosolver.ontology.instantiator_definitions import instantiators

__author__ = 'minjoon'



def parse_general_diagram(diagram_parse):
    variables = {'points': {}, 'radii': {}}
    values = {'points': {}, 'radii': {}}
    intersection_points = {}
    circles = {}
    for key, point in diagram_parse.intersection_points.iteritems():
        variables['points'][key] = {}
        values['points'][key] = {}
        x = sympy.symbols("%s_%d_%s" % ('points', key, 'x'))
        y = sympy.symbols("%s_%d_%s" % ('points', key, 'y'))
        variables['points'][key]['x'] = x
        variables['points'][key]['y'] = y
        values['points'][key]['x'] = point.x
        values['points'][key]['y'] = point.y
        intersection_points[key] = instantiators['point'](x, y)

    for center_key, d in diagram_parse.circles.iteritems():
        variables['radii'][center_key] = {}
        values['radii'][center_key] = {}
        circles[center_key] = {}
        for radius_key, radius in d.iteritems():
            r = sympy.symbols("%s_%d_%d" % ('radii', center_key, radius_key))
            variables['radii'][center_key][radius_key] = r
            values['radii'][center_key][radius_key] = radius
            circles[center_key][radius_key] = instantiators['circle'](variables['points'][center_key], r)

    general_diagram_parse = GeneralDiagramParse(diagram_parse, variables, values, intersection_points, circles)
    return general_diagram_parse