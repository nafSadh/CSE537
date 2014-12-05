class Question3_Solver:
  def __init__(self):
    return

  # Add your code here.
  # Return the centroids of clusters.
  # You must use [(30, 30), (150, 30), (90, 130)] as initial centroids
  def solve(self, points):
    # Algorithm
    # Step 1: Out of n objects, initialising LidstoneSmoothingFactor cluster centers
    # Step 2: Assign each object to its closest cluster center
    # Step 3: Update the center for each of the cluster
    # Step 4: Repeating Step 2 & Step 3 until there is no change in each of the cluster center.


    centroids = [(30, 60), (150, 60), (90, 130)]
    # centroids = [(30, 30), (150, 30), (90, 130)]
    return KMeans(points, 3, centroids, 0.00001)


def KMeans(points, k, seeds, threshold):
  if seeds is None or len(seeds) < k:
    seeds = points[0:k]

  cluster = []
  for i in range(0, k):
    cluster.append([])

  for p in points:
    minD, ci = None, None
    for i in range(0, k):
      d = euclideanDistance(p, seeds[i])
      if minD is None or d < minD:
        minD, ci = d, i
    cluster[ci].append(p)

  centroids = []
  hasChange = False
  for i in range(0, k):
    centroids.append(centroid(cluster[i]))
    change = euclideanDistance(centroids[i], seeds[i])
    if change > threshold: hasChange = True

  if hasChange:
    return KMeans(points, k, centroids, threshold)
  else:
    return centroids


def centroid(points):
  X, Y = 0, 0
  for (x, y) in points:
    X += x
    Y += y
  n = len(points)
  x, y = X / n, Y / n
  return (x, y)


def euclideanDistance(p1, p2):
  (x1, y1) = p1
  (x2, y2) = p2
  return (x1 - x2) ** 2 + (y1 - y2) ** 2
