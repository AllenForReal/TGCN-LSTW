import pandas as pd

# Read the dataset and sort it based on the timestamp
unique_mass_nodes = pd.read_csv('unique_mass_nodes_2.csv')
unique_mass_nodes['StartTime(UTC)'] = pd.to_datetime(unique_mass_nodes['StartTime(UTC)'])
sorted_data = unique_mass_nodes.sort_values(by='StartTime(UTC)')

# Find the lowest timestamp and round it to the closest hour
min_timestamp = sorted_data['StartTime(UTC)'].min()
rounded_hour = min_timestamp.replace(minute=0, second=0, microsecond=0)

# Calculate unique hourly intervals
intervals = []
current_hour = rounded_hour
largest_timestamp = sorted_data['StartTime(UTC)'].max()

while current_hour <= largest_timestamp:
    intervals.append((current_hour, current_hour + pd.Timedelta(hours=1)))
    current_hour += pd.Timedelta(hours=1)

# Print the lowest timestamp
print("Lowest Timestamp in StartTime(UTC) column:", min_timestamp)

# Print the hourly intervals and largest timestamp
print("Hourly Intervals (Start Time - End Time):")
for interval in intervals[:20]:
    print(interval[0], "-", interval[1])
print("Largest Timestamp in StartTime(UTC) column:", largest_timestamp)

# Save the calculated intervals to a CSV file
intervals_df = pd.DataFrame(intervals, columns=['Start Time', 'End Time'])
intervals_df.to_csv('calculated_intervals.csv', index=False)
