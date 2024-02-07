import pandas as pd
import numpy as np
from geopy.distance import geodesic

# # Load the CSV data into a pandas DataFrame
# df = pd.read_csv('all_nodes.csv')
#
# # Get the number of rows in the DataFrame and limit it to 1000 rows
# n = min(len(df), 1000)
#
# # Define your connectivity condition (e.g., within 20 miles)
# def is_connected(node1, node2):
#     lat1, lon1 = node1['LocationLat_x'], node1['LocationLng_x']
#     lat2, lon2 = node2['LocationLat_x'], node2['LocationLng_x']
#     distance = geodesic((lat1, lon1), (lat2, lon2)).miles
#     return distance <= 20
#
# adjacency_matrix = np.zeros((n, n), dtype=int)
#
# # Loop through all pairs of nodes and apply your connectivity condition
# for i in range(n):
#     for j in range(n):  # Loop through all nodes
#         if is_connected(df.iloc[i], df.iloc[j]):
#             adjacency_matrix[i, j] = 1
#         if (i + j ==1000):
#           print(i,' , ',j)
#
# # Save the adjacency matrix as a CSV file
# adjacency_df = pd.DataFrame(adjacency_matrix, columns=df['EventId_x'][:n], index=df['EventId_x'][:n])
# adjacency_df.to_csv('adjacency_matrix.csv')
#
# # Define feature columns including 'Distance' and 'Side'
# feature_columns = ['Type_x', 'Severity_x', 'Type_y', 'Severity_y', 'Distance(mi)', 'Side']
# feature_matrix = df[feature_columns][:n].values
#
# # Create a DataFrame for the feature matrix
# feature_df = pd.DataFrame(feature_matrix, columns=feature_columns, index=df['EventId_x'][:n])
#
# # Save the feature matrix as a CSV file
# feature_df.to_csv('feature_matrix.csv')
#
# print("Completed. Adjacency matrix and feature matrix (limited to 1000 rows) saved as CSV files.")


import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Load the CSV data into a pandas DataFrame
df = pd.read_csv('all_nodes.csv')

# Filter rows where the State is 'FL' (Florida)
florida_df = df[df['State'] == 'FL'][:1000]  # Limit to the first 1000 rows

# Get the number of rows in the DataFrame
n = len(florida_df)

# Define your connectivity condition (e.g., within 20 miles)
def is_connected(node1, node2):
    lat1, lon1 = node1['LocationLat_x'], node1['LocationLng_x']
    lat2, lon2 = node2['LocationLat_x'], node2['LocationLng_x']
    distance = geodesic((lat1, lon1), (lat2, lon2)).miles
    return distance <= 20

adjacency_matrix = np.zeros((n, n), dtype=int)

# Loop through all pairs of nodes and apply your connectivity condition
for i in range(n):
    for j in range(n):  # Loop through all nodes
        if is_connected(florida_df.iloc[i], florida_df.iloc[j]):
            adjacency_matrix[i, j] = 1

        if (i + j == n):
            print(i, " , ", j)

# Save the adjacency matrix as a CSV file
adjacency_df = pd.DataFrame(adjacency_matrix, columns=florida_df['EventId_x'], index=florida_df['EventId_x'])
adjacency_df.to_csv('florida_adjacency_matrix.csv')

# Define feature columns including 'Distance' and 'Side'
feature_columns = ['Type_x', 'Severity_x', 'Type_y', 'Severity_y', 'Distance(mi)', 'Side']
feature_matrix = florida_df[feature_columns].values

# Create a DataFrame for the feature matrix
feature_df = pd.DataFrame(feature_matrix, columns=feature_columns, index=florida_df['EventId_x'])

# Save the feature matrix as a CSV file
feature_df.to_csv('florida_feature_matrix.csv')

print("Completed. Adjacency matrix and feature matrix (limited to 1000 rows) for Florida nodes saved as CSV files.")
