import pandas as pd
import os

# Load all three CSV files
data_files = [
    'data/daily_sales_data_0.csv',
    'data/daily_sales_data_1.csv',
    'data/daily_sales_data_2.csv'
]

# Combine all data
combined_data = []
for file in data_files:
    df = pd.read_csv(file)
    combined_data.append(df)

# Concatenate all dataframes
df_all = pd.concat(combined_data, ignore_index=True)

# Filter for only Pink Morsels
df_pink = df_all[df_all['product'].str.lower() == 'pink morsel']

# Remove the $ symbol from price and convert to float
df_pink['price'] = df_pink['price'].str.replace('$', '').astype(float)

# Calculate sales (price × quantity)
df_pink['sales'] = df_pink['price'] * df_pink['quantity']

# Select only the required columns: Sales, Date, Region
df_output = df_pink[['sales', 'date', 'region']].copy()

# Rename columns to match output format
df_output.columns = ['Sales', 'Date', 'Region']

# Save to output file
output_path = 'data/processed_sales_data.csv'
df_output.to_csv(output_path, index=False)

print(f"✓ Processing complete!")
print(f"✓ Filtered for Pink Morsels only")
print(f"✓ Created Sales field (Price × Quantity)")
print(f"✓ Output saved to {output_path}")
print(f"✓ Total rows processed: {len(df_output)}")
print(f"\nFirst 5 rows of output:")
print(df_output.head())
