from string import ascii_lowercase

from question3_solver import CrossWordSolver


class Question4_Solver(CrossWordSolver):
  def __init__(self, cpt):
    CrossWordSolver.__init__(self, cpt)
    return

  def solve(self, query):
    """
    Find most likely letter in blank space of intersection of four words, where
    some neighboring letters are also unknown

    This is done using the CPT and setting the query as a graphical model  of
    following form:

    a1->?->C->?->e1
    a2->?->C->?->e2
    a3->?->C->?->e3
    a4->?->C->?->e4

    where C represent letter in the blank intersection and a1,e1...a4,e4 are
    known letters of four words

    the probability of having letter C=c, given a=a followed by two hidden
    letters a->H1->c is given by Sum (P(H1|a)*P(c|H1), for all h=H)
    one and two level of hidden values are pre-computed for this class and is
    accessible via getConditionalProbability function

    for it is intersection of four letter, the probability of C=c is product of
    P(c|ai)*P(ei|bi), for i=[1,4]; here P is probability with hidden
    intermediate variables

    this function compute the probability of each assignments of C from W (W
    is the set of all lowercase characters and `) and returns the letter with
    best likelihood

    :param query: array of four words with single blank and few hidden letters
                  e.g. ["que-_-on", "--_--icial", "in_elligence", "inter--_"]

    :return: a letter to fill the blank in intersection; e.g. 't'
    """
    q1, q2, q3, q4 = query
    P = self.getConditionalProbability

    enumEvidence = CrossWordSolver.enumEvidence
    (a1, h1), (e1, t1) = enumEvidence(q1)
    (a2, h2), (e2, t2) = enumEvidence(q2)
    (a3, h3), (e3, t3) = enumEvidence(q3)
    (a4, h4), (e4, t4) = enumEvidence(q4)

    mxp, likelyC = 0.0, '_'
    for c in ascii_lowercase:
      pr =   P(h1, c, a1) * P(t1, e1, c) \
           * P(h2, c, a2) * P(t2, e2, c) \
           * P(h3, c, a3) * P(t3, e3, c) \
           * P(h4, c, a4) * P(t4, e4, c)
      if pr > mxp:
        mxp, likelyC = pr, c
    return likelyC
