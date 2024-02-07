import pandas as pd

# Load your DataFrame
df = pd.read_csv('florida_nodes.csv')

df['StartTime(UTC)'] = pd.to_datetime(df['StartTime(UTC)'])

# Now to group them, first sort by time
df = df.sort_values(by='StartTime(UTC)')

# Create a list to hold groups
groups = []

# Create the first group with the first row
current_group = [df.iloc[0]]

for i in range(1, len(df)):
    # Calculate time difference from the last element in the current group
    time_diff = df.iloc[i]['StartTime(UTC)'] - current_group[-1]['StartTime(UTC)']

    # Check if the difference is less than an hour and the location is different
    if time_diff <= pd.Timedelta(hours=1) and (
            df.iloc[i]['LocationLat_x'] != current_group[-1]['LocationLat_x'] or df.iloc[i]['LocationLng_x'] !=
            current_group[-1]['LocationLng_x']):
        current_group.append(df.iloc[i])
    else:
        # If not, save the current group and start a new one
        groups.append(current_group)
        current_group = [df.iloc[i]]

# Don't forget to add the last group if it's not empty
if current_group:
    groups.append(current_group)

# Now 'groups' is a list of lists, where each sublist is a group of events within 1 hour of each other
# If you need to process these groups or convert them back into DataFrames:
grouped_dfs = [pd.DataFrame(group) for group in groups]

# Now you can process each group (DataFrame) individually
# For example, you can print out the groups or save them to separate CSV files.
for i, group_df in enumerate(grouped_dfs):
    print(f"Group {i}:")
    print(group_df)
    group_df.to_csv(f'grouped_csv/group_{i}.csv', index=False)
