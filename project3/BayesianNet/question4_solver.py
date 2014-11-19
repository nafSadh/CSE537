from string import ascii_lowercase
import math


def ind(c):
  return (ord(c) - 96)

class Question4_Solver:
    def __init__(self, cpt):
      self.cpt = cpt
      self.computeIntermediateProbabilities()


    def computeIntermediateProbabilities(self):
      letters = "`"+ascii_lowercase
      cp = self.cpt.conditional_prob

      self.cpt1 = [[0.0] * 27 for i in range(27)]
      for a in letters:
        total = 0.0
        for c in letters:
          sumB = 0.0
          for B in letters:
            sumB += (cp(B,a) * cp(c,B))
          self.cpt1[ind(a)][ind(c)] = 1.0*sumB
          total += sumB
        for c in letters:
          self.cpt1[ind(a)][ind(c)]/=total

      self.cpt2 = [[0.0] * 27 for i in range(27)]
      for a in letters:
        total = 0.0
        for d in letters:
          sumC = 0.0
          for C in letters:
            sumC += (self.cp1(C,a) * cp(d,C))
          self.cpt2[ind(a)][ind(d)] = 1.0*sumC
          total += sumC
        for c in letters:
          self.cpt2[ind(a)][ind(d)]/=total


    def cp1(self, c,a):
      return self.cpt1[ind(a)][ind(c)]

    def cp2(self, d,a):
      return self.cpt2[ind(a)][ind(d)]


    def prob(self, step, v, given):
      if step == 0:
        return  self.cpt.cpt[ind(given)][ind(v)]
      elif step == 1:
        return self.cpt1[ind(given)][ind(v)]
      elif step ==2:
        return self.cpt2[ind(given)][ind(v)]


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
      P = self.prob

      (hl1, hs1), (tl1, ts1) = self.enumEvidence(q1)
      (hl2, hs2), (tl2, ts2) = self.enumEvidence(q2)
      (hl3, hs3), (tl3, ts3) = self.enumEvidence(q3)
      (hl4, hs4), (tl4, ts4) = self.enumEvidence(q4)

      mxp = 0.0
      for c in ascii_lowercase:
        pr =  P(hs1,c,hl1) * P(ts1, tl1,c) \
            * P(hs2,c,hl2) * P(ts2, tl2,c) \
            * P(hs3,c,hl3) * P(ts3, tl3,c) \
            * P(hs4,c,hl4) * P(ts4, tl4,c)
        if pr > mxp:
          mxp, letter = pr, c

      return letter

    def enumEvidence(self, word):
      word = "`"+word+"`"
      pos = word.index("_")
      head, tail = word[:pos], word[pos+1:]
      tail = tail[::-1]
      return self.marginalLetter(head), self.marginalLetter(tail)

    def marginalLetter(self, phrase):
      n = len(phrase)
      phrase += "-"
      pos = phrase.index("-")
      # print phrase, phrase[pos-1],n, pos
      return phrase[pos-1],(n-pos)

