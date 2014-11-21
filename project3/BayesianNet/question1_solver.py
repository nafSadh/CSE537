class Question1_Solver:
  def __init__(self, cpt):
    self.cpt = cpt
    return

  # ####################################
  # ADD YOUR CODE HERE
  # Pr(x|y) = self.cpt.conditional_prob(x, y);
  # A word begins with "`" and ends with "`".
  # For example, the probability of word "ab":
  # Pr("ab") = \
  #    self.cpt.conditional_prob("a", "`") * \
  #    self.cpt.conditional_prob("b", "a") * \
  #    self.cpt.conditional_prob("`", "b");
  # query example:
  #    query: "ques_ion";
  #    return "t";
  def solve(self, query):
    """
    Find most likely letter in blank space of a word

    This is done using the CPT and setting the query as a Markov chain of
    following form:

    a->B->c

    where B represent letter in the blank and a and c are known letter before
    and after the blank

    e.g.: ques_ion will yield the following chain:
    s->B->i

    this function compute the probability of each assignments of B from W (W
    is the set of all lowercase characters and `) and returns the letter with
    best likelihood

    :param query: word with single blank; e.g. ques_ion
    :return: a letter to fill the blank; e.g. 't'
    """
    word = "`" + query + "`"
    pos = word.index('_')
    likelihood, a, c = 0.0, word[pos - 1], word[pos + 1]
    likelyB = "_"
    # shorthand for conditional probability
    P = self.cpt.conditional_prob
    # find best pair by iterating through all
    from string import ascii_lowercase

    for b in ascii_lowercase:
      p = P(b, a) * P(c, b)
      if p > likelihood:
        likelihood, likelyB = p, b
    return likelyB


