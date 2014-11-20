import string


class Question5_Solver:
  def __init__(self, cpt2):
    self.cpt2 = cpt2
    return

  # |         v
  # Given  z -> y -> x
  # Pr(x|z,y) = self.cpt2.conditional_prob(x, z, y);
  #
  # A word begins with "``" and ends with "``".
  # For example, the probability of word "ab":
  # Pr("ab") = \
  # self.cpt2.conditional_prob("a", "`", "`") * \
  # self.cpt2.conditional_prob("b", "`", "a") * \
  # self.cpt2.conditional_prob("`", "a", "b") * \
  #    self.cpt2.conditional_prob("`", "b", "`");
  # query example:
  #    query: "ques_ion";
  #    return "t";
  def solve(self, query):
    """
    Find most likely letter in blank space of a word

    This is done using the 2nd order CPT and setting the query as a 2nd order
    Markov chain of following form:

    a->b->C->d->e

    where C represent letter in the blank and a,b,d,e, are known letter
    before and after the blank

    CPT2 hold probability of occurring C based on a and b

    e.g.: ques_ion will yield the following chain:
    e->s->C->i->o

    this function compute the probability of each assignments of B from W (W
    is the set of all lowercase characters and `) and returns the letter with
    best likelihood

    :param query: word with single blank; e.g. ques_ion
    :return: a letter to fill the blank; e.g. 't'
    """
    word = "`" + query + "``"
    pos = word.index('_')
    a, b = word[pos - 2], word[pos - 1]
    d, e = word[pos + 1], word[pos + 2]
    likelihood, likelyC = 0.0, "_"
    # shorthand for conditional probability
    P = self.cpt2.conditional_prob
    # find best pair by iterating through all
    for c in string.ascii_lowercase:
      pr = P(c, a, b) * P(d, b, c) * P(e, c, d)
      if pr > likelihood:
        likelihood, likelyC = pr, c
    return likelyC
