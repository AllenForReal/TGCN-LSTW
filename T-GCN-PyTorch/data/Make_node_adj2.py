import pandas as pd
import torch
import numpy as np
import math
#
# # Function to compute haversine distance between two sets of points in PyTorch
# def haversine_distance_torch(lat1, lon1, lat2, lon2):
#     # Convert degrees to radians
#     lat1, lon1, lat2, lon2 = [x * math.pi / 180 for x in [lat1, lon1, lat2, lon2]]
#
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#
#     a = torch.sin(dlat / 2.0) ** 2 + torch.cos(lat1) * torch.cos(lat2) * torch.sin(dlon / 2.0) ** 2
#     c = 2 * torch.asin(torch.sqrt(a))
#     distance = 3959 * c  # 3959 is the radius of the Earth in miles
#     return distance
#
#
# # Load the CSV data into a pandas DataFrame
# df = pd.read_csv('quick_test_data.csv')
# sampled_df = df.sample(frac=0.02)
# sampled_df.to_csv('quick_test_data2.csv', index=False)
#
# # Convert latitude and longitude to PyTorch tensors
# coords = torch.tensor(df[['LocationLat_x', 'LocationLng_x'],['LocationLat_y', 'LocationLng_y']].values).to(torch.float32)
#
# # Use GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# coords = coords.to(device)
#
# # Calculate pairwise distance matrix
# lat = coords[:, 0].unsqueeze(1)
# lon = coords[:, 1].unsqueeze(1)
# distances_miles = haversine_distance_torch(lat, lat.t(), lon, lon.t())
#
# # Define your connectivity condition (e.g., within 20 miles)
# connectivity_condition = distances_miles <= 20
#
# # Convert boolean connectivity condition to integer adjacency matrix
# adjacency_matrix = connectivity_condition.to(torch.int)
#
# # Move the adjacency matrix back to CPU for further operations with pandas
# adjacency_matrix = adjacency_matrix.cpu()
#
# # Save the adjacency matrix as a CSV file
# adjacency_df = pd.DataFrame(adjacency_matrix.numpy(), columns=df['EventId_y'], index=df['EventId_x'])
# # adjacency_df = adjacency_df - np.eye(adjacency_df.shape[0]) # Keep connection to itself?
# adjacency_df.to_csv('adjacency_matrix.csv')
#
# feature_columns = ['Type_x', 'Severity_x', 'Type_y', 'Severity_y', 'Distance(mi)', 'Side']
# feature_matrix = sampled_df[feature_columns].values
# print(feature_matrix.shape)
# # Create a DataFrame for the feature matrix
# feature_df = pd.DataFrame(feature_matrix, columns=feature_columns, index=sampled_df['EventId_x'])
#
# # Save the feature matrix as a CSV file
# feature_df.to_csv('feature_matrix.csv')


# Load the CSV data into a pandas DataFrame
df = pd.read_csv('quick_test_data.csv')

print("weather Type:")
print(df['Type_y'].value_counts(),'\n')
print("weather Severity:")
print(df['Severity_y'].value_counts(),'\n')
print("weather State:")
print(df['State'].value_counts(),'\n')
print("traffic Type:")
print(df['Type_x'].value_counts(),'\n')
print("Traffic Severity:")
print(df['Severity_x'].value_counts(),'\n')
print("Traffic State:")
print(df['State'].value_counts(),'\n')

# One hot encoding:

df['Severity_y'] = df['Severity_y'].fillna(0)
df['Type_y'] = df['Type_y'].fillna(0)
df['EventId_y'] = df['EventId_y'].fillna(0)
df.to_csv('quick_test_data.csv', index=False)
def modify_event_id(event_id):
    event_id = str(event_id)
    if event_id.startswith('T-'):
        return '0' + event_id[2:]
    elif event_id.startswith('W-'):
        return '1' + event_id[2:]
    else:
        return event_id


# data = {
#     'Type_t': ['Congestion', 'Accident', 'Flow-Incident','Broken-Vehicle', 'Lane-Blocked','Construction'],
#     'Type_w': ['Rain', 'Fog', 'Cold', 'Precipitation', 'Snow', 'Storm', 'Hail'],
#     'Severity_w': ['Light', 'Moderate', 'Severe', 'Heavy', 'UNK','Other']
# }
# df = pd.DataFrame(data)
#
# # Perform one-hot encoding
# trafficType_dummies = pd.get_dummies(df['Type_x'], prefix='Type_t')
# weatherType_dummies = pd.get_dummies(df['Type_y'], prefix='Type_w')
# weatherSeverity_dummies = pd.get_dummies(df['Severity_y'], prefix='Severity_w')
# # Concatenate the original DataFrame with the new one-hot encoded columns
# df_encoded = pd.concat([df, trafficType_dummies, weatherType_dummies, weatherSeverity_dummies], axis=1)

df['TrafficTypeEncoded']=pd.factorize(df['Type_x'])[0] + 1
df['WeatherTypeEncoded']=pd.factorize(df['Type_y'])[0] + 1
df['WeatherSeverityEncoded']=pd.factorize(df['Severity_y'])[0] + 1
df['CityEncoded']=pd.factorize(df['City'])[0] + 1
df['StateEncoded']=pd.factorize(df['State'])[0] + 1

df.rename(columns = {'Severity_x':'TrafficSeverityEncoded'}, inplace=True)
# Optionally, drop the original categorical columns if they are no longer needed
#df_encoded.drop(['Type_x', 'Type_y', 'Severity_y'], axis=1, inplace=True)

print(df)
# End of One hot encoding

# Apply the function to the 'EventId' columns
df['EventId_x'] = df['EventId_x'].apply(modify_event_id)
df['EventId_y'] = df['EventId_y'].apply(modify_event_id)

df_ga = df[df['State'] == 'GA']
df_fl = df[df['State'] == 'FL']
df_fl2 = df_fl[:8000]
n = len(df_fl2)

#Creating the adjacency_mat by dot product
adjacency_values = np.dot(df_fl2['adjacency'].values.reshape(-1, 1), df_fl2['adjacency'].values.reshape(-1, 1).T)

# Creating DataFrame for the adjacency matrix with EventId_y as row indices, EventId_x as column indices
adjacency_mat_df = pd.DataFrame(adjacency_values, index=df_fl2['EventId_y'], columns=df_fl2['EventId_x'])

# Saving the adjacency matrix as CSV
# Check if index 0 exists in the DataFrame
if 0 in adjacency_mat_df.index:
    adjacency_mat_df = adjacency_mat_df.drop(index=0) #dropping the EventId column because GCN module does not take or need it
else:
    # Remove the first row of the DataFrame instead
    adjacency_mat_df = adjacency_mat_df.iloc[1:]

adjacency_mat_df.to_csv('adjacency_matrix.csv',index=False)
df_fl2.to_csv('Florida_sample_encoded.csv',index=False)

# Define feature columns including 'Distance' and 'Side'
feature_columns = ['EventId_y','TrafficTypeEncoded', 'TrafficSeverityEncoded', 'WeatherTypeEncoded', 'WeatherSeverityEncoded', 'CityEncoded', 'StateEncoded']
feature_matrix = df_fl2[feature_columns].values
# Create a DataFrame for the feature matrix
feature_df = pd.DataFrame(feature_matrix, columns=feature_columns, index=df_fl2['EventId_x'])

# Save the feature matrix as a CSV file
feature_df.to_csv('feature_matrix.csv')

print("Completed. Adjacency matrix and feature matrix saved as CSV files.")
feature_df.head(n=10)

print(len(adjacency_mat_df))
print(len(feature_df))
