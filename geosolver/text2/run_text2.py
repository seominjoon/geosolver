from geosolver.text2.annotation_tree_to_rules import annotation_tree_to_semantic_rules, annotation_tree_to_tag_rules
from geosolver.text2.get_annotation_tree import get_annotation_tree
from geosolver.text2.syntax_parser import SyntaxParse

__author__ = 'minjoon'

if __name__ == "__main__":
    words = {1: '5', 2: 'length', 3: 'good', 4: 'line'}
    syntax_parse = SyntaxParse(words, None)
    tree = get_annotation_tree(syntax_parse, "Is@i(IntersectionOf@1($l@1, $k@2), $Q@3)")
    print annotation_tree_to_tag_rules(syntax_parse, tree)
    print annotation_tree_to_semantic_rules(syntax_parse, tree)
