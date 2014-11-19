from string import ascii_lowercase

def ind(c):
  return (ord(c) - 96)

class Question3_Solver:
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
        return self.cpt.conditional_prob(v, given)
      if step == 1:
        return self.cpt1[ind(given)][ind(v)]
      if step ==2:
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
    #    query: "qu--_--n";
    #    return "t";
    def solve(self, query):
      letter = "e"
      P = self.prob
      word = "`"+query+"`"
      pos = word.index("_")
      head = word[:pos]
      tail = word[pos+1:]
      tail = tail[::-1]

      l1, h1 = self.marginalLetter(head)
      l2, h2 = self.marginalLetter(tail)
      mxp = 0.0
      for c in ascii_lowercase:
        pr = P(h1,c,l1) * P(h2, l2,c)
        if pr > mxp:
          mxp, letter = pr, c

      # print query, letter, l1, h1, l2, h2
      return letter

    def marginalLetter(self, phrase):
      n = len(phrase)
      if n<2: return "`",0
      cp = self.cpt.conditional_prob
      pos = phrase.index("-")
      return phrase[pos-1],(n-pos)
