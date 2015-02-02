__author__ = 'minjoon'


class ImageSegment(object):
    def __init__(self, segmented_image, sliced_image, pixels, offset, key):
        self.sliced_image = sliced_image
        self.segmented_image = segmented_image
        self.pixels = pixels
        self.offset = offset
        self.shape = segmented_image.shape
        self.key = key
        self.area = segmented_image.shape[0] * segmented_image.shape[1]


class ImageSegmentParse(object):
    def __init__(self, original_image, diagram_image_segment, label_image_segments):
        assert isinstance(diagram_image_segment, ImageSegment)
        self.original_image = original_image
        self.diagram_image_segment = diagram_image_segment
        self.label_image_segments = label_image_segments


class PrimitiveParse(object):
    def __init__(self, image_segment_parse, lines, circles):
        self.image_segment_parse = image_segment_parse
        self.lines = lines
        self.circles = circles
        self.primitives = dict(lines.items() + circles.items())


class DiagramParse(object):
    def __init__(self, primitive_parse, intersection_points):
        self.primitive_parse = primitive_parse
        self.intersection_points = intersection_points