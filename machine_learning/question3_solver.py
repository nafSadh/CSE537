class Question3_Solver:
  def __init__(self):
    return

  # Add your code here.
  # Return the centroids of clusters.
  # You must use [(30, 30), (150, 30), (90, 130)] as initial centroids
  def solve(self, points):
    # Algorithm
    # Step 1: Out of n objects, initialising k cluster centers
    # Step 2: Assign each object to its closest cluster center
    # Step 3: Update the center for each of the cluster
    # Step 4: Repeating Step 2 & Step 3 until there is no change in each of the cluster center.


    centroids = [(30, 60), (150, 60), (90, 130)]
    return KMeans(points,3,centroids,0.00001)
    # k should be a parameter ?? - how we know the value of k
    # Creating k clusters using those centroids
    clusters = [Cluster([p]) for p in centroids]

    # Looping on the dataset untill the clusters synchronise
    loopCounter = 0
    while True:
      lists = [[] for c in clusters]
      clusterCount = 1
      en(clusters)

      # loop counter
      loopCounter += 1
      # for every point in dataset
      for p in points:
        # Get the distance between the point and centroid of the first cluster
        smallest_distance = getDistamce(p, clusters[0].centroid)

        # Set the cluster this point belongs to
        clusterIndex = 0
        # For the remainder of the clusters ...
        for i in range(clusterCount - 1):
          # calculate the distance of that point to each other cluster's
          # centroid.
          distance = getDistance(p, clusters[i + 1].centroid)
          # If it's closer to that cluster's centroid update what we
          # think the smallest distance is, and set the point to belong
          # to that cluster
          if distance < smallest_distance:
            smallest_distance = distance
            clusterIndex = i + 1
        lists[clusterIndex].append(p)
        # Set our biggest_shift to zero for this iteration
    biggest_shift = 0.0
    # As many times as there are clusters ...
    for i in range(clusterCount):
      # Calculate how far the centroid moved in this iteration
      shift = clusters[i].update(lists[i])
      # Keep track of the largest move from all cluster centroid updates
      biggest_shift = max(biggest_shift, shift)

      # If the centroids have stopped moving much, say we're done!
    if biggest_shift < cutoff:
      print "Converged after %s iterations" % loopCounter
      # break

    return clusters

def KMeans(points, k, seeds, threshold):
  if seeds is None or len(seeds)<k:
    seeds = points[0:k]

  converged = False

  cluster = []
  for i in range(0,k):
    cluster.append([])

  for p in points:
    minD, ci = None, None
    for i in range(0,k):
      d = euclideanDistance(p, seeds[i])
      if minD is None or d<minD:
        minD, ci = d, i
    cluster[ci].append(p)
  centroids=[]
  hasChange = False
  for i in range(0,k):
    centroids.append(centroid(cluster[i]))
    change = euclideanDistance(centroids[i],seeds[i])
    if change > threshold: hasChange = True
  if not hasChange: converged =True

  if not converged:
    return KMeans(points,k, centroids, threshold)
  else:
    return centroids



def centroid(points):
  X,Y=0,0
  for (x,y) in points:
    X+=x
    Y+=y
  n = len(points)
  x,y = X/n, Y/n
  return (x,y)

def euclideanDistance(p1,p2):
  (x1,y1) = p1
  (x2,y2) = p2
  return (x1-x2)**2 + (y1-y2)**2

class Cluster:
  """
  A set of points & centroids
  """

  def __init__(self, points):
    # A list of point objects
    # The points that belong to this cluster
    self.points = points
    # The dimensionality of the points in this cluster
    self.n = points[0].n
    # Set up the initial centroid (this is usually based off one point)
    self.centroid = self.calculateCentroid()

  def __repr__(self):
    # string representation of the object
    return str(self.points)

  def update(self, points):
    """
    Returns the distance between the previous centroid and the new after
    recalculating and storing the new centroid.
    """
    old_centroid = self.centroid
    self.points = points
    self.centroid = self.calculateCentroid()
    shift = getDistance(old_centroid, self.centroid)
    return shift

  def calculateCentroid(self):
    """
    Finds a virtual center point for a group of n-dimensional points
    """
    numPoints = len(self.points)
    # Get a list of all coordinates in this cluster
    coords = [p.coords for p in self.points]
    # Reformat that so all x's are together, all y'z etc.
    unzipped = zip(*coords)
    # Calculate the mean for each dimension
    centroid_coords = [math.fsum(dList) / numPoints for dList in unzipped]

    return Point(centroid_coords)


def getDistance(a, b):
  """
  Euclidean distance between two n-dimensional points.
  """
  ret = reduce(lambda x, y: x + pow((a.coords[y] - b.coords[y]), 2), range(a.n), 0.0)
  return math.sqrt(ret)


def makeRandomPoint(n, lower, upper):
  """
  Returns a Point object with n dimensions and featValues between lower and
  upper in each of those dimensions
  """
  p = Point([random.uniform(lower, upper) for i in range(n)])
  return p