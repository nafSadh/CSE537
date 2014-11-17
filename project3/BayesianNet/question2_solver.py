class Question2_Solver:
    def __init__(self, cpt):
        self.cpt = cpt;
        return

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
      word = "`"+query+"`"
      pos = word.index("__")
      prev = word[pos-1]
      next = word[pos+2]
      from string import ascii_lowercase
      max = 0.0
      letter1, letter2 ="_","_"
      # shorthand for conditional probability
      cp = self.cpt.conditional_prob
      # find best pair by iterating through all
      for a in ascii_lowercase:
        for b in ascii_lowercase:
          pr = cp(a,prev) * cp(b,a) * cp(next,b)
          if pr > max:
            max, letter1, letter2 = pr, a,b

      #print query, letter1, letter2
      return [letter1, letter2]


