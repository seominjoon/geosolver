import sympy
from geosolver.diagram.states import GeneralDiagramParse
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.solver.variable_handler import VariableHandler

__author__ = 'minjoon'



def parse_general_diagram(diagram_parse):
    variable_handler = VariableHandler()
    variables = {'points': {}, 'radii': {}}
    names = {'points': {}, 'radii': {}}
    values = {'points': {}, 'radii': {}}
    intersection_points = {}
    circles = {}
    for key, point in diagram_parse.intersection_points.iteritems():
        name = "point_%d" % key
        point_variable = variable_handler.point(name)
        variables['points'][key] = {}
        values['points'][key] = {}
        x = sympy.symbols("%s_%d_%s" % ('points', key, 'x'))
        y = sympy.symbols("%s_%d_%s" % ('points', key, 'y'))
        variables['points'][key]['x'] = x
        variables['points'][key]['y'] = y
        # variables['points'][key] = point_variable
        values['points'][key]['x'] = point.x
        values['points'][key]['y'] = point.y
        # values['points'][key] = point
        intersection_points[key] = instantiators['point'](x, y)

    for center_key, d in diagram_parse.circles.iteritems():
        variables['radii'][center_key] = {}
        values['radii'][center_key] = {}
        circles[center_key] = {}
        for radius_key, radius in d.iteritems():
            name = "radius_%d_%d" % (center_key, radius_key)
            radius_variable = variable_handler.number(name)
            r = sympy.symbols("%s_%d_%d" % ('radii', center_key, radius_key))
            variables['radii'][center_key][radius_key] = r
            # variables['radii'][center_key][radius_key] = radius_variable
            values['radii'][center_key][radius_key] = radius
            # values['radii'][center_key][radius_key] = radius
            circles[center_key][radius_key] = instantiators['circle'](variables['points'][center_key], r)

    general_diagram_parse = GeneralDiagramParse(diagram_parse, variables, values, intersection_points, circles)
    return general_diagram_parse