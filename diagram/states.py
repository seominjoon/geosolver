import cv2
from geosolver.diagram.utils import draw_line, draw_circle
from geosolver.utils import block_display

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
        cv2.imshow("", self.segmented_image)
        if block:
            block_display()


class ImageSegmentParse(object):
    def __init__(self, original_image, diagram_image_segment, label_image_segments):
        assert isinstance(diagram_image_segment, ImageSegment)
        self.original_image = original_image
        self.diagram_image_segment = diagram_image_segment
        self.label_image_segments = label_image_segments

    def display_diagram(self):
        self.diagram_image_segment.display_segmented_image()

    def display_labels(self):
        for image_segment in self.label_image_segments.values():
            image_segment.display_segmented_image()


class PrimitiveParse(object):
    def __init__(self, image_segment_parse, lines, circles):
        self.image_segment_parse = image_segment_parse
        self.lines = lines
        self.circles = circles
        self.primitives = dict(lines.items() + circles.items())

    def display_primitives(self, block=True):
        image = cv2.cvtColor(self.image_segment_parse.original_image,
                             cv2.COLOR_GRAY2BGR)
        offset = self.image_segment_parse.diagram_image_segment.offset
        for line in self.lines.values():
            draw_line(image, line, offset=offset)
        for circle in self.circles.values():
            draw_circle(image, circle, offset=offset)
        cv2.imshow("", image)
        if block:
            block_display()


class DiagramParse(object):
    def __init__(self, primitive_parse, intersection_points):
        self.primitive_parse = primitive_parse
        self.intersection_points = intersection_points