from string import ascii_lowercase

from question3_solver import CrossWordSolver

class Question4_Solver(CrossWordSolver):
    def __init__(self, cpt):
      CrossWordSolver.__init__(self,cpt)
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
    #    query: ["que-_-on", "--_--icial",
    #            "in_elligence", "inter--_"];
    #    return "t";
    def solve(self, query):
      letter = "e"
      q1,q2,q3,q4 = query
      P = self.getConditionalProbability

      enumEv = CrossWordSolver.enumEvidence
      (hl1, hs1), (tl1, ts1) = enumEv(q1)
      (hl2, hs2), (tl2, ts2) = enumEv(q2)
      (hl3, hs3), (tl3, ts3) = enumEv(q3)
      (hl4, hs4), (tl4, ts4) = enumEv(q4)

      mxp = 0.0
      for c in ascii_lowercase:
        pr =  P(hs1,c,hl1) * P(ts1, tl1,c) \
            * P(hs2,c,hl2) * P(ts2, tl2,c) \
            * P(hs3,c,hl3) * P(ts3, tl3,c) \
            * P(hs4,c,hl4) * P(ts4, tl4,c)
        if pr > mxp:
          mxp, letter = pr, c

      return letter
