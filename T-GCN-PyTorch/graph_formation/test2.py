# import pandas as pd
# import time

# # Start timing
# start_time = time.time()
#
# traffic2 = pd.read_csv(r'D:\GCN + LSTM\T-GCN-PyTorch\LSTW\traffic_full.csv')
# weather2 = pd.read_csv(r'D:\GCN + LSTM\T-GCN-PyTorch\LSTW\weather_sample.csv')
#
# # Find the latest time frame present in the traffic dataset
# latest_weather_timestamp = weather2['StartTime(UTC)'].max()
#
# print("Latest timestamp in weather DataFrame:", latest_weather_timestamp)
#
# latest_traffic_timestamp = traffic2['StartTime(UTC)'].max()
#
# print("Latest timestamp in traffic DataFrame:", latest_traffic_timestamp)
#
#
# # Calculate and print execution time
# end_time = time.time()
# execution_time = end_time - start_time
# print("Execution time:", execution_time, "seconds")

# import pandas as pd
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap

# Read the CSV file from Google Drive
# One1_filtered = pd.read_csv('filtered_data.csv')
#
# # Filter the DataFrame to include only nodes from specific states (FL, SC, NC, VA)
# specific_states_nodes = One1_filtered[One1_filtered['State'].isin(['MA','NH'])]
#
# # Keep only rows with unique combinations of latitude and longitude
# unique_nodes = specific_states_nodes.drop_duplicates(subset=['LocationLat_y', 'LocationLng_y'])
#
# # Count the number of unique nodes per state
# unique_nodes_per_state = unique_nodes.groupby('State').size().reset_index(name='Unique Node Count')
#
# # Print the total number of nodes for each state
# print("Total number of nodes per state:")
# print(unique_nodes_per_state)
#
# # Draw visualization on Basemap
# plt.figure(figsize=(12, 8))
# m = Basemap(projection='merc', llcrnrlat=20, urcrnrlat=50, llcrnrlon=-130, urcrnrlon=-60, resolution='l')
#
# # Draw coastlines, country boundaries, and states
# m.drawcoastlines()
# m.drawcountries()
# m.drawstates()
#
# # Plot unique nodes on the map
# for index, row in unique_nodes.iterrows():
#     lon, lat = row['LocationLng_y'], row['LocationLat_y']
#     x, y = m(lon, lat)
#     plt.plot(x, y, 'bo', markersize=3)  # Plotting points as blue circles
#     plt.text(x, y, f"{row['City']}, {row['State']}", fontsize=8, ha='left', va='center', color='black')
#
# plt.title('Unique Nodes of FL, SC, NC, VA on East Coast with City Names')
# plt.show()


import pandas as pd
import time

start_time = time.time()
# Read the CSV file from Google Drive
One1_filtered = pd.read_csv('filtered_data.csv')

# Assuming One1_filtered contains the DataFrame with Manchester nodes

One1_filtered_ma = One1_filtered[One1_filtered['State'] == 'MA']

# Group nodes based on latitude and longitude values
grouped_nodes_ma = One1_filtered_ma.groupby(['LocationLat_y', 'LocationLng_y'])

# Count the number of instances for each unique node
unique_nodes_counts_ma = grouped_nodes_ma.size().reset_index(name='Instance_Count')

# Save unique nodes with their instance counts to a CSV file
unique_nodes_counts_ma.to_csv('unique_nodes_ma.csv', index=False)

print("CSV file 'unique_nodes_ma.csv' has been saved with unique nodes in Massachusetts (MA) along with their instance counts.")


end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")





