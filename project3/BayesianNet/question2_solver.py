from string import ascii_lowercase

def ind(c):
  return (ord(c) - 96)

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
      word = "`"+query+"`"
      pos = word.index("__")
      prev, next  = word[pos-1], word[pos+2]
      max = 0.0
      letter1, letter2 ="_","_"
      # shorthand for conditional probability
      P = self.cpt.conditional_prob
      # find best pair by iterating through all
      from string import ascii_lowercase
      for a in ascii_lowercase:
        for b in ascii_lowercase:
          pr = P(a,prev) * P(b,a) * P(next,b)
          if pr > max:
            max, letter1, letter2 = pr, a,b

      #print query, letter1, letter2
      return [letter1, letter2]
    