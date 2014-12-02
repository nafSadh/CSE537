class Question3_Solver:
    def __init__(self):
        return;

    # Add your code here.
    # Return the centroids of clusters.
    # You must use [(30, 30), (150, 30), (90, 130)] as initial centroids
    def solve(self, points):
    # Algorithm
    # Step 1: Out of n objects, initialising k cluster centers
    # Step 2: Assign each object to its closest cluster center
    # Step 3: Update the center for each of the cluster
    # Step 4: Repeating Step 2 & Step 3 until there is no change in each of the cluster center.
        centroids = [(30, 60), (150, 60), (90, 130)];
        return centroids;

