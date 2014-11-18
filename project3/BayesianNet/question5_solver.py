class Question5_Solver:
    def __init__(self, cpt2):
        self.cpt2 = cpt2
        return

    #####################################
    # ADD YOUR CODE HERE
    #         _________
    #        |         v
    # Given  z -> y -> x
    # Pr(x|z,y) = self.cpt2.conditional_prob(x, z, y);
    #
    # A word begins with "``" and ends with "``".
    # For example, the probability of word "ab":
    # Pr("ab") = \
    #    self.cpt2.conditional_prob("a", "`", "`") * \
    #    self.cpt2.conditional_prob("b", "`", "a") * \
    #    self.cpt2.conditional_prob("`", "a", "b") * \
    #    self.cpt2.conditional_prob("`", "b", "`");
    # query example:
    #    query: "ques_ion";
    #    return "t";
    def solve(self, query):
      word = "``"+query+"``"
      pos = word.index('_')
      a,b = word[pos-2],word[pos-1]
      d,e = word[pos+1],word[pos+2]
      mxp, letter = 0.0, "_"
      # shorthand for conditional probability
      cp = self.cpt2.conditional_prob
      # find best pair by iterating through all
      from string import ascii_lowercase
      for c in ascii_lowercase:
        pr = cp(c,a,b) * cp(d,b,c) * cp (e,c,d)
        if pr > mxp:
          mxp, letter = pr, c
      return letter
