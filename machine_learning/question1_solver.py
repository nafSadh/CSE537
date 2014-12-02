class Question1_Solver:
    def __init__(self):
        self.learn('train.data')
        return

    # Add your code here.
    # Read training data and build your decision tree
    # Store the decision tree in this class
    # This function runs only once when initializing
    # Please read and only read train_data: 'train.data'
    def learn(self, train_data):
      with open("validation.data", "r") as f:
        data = f.read().splitlines()

      label, field = data[0].split()
      attributes = range (0, len(field.split(',')))

      values = []
      for a in attributes:
        values.append(set())

      domain, examples = set(),[]
      for row in data:
        label, fields = row.split()
        domain.add(label)
        fields = fields.split(',')
        examples.append((label, fields))
        for a in attributes:
          values[a].add(fields[a])

      tree = ID3(examples, attributes, values, domain,"-",3)

      print tree
      self.decisionTree = tree
      self.attributes = attributes
      self.values = values
      self.domain = domain
      return


    # Add your code here.
    # Use the learned decision tree to predict
    # query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
    # return 'republican' or 'republican'
    def solve(self, query):
      node = self.decisionTree
      fields = query.split(',')
      label = None

      while label is None:
        label = node.label
        if node.decisionAttribute is not None:
          v = fields[node.decisionAttribute]
          node = node.children[v]
        else:
          label = node.label
          if label is None:
            print node
            label='democrat'

      return label

class DTNode:
  def __init__(self, level, entropy, label=None, decisionAttribute=None, domain=set(), children={}):
    self.label = label
    self.level = level
    self.decisionAttribute = decisionAttribute
    self.domain = domain
    self.children = children
    self.entropy = entropy

  def __str__(self):
    if self.label is not None:
      return "(" + self.label+":"+str(self.entropy) + ")"

    childrenStr = ""
    for child in self.children:
      childrenStr+='\n'+str(len(self.level))+self.level+''+str(child)+":"+str(self.children[child])

    return "(" + str(self.decisionAttribute)+":"+str(self.entropy)+"|"+str(self.domain)+"|"+childrenStr+")"

def ID3(examples, attributes, values, domain, level, threshold=1):
  entropy = Entropy(examples,domain)
  label = examples[0][0]
  domainCount = {}
  for d in domain: domainCount[d] = 0

  allSame = True
  for example in examples:
    l = example[0]
    if l != label: allSame = False
    domainCount[l] +=1

  if allSame:
    return DTNode(level,entropy,label,None,set())

  majority, mx = None,0
  for d in domain:
    if domainCount[d] > mx:
      majority,mx = d, domainCount[d]

  if attributes is None or len(attributes) <1 or len(examples)<threshold:
    return DTNode(level,entropy,majority,None, set())

  (bestAttrib, subsets) = BestAttrib(examples, entropy,attributes, values, domain)

  children = {}

  remainingAttributes = attributes[:]
  remainingAttributes.remove(bestAttrib)

  for v in values[bestAttrib]:
    if len(subsets[v])<1: children[v] = DTNode(level,entropy,majority)
    else:
      children[v] = ID3(subsets[v],remainingAttributes,values,domain, level+'-', threshold)

  return DTNode(level,entropy, None, bestAttrib,domain,children)

def BestAttrib(examples, baseEntropy, attributes, values, domain):
  best, bestGain = None, None
  nS = len(examples)
  for a in attributes:
    gain = baseEntropy
    subsets = {}
    for val in values[a]:
      subsets[val] = []
    for example in examples:
      label, fields = example
      fieldVal = fields[a]
      subsets[fieldVal].append(example)
    entropies = {}
    for val in values[a]:
      e = Entropy(subsets[val],domain)
      entropies[val] = e
      gain -=(1.0*len(subsets[val])/nS)*e

    if bestGain is None or gain>bestGain:
      best, bestGain = (a, subsets), gain
      
  return best

from math import log
def Entropy(examples, domain):
  domainCount = {}
  for d in domain: domainCount[d] = 0
  for example in examples:
    l = example[0]
    domainCount[l] +=1

  entropy = 0
  total = len(examples)
  if total<1: return 0.0
  for d in domain:
    n = domainCount[d]
    x = 1.0*n/total
    p = 0 if x==0.0 else (x * log(x))
    entropy-=p
    
  return entropy

