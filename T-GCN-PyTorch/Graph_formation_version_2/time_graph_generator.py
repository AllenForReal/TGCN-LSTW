# import os
# import pandas as pd
# import folium
#
# # Read the dataset and sort it based on the timestamp
# unique_mass_nodes = pd.read_csv('unique_mass_nodes.csv')
# unique_mass_nodes['StartTime(UTC)'] = pd.to_datetime(unique_mass_nodes['StartTime(UTC)'])
#
# # Read the calculated intervals
# calculated_intervals = pd.read_csv('calculated_intervals.csv', parse_dates=['Start Time', 'End Time'])
#
# # Create a directory to store the maps
# os.makedirs('time_maps', exist_ok=True)
#
# # Iterate through the first 10 intervals
# for index, row in calculated_intervals.head(10).iterrows():
#     start_time = row['Start Time']
#     end_time = row['End Time']
#
#     # Filter the dataset based on the interval
#     filtered_data = unique_mass_nodes[
#         (unique_mass_nodes['StartTime(UTC)'] >= start_time) & (unique_mass_nodes['StartTime(UTC)'] < end_time)]
#
#     # Create a map centered on Massachusetts
#     m = folium.Map(location=[42.4075, -71.119], zoom_start=8)
#
#     # Add markers for each node
#     for i, node in filtered_data.iterrows():
#         folium.Marker(
#             location=[node['LocationLat_x'], node['LocationLng_x']],
#             popup=node['Description'],  # You can change this to display different information in the popup
#             icon=folium.Icon(color='blue', icon='info-sign')
#         ).add_to(m)
#
#     # Save the map to a file in the 'time_maps' directory
#     filename = f'time_maps/map_{start_time.strftime("%Y-%m-%d_%H-%M")}.html'
#     m.save(filename)


import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Read the dataset and sort it based on the timestamp
unique_mass_nodes = pd.read_csv('unique_mass_nodes_2.csv')
unique_mass_nodes['StartTime(UTC)'] = pd.to_datetime(unique_mass_nodes['StartTime(UTC)'])

# Read the calculated intervals
calculated_intervals = pd.read_csv('calculated_intervals_2.csv', parse_dates=['Start Time', 'End Time'])

# Create a directory to store the maps
os.makedirs('time_maps', exist_ok=True)

# Initialize map width and height
map_width = 800
map_height = 600

# Set up the Basemap
m = Basemap(projection='merc', llcrnrlat=41, urcrnrlat=43, llcrnrlon=-73, urcrnrlon=-69, resolution='i')

# Iterate through all intervals
for index, row in calculated_intervals.iterrows():
    start_time = row['Start Time']
    end_time = row['End Time']

    # Filter the dataset based on the interval
    filtered_data = unique_mass_nodes[
        (unique_mass_nodes['StartTime(UTC)'] >= start_time) & (unique_mass_nodes['StartTime(UTC)'] < end_time)]

    # Create a new figure and axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    # Plot the Basemap
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    # Plot data points
    x, y = m(filtered_data['LocationLng_x'].values, filtered_data['LocationLat_x'].values)
    m.scatter(x, y, marker='o', color='blue', zorder=10, label='Traffic Event')

    # Add a title and legend
    plt.title(f'Traffic Events in Massachusetts ({start_time.strftime("%Y-%m-%d %H:%M")} - {end_time.strftime("%Y-%m-%d %H:%M")})')
    plt.legend()

    # Save the map as PNG image
    map_image_path = f'time_maps/map_{start_time.strftime("%Y-%m-%d_%H-%M")}.png'
    plt.savefig(map_image_path, bbox_inches='tight')

    # Close the plot to free memory
    plt.close()

# Display completion message
print("Maps saved successfully.")


