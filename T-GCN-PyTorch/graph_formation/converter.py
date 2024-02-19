# import pandas as pd
# import csv
# # Set the input CSV file path and name (without double quotes)
# input_csv_file = r'D:\RA work\traffic_full.csv'
#
# # Set the number of rows to read (e.g., 10,000)
# num_rows_to_read = 10000
#
# # Read the first num_rows_to_read rows from the CSV file into a Pandas DataFrame
# df = pd.read_csv(input_csv_file, nrows=num_rows_to_read)
#
# # Now you have a DataFrame 'df' with the first 10,000 rows of the CSV file.
#
#
# # Save the first num_rows_to_save rows as a separate CSV file
# output_csv_file = r'D:\GCN + LSTM\T-GCN-PyTorch\LSTW\traffic_sample_crop.csv.csv'
# df.head(num_rows_to_read).to_csv(output_csv_file, index=False)


import pandas as pd

# Read the original CSV file into a DataFrame
df = pd.read_csv('../quick_test_data.csv')

# Get the last column index (assuming zero-based indexing)
last_column_index = df.columns.get_loc('adjacency')

print(last_column_index)

# Filter rows where the last column (index) has a value of 1
filtered_df = df[df.iloc[:, 29] == 1]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('all_nodes.csv', index=False)












