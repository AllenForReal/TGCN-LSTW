import pandas as pd
import numpy as np
from geopy.distance import geodesic
from sklearn.metrics.pairwise import haversine_distances
from scipy.spatial import distance_matrix
from scipy.sparse import csr_matrix

# Load the CSV data into a pandas DataFrame
df = pd.read_csv('graph_formation/all_nodes.csv')

# Get the number of rows in the DataFrame
n = len(df)

# Initialize an n x n adjacency matrix with all zeros
adjacency_matrix = np.zeros((n, n), dtype=int)

# Define your connectivity condition (e.g., within 20 miles)
def is_connected(node1, node2):
    lat1, lon1 = node1['LocationLat_x'], node1['LocationLng_x']
    lat2, lon2 = node2['LocationLat_x'], node2['LocationLng_x']
    distance = geodesic((lat1, lon1), (lat2, lon2)).miles
    return distance <= 20

# Iterate through the rows and set adjacency_matrix[i][j] to 1 if connected
for i in range(n):
    for j in range(n):
        if is_connected(df.iloc[i], df.iloc[j]):
            adjacency_matrix[i][j] = 1

# Convert the adjacency matrix to a DataFrame
adjacency_df = pd.DataFrame(adjacency_matrix, columns=df.index, index=df.index)

# Save the adjacency matrix as a CSV file
adjacency_df.to_csv('adjacency_matrix.csv')

# Define feature columns including 'Distance' and 'Side'
feature_columns = ['Type_x', 'Severity_x', 'Type_y', 'Severity_y', 'Distance(mi)', 'Side']
feature_matrix = df[feature_columns].values

# Convert the adjacency matrix to a DataFrame with 'EventId_x' as both index and columns
# adjacency_df = pd.DataFrame(adjacency_matrix, columns=df['EventId_x'], index=df['EventId_x'])
#
# # Save the adjacency matrix as a CSV file
# adjacency_df.to_csv('adjacency_matrix.csv')

print(adjacency_matrix)


def print_feature_matrix():
    print(feature_matrix)

print("completed")
# Now you have the adjacency matrix and updated feature matrix for your GCN model.


