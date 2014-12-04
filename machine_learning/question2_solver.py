class Question2_Solver:
  def __init__(self):
    self.classifier = NBClassifier()
    self.learn('train.data')
    return

  # Add your code here.
  # Read training data and build your naive bayes classifier
  # Store the classifier in this class
  # This function runs only once when initializing
  # Please read and only read train_data: 'train.data'
  def learn(self, train_data):
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
      #   values[a].add(features[a])

    # print threshold
    self.classifier.setup(domain,attributes,values)
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

  def setup(self, domain, attributes=[], values={}):
    self.domain = domain
    self.attributes = attributes
    self.dimension = len(attributes)
    self.values = values
    return

  def learn(self, examples):
    count = {}
    for a in self.attributes:
      count[a] = 0.0
      for v in self.values[a]:
        count[(a, v)] = 0.0

    for type in self.domain:
      count[type] = 0.0
      for a in self.attributes:
        for v in self.values[a]:
          count[(type, a, v)] = 0.0

    for (type, features) in examples:
      count[type] += 1.0
      for a in self.attributes:
        v = features[a]
        count[(a, v)] += 1.0
        count[a] += 1.0
        count[(type, a, v)] += 1.0

    n = len(examples)
    P = {}
    for type in self.domain:
      P[type] = count[type]/n
      for a in self.attributes:
        for v in self.values[a]:
          P[(type, a, v)] = (count[(type, a, v)]) / (count[type])

    self.P = P
    return

  def classify(self, features):
    mx = 0.0
    type = None
    for t in self.domain:
      p = self.P[t]
      for a in self.attributes:
        v = features[a]
        #if v != '?':
        p *= self.P[(t, a, v)]
      if type is None or p >= mx:
        type, mx = t, p

    return type
