from geosolver.text.lexer.string_to_words import string_to_words

__author__ = 'minjoon'


dummy_sentence = "a statement is true".split(' ')

def separate_sentence_and_equations(string):
    """
    separate sentence and equations and

    :param tokens:
    :return:
    """
    words = string_to_words(string)
    sentence = []
    equations = []
    current_equation = []
    flags = [is_operator(word) for word in words]
    neighbor_flags = [is_neighbor(words, flags, idx) for idx, _ in enumerate(words)]
    extended_flags = [is_extended(words, neighbor_flags, idx) for idx, _ in enumerate(words)] # line AB = 5, etc.

    previous_flag = False
    for idx, word in enumerate(words):
        if previous_flag and not extended_flags[idx]:
            """
            Exited equation.
            """
            equations.append(current_equation)
            current_equation = []
            sentence.extend(dummy_sentence)
        if extended_flags[idx]:
            current_equation.append(word)
        else:
            sentence.append(word)
        previous_flag = extended_flags[idx]
    if len(current_equation) > 0:
        equations.append(current_equation)

    return sentence, equations

def is_operator(word):
    if word in "+-*/=><^":
        return True
    return False


def is_neighbor(words, flags, idx):
    if flags[idx]:
        return True
    if idx > 0:
        if flags[idx-1]:
            return True
    if idx < len(words) -1:
        if flags[idx+1]:
            return True
    return False


def is_extended(words, flags, idx):
    if flags[idx]:
        return True
    if idx < len(words) - 1:
        if flags[idx+1] and words[idx] in ['line', 'arc']:
            return True
    return False