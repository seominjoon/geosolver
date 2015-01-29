__author__ = 'minjoon'


def normalize_truths(truths):
    """
    Returns a list of normalized equations obtained from expression and sigma of each truth.
    "normalized" means:
    Suppose the truth a has expression abs(a - b), which effectively means the equality of a and b.
    Suppose a and b are 1000, 1001, respectively. Then they are only 0.1% different, but abs(a-b) = 1.
    If a and b are 0.1 and 0.2, then they are 100%  different but abs(a-b) = 0.1
    So abs(a-b) means differently, depending on sigma value (thus truth has sigma value).
    But the algebraic solver is ignorant of this fact. So the equation needs to be scaled accordingly,
    ex. expression/sigma.

    :param truths:
    :return:
    """
