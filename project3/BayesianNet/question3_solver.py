from string import ascii_lowercase

class Question3_Solver:
    def __init__(self, cpt):
        self.cpt = cpt;

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
      cp = self.cpt.conditional_prob
      word = "`"+query+"`"
      pos = word.index("_")
      head = word[:pos]
      tail = word[pos+1:]
      tail = tail[::-1]

      l1 = self.marginalLetter(head)
      l2 = self.marginalLetter(tail)

      max = 0.0
      for c in ascii_lowercase:
        pr = cp(c,l1) * cp(l2,c)
        if pr > max:
          max, letter = pr, c
      return letter

    def marginalLetter(self, phrase):
      n = len(phrase)
      if n<2: return "`"
      cp = self.cpt.conditional_prob
      pos = phrase.index("-")
      ltr = "-"
      while pos < n:
        prev = phrase[pos-1]
        p1=0.0
        for a in ascii_lowercase:
          p = cp(a,prev)
          if p>p1:
            ltr,p1 = a,p
        phrase = phrase[:pos]+ltr+phrase[pos+1:]
        pos+=1
      return ltr
