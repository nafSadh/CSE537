class Question1_Solver:
    def __init__(self, cpt):
        self.cpt = cpt;
        return;

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
    #    query: "ques_ion";
    #    return "t";
    def solve(self, query):
      word = "`"+query+"`"
      pos = word.index('_')
      prev = word[pos-1]
      next = word[pos+1]
      from string import ascii_lowercase
      max = 0.0
      letter ="_"
      for c in ascii_lowercase:
        pr = self.cpt.conditional_prob(c,prev) * self.cpt.conditional_prob(next,c)
        if pr > max:
          max, letter = pr, c

      #print query, letter
      return letter


