class Question2_Solver:
    def __init__(self, cpt):
      self.cpt = cpt

    #####################################
    # ADD YOUR CODE HERE
    # Pr(x|y) = self.cpt.conditional_prob(x, y);
    # A word begins with "`" and ends with "`".
    # For example, the probability of word "ab":
    # Pr("ab") = \
    #    self.cpt.conditional_prob("a", "`") * \
    #    self.cpt.conditional_prob("b", "a") * \
    #    self.cpt.conditional_prob("`", "b");
    # query example:
    #    query: "que__ion";
    #    return ["s", "t"];

    def solve(self, query):
      """
      Find most likely letter in blank spaces of a word

      This is done using the CPT and setting the query as a Markov chain of
      following form:

      a->B->C->d

      where B and C represent letters in the blanks and a and d are known letter
      before and after the pair of blanks

      e.g.: que__ion will yield the following chain:
      e->B->C->i

      this function compute the probability of each assignments of (B,C) from
      WxW (W is the set of all lowercase characters and `) and returns the pair
      with best likelihood

      :param query: word with two blanks; e.g. que__ion
      :return: list of two letter to fill the blanks; e.g. ['s','t']
      """
      word = "`"+query+"`"
      pos = word.index("__")
      likelihood, a, d  = 0.0, word[pos-1], word[pos+2]
      likelyB, likelyC ="_","_"
      # shorthand for conditional probability
      P = self.cpt.conditional_prob
      # find best pair by iterating over WxW
      from string import ascii_lowercase
      for b in ascii_lowercase:
        for c in ascii_lowercase:
          p = P(b,a) * P(c,b) * P(d,c)
          if p > likelihood:
            likelihood, likelyB, likelyC = p, b, c
      #return the most likely pair
      return [likelyB, likelyC]
    