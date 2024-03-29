from string import ascii_lowercase


def ind(c):
  return ord(c) - 96


class CrossWordSolver:
  @staticmethod
  def enumEvidence(word):
    word = "`" + word + "`"
    pos = word.index("_")
    head, tail = word[:pos], word[pos + 1:]
    tail = tail[::-1]
    return CrossWordSolver.marginalLetter(head), \
           CrossWordSolver.marginalLetter(tail)

  @staticmethod
  def marginalLetter(phrase):
    n = len(phrase)
    phrase += "-"
    pos = phrase.index("-")
    # print phrase, phrase[pos-1],n, pos
    return phrase[pos - 1], (n - pos)


  def __init__(self, cpt):
    """
    :param cpt: First order Conditional Probability Table
    """
    self.cpt = cpt
    self.cpt1 = [[0.0] * 27 for i in range(27)]
    self.cpt2 = [[0.0] * 27 for i in range(27)]
    self.computeIntermediateProbabilities()
    # self.print_cpTable(self.cpt1)
    # self.print_cpTable(self.cpt2)


  def cp1(self, c, a):
    """
    conditional probability after eliminating one hidden variable
    ref: following Markov chain
    a->?->c
    :param c:
    :param a:
    :return:
    """
    return self.cpt1[ind(a)][ind(c)]

  def cp2(self, d, a):
    """
    conditional probability after eliminating two hidden variable
    ref: following Markov chain
    a->?->?->c
    :param d:
    :param a:
    :return:
    """
    return self.cpt2[ind(a)][ind(d)]


  def computeIntermediateProbabilities(self):
    """
    compute CPT1 and CPT2, for conditional probabilities with one and two hidden
    variables eliminated
    """
    letters = "`" + ascii_lowercase
    P = self.cpt.conditional_prob

    for a in letters:
      total = 0.0
      for c in letters:
        sum1 = 0.0
        for B in ascii_lowercase:
          sum1 += 0.0 if a==B and B==c else (P(B, a) * P(c, B))
        self.cpt1[ind(a)][ind(c)] = sum1
        total += sum1
      for c in letters:
        self.cpt1[ind(a)][ind(c)] /= total

    for a in letters:
      total = 0.0
      for d in letters:
        sum2 = 0.0
        for C in ascii_lowercase:
          sum2 += self.cp1(C, a) * P(d, C)
        self.cpt2[ind(a)][ind(d)] = 1.0 * sum2
        total += sum2
      for d in letters:
        self.cpt2[ind(a)][ind(d)] /= total


  def getConditionalProbability(self, numberOfHiddenVariables, v, given):
    """
    get CPT (0,1,2) based on number of hidden variables
    :param numberOfHiddenVariables: number of eliminated hidden variables
    :param v: estimating value
    :param given: given that
    :return: conditional probability
    """
    if numberOfHiddenVariables==0:
      return self.cpt.cpt[ind(given)][ind(v)]
    elif numberOfHiddenVariables==1:
      return self.cpt1[ind(given)][ind(v)]
    elif numberOfHiddenVariables==2:
      return self.cpt2[ind(given)][ind(v)]

  def print_cpTable(self, table):
    print "%     `    a    b    c    d    e    f    " \
          "g    h    i    j    k    l    m    n    " \
          "o    p    q    r    s    t    u    v    w    x    y    z"
    print "===========================================" \
          "===========================================" \
          "===================================================="
    print "`", "|", "|".join(
      str("%.1f" % (p * 100)).rjust(4, ' ') for p in table[0])
    for i in range(1, 27):
      print chr(i + 96), "|", \
        "|".join(str("%.1f" % (p * 100)).rjust(4, ' ') for p in table[i])
    for i in range(0, 27):
      s = sum(table[i])
      if abs(s - 1.0) > 0.01:
        print "[ERROR] The conditional probability of Pr(*|%s) " \
              "does not add up to 1 (actual: %f)." % (chr(i + 96), s)


class Question3_Solver(CrossWordSolver):
  def __init__(self, cpt):
    CrossWordSolver.__init__(self, cpt)
    return


  def solve(self, query):
    """
    Find most likely letter in blank space of a word, where some neighboring
    letters are also unknown

    This is done using the CPT and setting the query as a Markov chain of
    following form:

    a->?->C->?->e

    where C represent letter in the blank and a and e are known letters
    there are zero, one or more hidden letters between a and C, same for e

    e.g.: qu--_--n will yield the following chain:
    u->??->C->??->n

    here the level of indirection between a='u' and C is 2, we call it h
    similarly t for C and e

    the probability of having letter C=c, given a=a followed by two hidden
    letters a->H1->c is given by Sum (P(H1|a)*P(c|H1), for all h=H)
    one and two level of hidden values are pre-computed for this class and is
    accessible via getConditionalProbability function

    this function compute the probability of each assignments of C from W (W
    is the set of all lowercase characters and `) and returns the letter with
    best likelihood

    :param query: word with single blank and few hidden letter; e.g. qu--_--n
    :return: a letter to fill the blank; e.g. 't'
    """
    (a, h), (e, t) = CrossWordSolver.enumEvidence(query)
    likelihood, likelyC = 0.0, "_"
    P = self.getConditionalProbability
    for c in ascii_lowercase:
      p = P(h, c, a) * P(t, e, c)
      if p > likelihood:
        likelihood, likelyC = p, c
    # print query, letter, l1, h1, l2, h2
    return likelyC
