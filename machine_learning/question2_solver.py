class Question2_Solver:
  def __init__(self, k=None):
    if k == None: k = 0.0001
    self.classifier = NBClassifier()
    self.learn('train.data',k)
    return

  # Add your code here.
  # Read training data and build your naive bayes classifier
  # Store the classifier in this class
  # This function runs only once when initializing
  # Please read and only read train_data: 'train.data'
  def learn(self, train_data,k):
    with open(train_data, "r") as f:
      data = f.read().splitlines()

    label, field = data[0].split()
    attributes = range(0, len(field.split(',')))

    values = {}
    for a in attributes:
      values[a]=['y','n','?']

    domain, examples = set(), []
    for row in data:
      label, features = row.split()
      domain.add(label)
      features = features.split(',')
      examples.append((label, features))
      # for a in attributes:
        # values[a].add(features[a])

    # print threshold
    self.classifier.setup(domain,attributes,values,k)
    self.classifier.learn(examples)
    return

  # Add your code here.
  # Use the learned naive bayes classifier to predict
  # query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
  # return 'republican' or 'republican'
  def solve(self, query):
    features = query.split(',')
    return self.classifier.classify(features)

class NBClassifier:
  def __init__(self):
    return

  def setup(self, domain, featureNames=[], featValues={}, k=0.0):
    self.domain = domain
    self.featNames = featureNames
    self.dimension = len(featureNames)
    self.featValues = featValues
    self.k = k
    return

  def learn(self, examples):
    count = {}
    for feat in self.featNames:
      count[feat] = 0.0
      for val in self.featValues[feat]:
        count[(feat, val)] = 1.0

    for label in self.domain:
      count[label] = 0.0
      for feat in self.featNames:
        for val in self.featValues[feat]:
          count[(label, feat, val)] = 0.0

    for (label, features) in examples:
      count[label] += 1.0
      for feat in self.featNames:
        val = features[feat]
        count[(feat, val)] += 1.0
        count[feat] += 1.0
        count[(label, feat, val)] += 1.0

    n = len(examples)
    P = {}
    k = self.k
    for label in self.domain:
      P[label] = (count[label])/(n)
      for feat in self.featNames:
        for val in self.featValues[feat]:
          P[(label, feat, val)] = (k+count[(label, feat, val)]) / (count[label]+k*len(self.featValues[feat]))

    self.P = P
    return

  def classify(self, features):
    mx = 0.0
    result = None
    for label in self.domain:
      p = (self.P[label])
      for feat in self.featNames:
        val = features[feat]
        if (label, feat, val) in self.P:
          p *= (self.P[(label, feat, val)])
      if result is None or p >= mx:
        result, mx = label, p

    return result

import math
lg=math.log