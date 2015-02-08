import cv2

from geosolver.diagram.draw_on_image import draw_line, draw_circle, draw_point, draw_instance, draw_label
from geosolver.utils import display_image


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

    def display_instances(self, instances, block=True, **kwargs):
        image = self.get_colored_original_image()
        for instance in instances:
            draw_instance(image, instance, offset=self.diagram_image_segment.offset, **kwargs)
        display_image(image, block=block)



class PrimitiveParse(object):
    def __init__(self, image_segment_parse, lines, circles):
        assert isinstance(image_segment_parse, ImageSegmentParse)
        self.image_segment_parse = image_segment_parse
        self.lines = lines
        self.circles = circles
        self.primitives = dict(lines.items() + circles.items())

    def display_primitives(self, block=True, **kwargs):
        self.image_segment_parse.display_instances(self.primitives.values(), block=block, **kwargs)

    def display_each_primitive(self, **kwargs):
        for primitive in self.primitives.values():
            self.image_segment_parse.display_instances([primitive], block=True, **kwargs)


class DiagramParse(object):
    def __init__(self, primitive_parse, intersection_points):
        assert isinstance(primitive_parse, PrimitiveParse)
        self.image_segment_parse = primitive_parse.image_segment_parse
        self.primitive_parse = primitive_parse
        self.intersection_points = intersection_points

    def display_points(self, block=True, **kwargs):
        image = self.image_segment_parse.get_colored_original_image()
        offset = self.image_segment_parse.diagram_image_segment.offset
        for key, point in self.intersection_points.iteritems():
            label = Label("%d" % key, point)
            draw_label(image, label, offset=offset, **kwargs)
            draw_point(image, point, offset=offset, **kwargs)
        display_image(image, block=block)



class GraphParse(object):
    # TODO :
    def __init__(self, diagram_parse, line_graph, circle_dict, arc_graphs):
        assert isinstance(diagram_parse, DiagramParse)
        self.diagram_parse = diagram_parse
        self.primitive_parse = diagram_parse.primitive_parse
        self.image_segment_parse = diagram_parse.primitive_parse.image_segment_parse
        self.line_graph = line_graph  # Undirected graph
        self.circle_dict = circle_dict
        self.arc_graphs = arc_graphs  # Directed graph

    def display_instances(self, instances, block=True, **kwargs):
        self.image_segment_parse.display_instances(instances, block=block, **kwargs)

class Label:
    def __init__(self, text, position):
        self.text = text
        self.position = position
