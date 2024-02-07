# import pandas as pd
# import folium
# import networkx as nx
# import numpy as np
#
# # Load the CSV data into a pandas DataFrame
# df = pd.read_csv('florida_nodes.csv')[:1000]
#
# # Load the adjacency matrix from the CSV file
# adjacency_df = pd.read_csv('florida_adjacency_matrix.csv', index_col=0)
# adjacency_matrix = adjacency_df.values
# n = len(adjacency_matrix)
#
# # Create a networkx graph from the adjacency matrix
# G = nx.Graph(adjacency_matrix)
#
# # Create a Folium map centered on Florida
# florida_map = folium.Map(location=[27.7663, -81.6868], zoom_start=7)
#
# # Plot data points on the map
# for index, row in df.iterrows():
#     folium.CircleMarker(
#         location=[row['LocationLat_x'], row['LocationLng_x']],
#         radius=5,
#         color='blue',
#         fill=True,
#         fill_color='blue',
#         fill_opacity=0.7,
#         popup=row['City']
#     ).add_to(florida_map)
#
# # Plot edges on the map
# for i, (src, dest) in enumerate(G.edges()):
#     src_lat, src_lng = df.loc[src, 'LocationLat_x'], df.loc[src, 'LocationLng_x']
#     dest_lat, dest_lng = df.loc[dest, 'LocationLat_x'], df.loc[dest, 'LocationLng_x']
#
#     edge = folium.PolyLine(
#         locations=[(src_lat, src_lng), (dest_lat, dest_lng)],
#         color='red',
#         weight=2,  # Adjust edge thickness here
#         opacity=1
#     ).add_to(florida_map)
#
#     # # Add edge number as a tooltip
#     # folium.Marker(
#     #     [(src_lat + dest_lat) / 2, (src_lng + dest_lng) / 2],
#     #     icon=None,
#     #     tooltip=f'Edge {i+1}'
#     # ).add_to(edge)
#
# # Display the map
# florida_map.save('florida_map_with_edges.html')


# For number of unique nodes

# import pandas as pd
#
# # Load the Florida nodes CSV
# df = pd.read_csv('florida_nodes.csv')
#
# # Create a set to store unique coordinates as tuples (latitude, longitude)
# unique_coordinates = set()
#
# # Iterate through the DataFrame and check for duplicate coordinates
# duplicate_count = 0
# for index, row in df.iterrows():
#     coordinates = (row['LocationLat_x'], row['LocationLng_x'])
#     if coordinates in unique_coordinates:
#         duplicate_count += 1
#     else:
#         unique_coordinates.add(coordinates)
#
# print(f"Total nodes in Florida nodes CSV: {len(df)}")
# print(f"Nodes with similar or the same coordinates: {duplicate_count}")
# print(f"Unique number of nodes are: {len(df)-duplicate_count}")

# import pandas as pd
#
# # Load the Florida nodes CSV
# df = pd.read_csv('florida_nodes.csv')
#
# # Sort the DataFrame by longitude, latitude, and start_time
# sorted_df = df.sort_values(by=['LocationLat_x', 'LocationLng_x', 'StartTime(UTC)'])
#
# # Save the sorted DataFrame to a new CSV file
# sorted_df.to_csv('florida_nodes_sorted.csv', index=False)


import pandas as pd
import numpy as np

# Load the CSV data into a pandas DataFrame
df = pd.read_csv('florida_nodes_sorted.csv')

# Create a mapping from node IDs to indices
node_indices = {node_id: idx for idx, node_id in enumerate(df['EventId_x'])}

# Initialize empty lists to store source and target nodes (edges)
source_nodes = []
target_nodes = []

# Iterate through the DataFrame rows to extract edges
for index, row in df.iterrows():
    source_id = node_indices[row['EventId_x']]
    target_id = node_indices[row['EventId_y']]

    # Add the edge to the lists
    source_nodes.append(source_id)
    target_nodes.append(target_id)

# Convert the lists to numpy arrays
edge_index = np.array([source_nodes, target_nodes], dtype=np.int64)

# Save the edge_index as a CSV file if needed
# np.savetxt('edge_index.csv', edge_index, delimiter=',', fmt='%d')

# Print the edge_index if needed
print(edge_index)



