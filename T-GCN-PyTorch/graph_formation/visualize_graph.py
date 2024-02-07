# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt
#
# # Load the adjacency matrix from your CSV file
# adjacency_df = pd.read_csv('adjacency_matrix.csv', index_col=0)
# adjacency_matrix = adjacency_df.values
#
# # Load the 'City' feature from the original CSV file
# df = pd.read_csv('all_nodes.csv')
# city_feature = df['City'].values[:len(adjacency_matrix)]  # Get city feature for the same number of nodes as in the adjacency matrix
#
# # Get the number of nodes (n)
# n = len(adjacency_matrix)
#
# # Create an empty networkx graph
# G = nx.Graph()
#
# # Add nodes to the graph
# for i in range(n):
#     G.add_node(i, city=city_feature[i])  # Add city as an attribute to each node
#
# # Add edges to the graph based on the adjacency matrix
# for i in range(n):
#     for j in range(i + 1, n):  # Avoid duplicate edges
#         if adjacency_matrix[i, j] == 1:
#             G.add_edge(i, j)
#
# # Get the connected nodes (nodes with at least one connection)
# connected_nodes = [node for node, degree in G.degree() if degree > 0]
#
# # Create a subgraph with only connected nodes and their edges
# subgraph = G.subgraph(connected_nodes)
#
# # Compute node positions using Kamada-Kawai layout
# # node_positions = nx.kamada_kawai_layout(subgraph)
#
# node_positions = nx.spring_layout(subgraph)
#
# # Plot the subgraph with connected nodes, labels, and city feature on top
# plt.figure(figsize=(12, 12))
# node_labels = {node: city for node, city in nx.get_node_attributes(subgraph, 'city').items()}
# nx.draw(subgraph, pos=node_positions, with_labels=False, node_size=10, width=2, edge_color='b', node_color='r', style='solid')  # Added edge_color and node_color parameters
# nx.draw_networkx_labels(subgraph, pos=node_positions, labels=node_labels, font_size=8)
# plt.title('Connected Nodes with City Feature (Kamada-Kawai Layout)')
# plt.show()



# Using BaseMap


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from mpl_toolkits.basemap import Basemap

# # Load the CSV data into a pandas DataFrame
# df = pd.read_csv('all_nodes.csv')
#
# # Load the adjacency matrix from the CSV file
# adjacency_df = pd.read_csv('adjacency_matrix.csv', index_col=0)
# adjacency_matrix = adjacency_df.values
# n = len(adjacency_matrix)
#
# # Create a Basemap instance for plotting
# map = Basemap(projection='merc', llcrnrlat=min(df['LocationLat_x']), urcrnrlat=max(df['LocationLat_x']),
#               llcrnrlon=min(df['LocationLng_x']), urcrnrlon=max(df['LocationLng_x']), resolution='i')
#
# # Compute node positions based on latitude and longitude
# node_positions = {i: map(lon, lat) for i, lat, lon in zip(range(n), df['LocationLat_x'][:n], df['LocationLng_x'][:n])}
#
# # Create an empty networkx graph
# G = nx.Graph()
#
# # Add nodes to the graph with positions based on latitude and longitude
# for i in range(n):
#     city_name = df['City'].iloc[i]
#     state_name = df['State'].iloc[i]
#     G.add_node(i, lat=df['LocationLat_x'].iloc[i], lon=df['LocationLng_x'].iloc[i], city=city_name, state=state_name)
#
# # Add edges to the graph based on the adjacency matrix
# for i in range(n):
#     for j in range(i + 1, n):
#         if adjacency_matrix[i, j] == 1:
#             G.add_edge(i, j)
#
# # Get the connected nodes (nodes with at least one connection)
# connected_nodes = [node for node, degree in G.degree() if degree > 0]
#
# # Create a subgraph with only connected nodes and their edges
# subgraph = G.subgraph(connected_nodes)
#
# # Plot the subgraph with connected nodes, geographical positions, and city/state labels
# plt.figure(figsize=(12, 12))
# nx.draw(subgraph, pos=node_positions, with_labels=False, node_size=10, width=2, edge_color='b', node_color='r', style='solid')
# for node, data in subgraph.nodes(data=True):
#     x, y = node_positions[node]
#     city_name = data['city']
#     state_name = data['state']
#     label = f'{city_name}, {state_name}'
#     plt.text(x, y, label, fontsize=8, ha='center', va='center', color='k', fontweight='bold')
# map.drawcoastlines()
# map.drawcountries()
# map.drawmapboundary(fill_color='aqua')
# map.drawparallels(range(-90, 91, 5))
# map.drawmeridians(range(-180, 181, 5))
# plt.title(f'Connected Nodes within 20 Miles (Based on Latitude and Longitude) with City/State Labels')
# plt.show()


# Florida nodes basemap representation

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from mpl_toolkits.basemap import Basemap

# Load the CSV data into a pandas DataFrame
df = pd.read_csv('florida_nodes.csv')[:1000]

# Load the adjacency matrix from the CSV file
adjacency_df = pd.read_csv('florida_adjacency_matrix.csv', index_col=0)
adjacency_matrix = adjacency_df.values
n = len(adjacency_matrix)

# Create a Basemap instance for plotting
map = Basemap(projection='merc', llcrnrlat=min(df['LocationLat_x']), urcrnrlat=max(df['LocationLat_x']),
              llcrnrlon=min(df['LocationLng_x']), urcrnrlon=max(df['LocationLng_x']), resolution='i')

# Compute node positions based on latitude and longitude
node_positions = {i: map(lon, lat) for i, lat, lon in zip(range(n), df['LocationLat_x'][:n], df['LocationLng_x'][:n])}

# Create an empty networkx graph
G = nx.Graph()

# Add nodes to the graph with positions based on latitude and longitude
for i in range(n):
    city_name = df['City'].iloc[i]
    G.add_node(i, lat=df['LocationLat_x'].iloc[i], lon=df['LocationLng_x'].iloc[i], city=city_name)

# Add edges to the graph based on the adjacency matrix
for i in range(n):
    for j in range(i + 1, n):
        if adjacency_matrix[i, j] == 1:
            G.add_edge(i, j)

# Get the connected nodes (nodes with at least one connection)
connected_nodes = list(G.nodes())

# Create a subgraph with all nodes and their edges
subgraph = G.subgraph(connected_nodes)

# Plot the subgraph with connected nodes, geographical positions, city names, and node degrees
plt.figure(figsize=(12, 12))
nx.draw(subgraph, pos=node_positions, with_labels=False, node_size=10, width=0.2, edge_color='b', node_color='r', style='solid')
for node, data in subgraph.nodes(data=True):
    x, y = node_positions[node]
    city_name = data['city']
    node_degree = subgraph.degree[node]
    label = f'{city_name}\nDegree: {node_degree}'
    plt.text(x, y, label, fontsize=8, ha='center', va='center', color='k', fontweight='bold')
map.drawcoastlines()
map.drawcountries()
map.drawmapboundary(fill_color='aqua')
map.drawparallels(range(-90, 91, 5))
map.drawmeridians(range(-180, 181, 5))
plt.title(f'All Nodes (Based on Latitude and Longitude) with City and Node Degree')
plt.show()


# Kamada Kawai Layout for florida nodes

# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt
#
# # Load the adjacency matrix from your CSV file
# adjacency_df = pd.read_csv('florida_adjacency_matrix.csv', index_col=0)
# adjacency_matrix = adjacency_df.values
#
# # Load the 'City' feature from the original CSV file
# df = pd.read_csv('florida_nodes.csv')
# city_feature = df['City'].values[:len(adjacency_matrix)]  # Get city feature for the same number of nodes as in the adjacency matrix
#
# # Get the number of nodes (n)
# n = len(adjacency_matrix)
#
# # Create an empty networkx graph
# G = nx.Graph()
#
# # Add nodes to the graph
# for i in range(n):
#     G.add_node(i, city=city_feature[i])  # Add city as an attribute to each node
#
# # Add edges to the graph based on the adjacency matrix
# for i in range(n):
#     for j in range(i + 1, n):  # Avoid duplicate edges
#         if adjacency_matrix[i, j] == 1:
#             G.add_edge(i, j)
#
# # Get the connected nodes (nodes with at least one connection)
# connected_nodes = [node for node, degree in G.degree() if degree > 0]
#
# # Create a subgraph with only connected nodes and their edges
# subgraph = G.subgraph(connected_nodes)
#
# # Compute node positions using Kamada-Kawai layout
# # node_positions = nx.kamada_kawai_layout(subgraph)
#
# node_positions = nx.spring_layout(subgraph)
#
# # Plot the subgraph with connected nodes, labels, and city feature on top
# plt.figure(figsize=(12, 12))
# node_labels = {node: city for node, city in nx.get_node_attributes(subgraph, 'city').items()}
# nx.draw(subgraph, pos=node_positions, with_labels=False, node_size=10, width=0.1, edge_color='b', node_color='r', style='solid')  # Added edge_color and node_color parameters
# nx.draw_networkx_labels(subgraph, pos=node_positions, labels=node_labels, font_size=8)
# plt.title('Connected Nodes with City Feature (Kamada-Kawai Layout)')
# plt.show()














