import cv2

from geosolver.diagram.draw_on_image import draw_line, draw_circle, draw_point, draw_instance, draw_label
from geosolver.utils import display_image, save_image


__author__ = 'minjoon'


class ImageSegment(object):
    def __init__(self, segmented_image, sliced_image, binarized_segmented_image, pixels, offset, key):
        self.sliced_image = sliced_image
        self.segmented_image = segmented_image
        self.binarized_segmented_image = binarized_segmented_image
        self.pixels = pixels
        self.offset = offset
        self.shape = segmented_image.shape
        self.key = key
        self.area = segmented_image.shape[0] * segmented_image.shape[1]

    def display_segmented_image(self, block=True):
        display_image(self.segmented_image, block=block)

    def display_binarized_segmented_image(self, block=True):
        display_image(self.binarized_segmented_image, block=block)

    def display_pixels(self, block=True):
        image = cv2.cvtColor(self.segmented_image, cv2.COLOR_GRAY2BGR)
        for pixel in self.pixels:
            draw_point(image, pixel)
        display_image(image, block=block)


class ImageSegmentParse(object):
    def __init__(self, original_image, diagram_image_segment, label_image_segments):
        assert isinstance(diagram_image_segment, ImageSegment)
        self.original_image = original_image
        self.diagram_image_segment = diagram_image_segment
        self.label_image_segments = label_image_segments

    def get_colored_original_image(self):
        return cv2.cvtColor(self.original_image, cv2.COLOR_GRAY2BGR)

    def display_diagram(self):
        self.diagram_image_segment.display_segmented_image()

    def display_labels(self):
        for image_segment in self.label_image_segments.values():
            image_segment.display_segmented_image()

    def get_image_instances(self, instances, **kwargs):
        image = self.get_colored_original_image()
        for instance in instances:
            draw_instance(image, instance, offset=self.diagram_image_segment.offset, **kwargs)
        return image

    def display_instances(self, instances, block=True, **kwargs):
        display_image(self.get_image_instances(instances, **kwargs), block=block)


class PrimitiveParse(object):
    def __init__(self, image_segment_parse, lines, circles):
        assert isinstance(image_segment_parse, ImageSegmentParse)
        self.image_segment_parse = image_segment_parse
        self.lines = lines
        self.circles = circles
        self.primitives = dict(lines.items() + circles.items())

    def display_primitives(self, block=True, **kwargs):
        self.image_segment_parse.display_instances(self.primitives.values(), block=block, **kwargs)

    def get_image_primitives(self, **kwargs):
        return self.image_segment_parse.get_image_instances(self.primitives.values(), **kwargs)

    def display_each_primitive(self, **kwargs):
        for primitive in self.primitives.values():
            self.image_segment_parse.display_instances([primitive], block=True, **kwargs)


class CoreParse(object):
    def __init__(self, primitive_parse, intersection_points, point_variables, circles, radius_variables):
        assert isinstance(primitive_parse, PrimitiveParse)
        self.image_segment_parse = primitive_parse.image_segment_parse
        self.primitive_parse = primitive_parse
        self.intersection_points = intersection_points
        self.circles = circles
        self.point_variables = point_variables
        self.radius_variables = radius_variables

    def get_image_points(self, **kwargs):
        image = self.image_segment_parse.get_colored_original_image()
        offset = self.image_segment_parse.diagram_image_segment.offset
        for key, point in self.intersection_points.iteritems():
            label = Label("%d" % key, point)
            draw_label(image, label, offset=offset, **kwargs)
            draw_point(image, point, offset=offset, **kwargs)
        return image

    def display_points(self, block=True, **kwargs):
        image = self.get_image_points(**kwargs)
        display_image(image, block=block)


class GraphParse(object):
    # TODO :
    def __init__(self, diagram_parse, line_graph, circle_dict, arc_graphs):
        assert isinstance(diagram_parse, CoreParse)
        self.diagram_parse = diagram_parse
        self.primitive_parse = diagram_parse.primitive_parse
        self.image_segment_parse = diagram_parse.primitive_parse.image_segment_parse
        self.line_graph = line_graph  # Undirected graph
        self.circle_dict = circle_dict
        self.arc_graphs = arc_graphs  # Directed graph
        self.intersection_points = diagram_parse.intersection_points
        self.point_variables = diagram_parse.point_variables
        self.radius_variables = diagram_parse.radius_variables

    def display_instances(self, instances, block=True, **kwargs):
        self.image_segment_parse.display_instances(instances, block=block, **kwargs)


class GeneralDiagramParse(CoreParse):
    def __init__(self, diagram_parse, variables, values, intersection_points, circles):
        """
        :param diagram_parse:
        :param intersection_points:
        :param circles:
        :param variables: {'points': {1: {'x': symbol('p_1_x') 'y': symbol('p_1_y')}}, 'radii': {1: {0: symbol('r_1_0')}}}
        :return:
        """
        assert isinstance(diagram_parse, CoreParse)
        self.diagram_parse = diagram_parse
        self.intersection_points = intersection_points
        self.circles = circles
        self.variables = variables
        self.values = values


class GeneralGraphParse(GraphParse):
    def __init__(self, general_diagram_parse, graph_parse, line_graph, circle_dict, arc_graphs):
        assert isinstance(general_diagram_parse, GeneralDiagramParse)
        assert isinstance(graph_parse, GraphParse)
        self.general_diagram_parse = general_diagram_parse
        self.graph_parse = graph_parse
        self.line_graph = line_graph
        self.circle_dict = circle_dict
        self.arc_graphs = arc_graphs
        self.intersection_points = general_diagram_parse.intersection_points


class Label:
    def __init__(self, text, position):
        self.text = text
        self.position = position


class ImageLabelParse:
    def __init__(self, image, labels):
        self.image = image
        self.labels = labels

    def get_labeled_image(self, **kwargs):
        image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        for label in self.labels.values():
            draw_label(image, label, **kwargs)
            draw_point(image, label.position)
        return image