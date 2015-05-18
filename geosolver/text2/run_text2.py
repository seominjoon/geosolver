from geosolver.text2.annotation_tree_to_rules import annotation_tree_to_semantic_rules
from geosolver.text2.get_annotation_tree import get_annotation_tree

__author__ = 'minjoon'

if __name__ == "__main__":
    words = {1: '5', 2: 'length', 3: 'good', 4: 'line'}
    tree = get_annotation_tree(words, "Equals@i(LengthOf@2($line@3:5), What@1)")
    syntax_parse = None
    annotation_tree_to_semantic_rules(syntax_parse, tree)
    print tree
