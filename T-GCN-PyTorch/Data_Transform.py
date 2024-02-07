import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
#from torch_geometric.nn import GCNConv, GATConv
import sys
#analyze the weight of nodes and relationship between them base on severity
from datetime import datetime, timedelta
import seaborn as sns
from geopy.distance import geodesic

# weather_sample=pd.read_csv('LSTW/weather.csv')
# traffic_sample=pd.read_csv('LSTW/traffic.csv')
#
# # weather=weather.sort_values(by=['State','City','StartTime(UTC)'])
# # traffic=traffic.sort_values(by=['State','City','StartTime(UTC)'])
# # # Crop to the first 37000 rows
# # weather_short = weather.iloc[:37000]
# # traffic_short = traffic.iloc[:37000]
#
# # weather_sample = weather[weather['State'].isin(['FL', 'GA'])]
# # traffic_sample = traffic[traffic['State'].isin(['FL', 'GA'])]
# # # Save the cropped data to a new CSV file
# # weather_sample.to_csv('LSTW/weather_sample.csv', index=False)
# # traffic_sample.to_csv('LSTW/traffic_sample.csv', index=False)
# #-------------------------------------------------------------------------------------------------------------
#
# traffic_sample['StartTime(UTC)'] = pd.to_datetime(traffic_sample['StartTime(UTC)'])
# weather_sample['StartTime(UTC)'] = pd.to_datetime(weather_sample['StartTime(UTC)'])
#
# # traffic.rename(columns={"StartTime(UTC)": "StartTime(UTC)_T", "EndTime(UTC)": "EndTime(UTC)_T"})
# # weather.rename(columns={"StartTime(UTC)": "StartTime(UTC)_W", "EndTime(UTC)": "EndTime(UTC)_W"})
#
# # Assuming traffic and weather are already defined and loaded DataFrame
# # Sort and drop NaN values as well as non important columns
# traffic2 = traffic_sample.drop(['TMC', 'Description', 'TimeZone'], axis=1)
# weather2 = weather_sample.drop(['AirportCode', 'County', 'TimeZone'], axis=1)
# traffic2 = traffic2.dropna(subset=['StartTime(UTC)', 'LocationLat', 'LocationLng', 'ZipCode'])
# weather2 = weather2.dropna(subset=['StartTime(UTC)', 'LocationLat', 'LocationLng', 'ZipCode'])
# # traffic2 = traffic.sort_values(by=[ 'StartTime(UTC)','LocationLat', 'LocationLng'], ascending=True)
# # weather2 = weather.sort_values(by=[ 'StartTime(UTC)','LocationLat', 'LocationLng'], ascending=True)
# #print(traffic2['StartTime(UTC)'].dtype, weather2['ZipCode'].dtype)
#
# #-------------------------------------------------------------------------------------------------------------
# print(traffic2['StartTime(UTC)'].dtype, weather2['StartTime(UTC)'].dtype)
# print(traffic2['State'].dtype, weather2['State'].dtype)
# print(traffic2['City'].dtype, weather2['City'].dtype)
#
# # Ensure 'StartTime(UTC)' is of datetime type
# traffic2['StartTime(UTC)'] = pd.to_datetime(traffic2['StartTime(UTC)'])
# weather2['StartTime(UTC)'] = pd.to_datetime(weather2['StartTime(UTC)'])
#
# # Ensure 'State' and 'City' are of string type
# traffic2['State'] = traffic2['State'].astype(str)
# weather2['State'] = weather2['State'].astype(str)
# traffic2['City'] = traffic2['City'].astype(str)
# weather2['City'] = weather2['City'].astype(str)
#
# #-------------------------------------------------------------------------------------------------------------
# # Create new column 'StartTime(UTC)_W' in weather2
# weather2['StartTime(UTC)_W'] = weather2['StartTime(UTC)']
#
# # Display the first few rows of both DataFrames
# # print(traffic2.head())
# # print(weather2.head())
# #-------------------------------------------------------------------------------------------------------------

weather2=pd.read_csv('LSTW/weather_sample.csv')
traffic2=pd.read_csv('LSTW/traffic_sample.csv')

traffic2['StartTime(UTC)'] = pd.to_datetime(traffic2['StartTime(UTC)'])
weather2['StartTime(UTC)'] = pd.to_datetime(weather2['StartTime(UTC)'])
# Drop duplicates
traffic2 = traffic2.drop_duplicates(subset=['State', 'City', 'StartTime(UTC)'])
weather2 = weather2.drop_duplicates(subset=['State', 'City', 'StartTime(UTC)'])
# Drop rows with NaN in specific columns
traffic2 = traffic2.dropna(subset=['State', 'City', 'StartTime(UTC)', 'LocationLat', 'LocationLng', 'ZipCode'])
weather2 = weather2.dropna(subset=['State', 'City', 'StartTime(UTC)', 'LocationLat', 'LocationLng', 'ZipCode'])


traffic2 = traffic2.sort_values(by=['StartTime(UTC)', 'State','City'], ascending=True)
weather2 = weather2.sort_values(by=['StartTime(UTC)', 'State','City'], ascending=True)

print(traffic2.head())
print(weather2.head())

weather2.to_csv('LSTW/weather_sorted.csv', index=False)
traffic2.to_csv('LSTW/traffic_sorted.csv', index=False)
One1 = pd.merge_asof(
    weather2,
    traffic2,
    on='StartTime(UTC)',
    by=['State','City'],
    tolerance=pd.Timedelta(hours=1),
    direction='nearest'
)

# For now we have set the distance to nearest, later we can filter connections and edges using the calculate_distance function
# def calculate_distance(row):
#     # Create tuples of (latitude, longitude) for traffic and weather
#     coords_traffic = (row['LocationLat_x'], row['LocationLng_x'])
#     coords_weather = (row['LocationLat_y'], row['LocationLng_y'])
#
#     # Calculate the distance
#     return geodesic(coords_traffic, coords_weather).kilometers
#
# One1['Distance'] = One1.apply(calculate_distance, axis=1)
# Save 'One' DataFrame to a CSV file

One1['adjacency']=0
One1.loc[One1['EventId_y'].notna(), 'adjacency'] = 1

One1.to_csv('quick_test_data.csv', index=False)

print("DataFrame 'One' has been saved as 'merged_data.csv'")

One1.head()
#
# # Phase 1: Traffic modeling only, do transpose on ZipCode_x, nodes are locations, and node features are type, severity, duration etc
# # Phase 2: Model traffic weather relation using the merged data, heterogeneous GNN, nodes are locations, and node features are type, severity, duration etc from both traffic and weather.
# # Phase 3: Validate the model with noise, Gaussian or Poisson. Try to implement Transformer based models, such as BERT.
# # we need to do transpose on ZipCode_y, such that there are many observation
#
# # if One1['EventId_x'].notna().bool() and One1['EventId_y'].notna().bool():
# #     One1['adjacency_t'] = 1
# #     One1['adjacency_w'] = 1
# #     #features_traffic = traffic2['EventId_x', '']
# #     features_both = One['EventId_x', 'EventId_y', 'Type_x', 'Type_y', 'Severity_x', 'Severity_y', 'TMC', 'StartTime(UTC)', 'EndTime(UTC)', 'LocationLat_x', 'LocationLng_x','LocationLat_y', 'LocationLng_y','City', 'State', 'ZipCode_x', 'ZipCode_y']
# # else:
# #     One1['adjacency_t'] = 0
# #     One1['adjacency_w'] = 0
#
# #create feature matrix
# features_traffic = np.stack([traffic2['EventId'], traffic2['StartTime(UTC)'], traffic2['Type'], traffic2['Severity'], traffic2['State'], traffic2['City']])
# features_weather = np.stack([weather2['EventId'], weather2['StartTime(UTC)'], weather2['Type'], weather2['Severity'], weather2['State'], weather2['City']])
# features_both = np.stack([One1['EventId_x'], One1['EventId_y'],One1['Type_x'], One1['Type_y'], One1['Severity_x'], One1['Severity_y'])#, 'Severity_x', 'Severity_y', 'TMC', 'StartTime(UTC)', 'EndTime(UTC)', 'LocationLat_x', 'LocationLng_x', 'LocationLat_y', 'LocationLng_y']) # 'City', 'State', 'ZipCode_x', 'ZipCode_y']
# features_traffic = features_traffic.transpose()
# features_weather = features_weather.transpose()
# features_both = features_both.transpose()
# print(features_both)
# print(features_both.shape)
#
#
#
#
# #def set_adj(pd:DataFrame, func,)->list:
#
#
# for index, value in One1['EventId_y'].items():
#     if index<100:
#         print(value)
#     if pd.isna(value):
#         One1['adjacency_t'] = 0
#         One1['adjacency_w'] = 0
#     else:
#         One1['adjacency_t'] = 1
#         One1['adjacency_w'] = 1
#         #features_traffic = traffic2['EventId_x', '']
#         features_both = np.stack([One1['EventId_x'], One1['EventId_y'],One1['Type_x'], One1['Type_y']])#, 'Severity_x', 'Severity_y', 'TMC', 'StartTime(UTC)', 'EndTime(UTC)', 'LocationLat_x', 'LocationLng_x', 'LocationLat_y', 'LocationLng_y']) # 'City', 'State', 'ZipCode_x', 'ZipCode_y']
#
# if 'adjacency_t' in One1 and 'adjacency_w' in One1:
#     adjacency_mat = np.dot(One1['adjacency_t'].values.reshape(-1, 1), One1['adjacency_w'].values.reshape(-1, 1).T)
#     pd.DataFrame(adjacency_mat).to_csv('adj_data.csv', index=True)
#
# # print('weather csv dimension:')
# # print(weather.shape)
# #
# # print("weather Type:")
# # print(weather['Type'].value_counts(),'\n')
# # print("weather Severity:")
# # print(weather['Severity'].value_counts(),'\n')
# # print("weather State:")
# # print(weather['State'].value_counts(),'\n')
# #
# # print('traffic csv dimension:')
# # print(traffic.shape)
# # print("traffic Type:")
# # print(traffic['Type'].value_counts(),'\n')
# # print("traffic Severity:")
# # print(traffic['Severity'].value_counts(),'\n')
# # print("traffic State:")
# # print(traffic['State'].value_counts(),'\n')
# #
# #
# # # Assuming 'weather' and 'traffic' are your pandas dataframes
# # weather_type_counts = weather['Type'].value_counts()
# # weather_severity_counts = weather['Severity'].value_counts()
# # weather_state_counts = weather['State'].value_counts()
# #
# # traffic_type_counts = traffic['Type'].value_counts()
# # traffic_severity_counts = traffic['Severity'].value_counts()
# # traffic_state_counts = traffic['State'].value_counts()
# #
# # # Set up the matplotlib figure and axes
# # fig, axs = plt.subplots(4, 1, figsize=(10, 10))  # 4 rows of plots, 1 columns
# # fig2, axs2 = plt.subplots(2, 1, figsize=(25, 10))  # 2 rows of plots, 1 columns
# # # Plot for Weather Data
# # axs[0].bar(weather_type_counts.index, weather_type_counts.values)
# # axs[0].set_title('Weather Type Counts')
# # axs[0].set_ylim(0, 5000000)  # Set y-axis limit for weather type
# #
# # axs[1].bar(weather_severity_counts.index, weather_severity_counts.values)
# # axs[1].set_title('Weather Severity Counts')
# # axs[1].set_ylim(0, 5000000)  # Set y-axis limit for weather severity
# #
# # axs2[0].bar(weather_state_counts.index, weather_state_counts.values)
# # axs2[0].set_title('Weather State Counts')
# # axs2[0].set_ylim(0, 600000)  # Set y-axis limit for weather states
# #
# # # Plot for Traffic Data
# # axs[2].bar(traffic_type_counts.index, traffic_type_counts.values)
# # axs[2].set_title('Traffic Type Counts')
# # axs[2].set_ylim(0, 35000000)  # Set y-axis limit for traffic type
# #
# # axs[3].bar(traffic_severity_counts.index, traffic_severity_counts.values)
# # axs[3].set_title('Traffic Severity Counts')
# # axs[3].set_ylim(0, 35000000)  # Set y-axis limit for traffic severity
# #
# # axs2[1].bar(traffic_state_counts.index, traffic_state_counts.values)
# # axs2[1].set_title('Traffic State Counts')
# # axs2[1].set_ylim(0, 3500000)  # Set y-axis limit for traffic severity
# #
# # fig.tight_layout()
# # fig.subplots_adjust(hspace=0.4)
# #
# # fig2.tight_layout()
# # fig2.subplots_adjust(hspace=0.4)
# #
# # plt.show()
#
# # weather2["StartTime(UTC)"] = pd.to_datetime(weather2["StartTime(UTC)"], format="%Y-%m-%d %H:%M:%S")
# # weather2["EndTime(UTC)"] = pd.to_datetime(weather2["EndTime(UTC)"], format="%Y-%m-%d %H:%M:%S")
# #
# # start_date = datetime.strptime("2016-08-01 00:00:01", "%Y-%m-%d %H:%M:%S")
# # end_date = datetime.strptime("2023-12-01 00:00:01", "%Y-%m-%d %H:%M:%S")
# # interval = timedelta(minutes=60)
# # bucket_elements = []
# # while start_date <= end_date:
# #     # Check how many trips fall into this interval
# #     bucket_elements.append(weather2[((start_date + interval) >= weather2["EndTime(UTC)"])
# #                                   & (start_date <= weather2["EndTime(UTC)"])].shape[0])
# #     # Increment
# #     start_date += interval
# #
# # sns.scatterplot(x=weather2['StartTime(UTC)'], y="Event_per_hour", data=pd.DataFrame(bucket_elements, columns=["Event_per_hour"]).reset_index())
# #
# # df_plot = pd.DataFrame(bucket_elements, columns=["Event_per_hour"]).reset_index()
# # print(df_plot)
# # sns.scatterplot(x="index", y="Event_per_hour", data=df_plot)
# # plt.show()
# # look = pd.read_csv('../../quick_test_data.csv')
# # print(look['EventId_y'].count())
