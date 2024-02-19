import pandas as pd

# file_path = r'D:\GCN + LSTM\T-GCN-PyTorch\quick_test_data.csv'
#
# # Read the CSV file into a pandas DataFrame
# df = pd.read_csv(file_path)
#
# # Count the total number of rows
# total_rows = len(df)
#
# print("Total number of rows:", total_rows)

import pandas as pd
import time

import pandas as pd
import time

# Start timing
start_time = time.time()

weather2 = pd.read_csv(r'D:\GCN + LSTM\T-GCN-PyTorch\LSTW\weather_sample.csv')
traffic2 = pd.read_csv(r'D:\GCN + LSTM\T-GCN-PyTorch\LSTW\traffic_full.csv')

print(traffic2.head(10))

traffic2['StartTime(UTC)'] = pd.to_datetime(traffic2['StartTime(UTC)'])
weather2['StartTime(UTC)'] = pd.to_datetime(weather2['StartTime(UTC)'])

# Drop duplicates
traffic2 = traffic2.drop_duplicates(subset=['State', 'City', 'StartTime(UTC)'])
weather2 = weather2.drop_duplicates(subset=['State', 'City', 'StartTime(UTC)'])

# Drop rows with NaN in specific columns
traffic2 = traffic2.dropna(subset=['State', 'City', 'StartTime(UTC)', 'LocationLat', 'LocationLng', 'ZipCode'])
weather2 = weather2.dropna(subset=['State', 'City', 'StartTime(UTC)', 'LocationLat', 'LocationLng', 'ZipCode'])

# Sort both left and right DataFrames by 'StartTime(UTC)'
weather2 = weather2.sort_values(by=['StartTime(UTC)'])
traffic2 = traffic2.sort_values(by=['StartTime(UTC)'])

One1 = pd.merge_asof(
    weather2,
    traffic2,
    on='StartTime(UTC)',
    by=['State', 'City'],
    tolerance=pd.Timedelta(hours=1),
    direction='nearest'
)

# Count the total number of rows
total_rows = len(One1)

print("Total number of rows:", total_rows)

# Save merged data to a new CSV file without the adjacency column
One1.to_csv('quick_data_2.csv', index=False)
print("Merged data has been saved as 'merged_data.csv'")

# Calculate and print execution time
end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")


