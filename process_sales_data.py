import pandas as pd
import os

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Load all three CSV files
data_files = [
    'data/daily_sales_data_0.csv',
    'data/daily_sales_data_1.csv',
    'data/daily_sales_data_2.csv'
]

# Combine all data using generator expression (memory efficient)
df_all = pd.concat((pd.read_csv(file) for file in data_files), ignore_index=True)

# Filter for only Pink Morsels and explicitly copy to avoid SettingWithCopyWarning
df_pink = df_all[df_all['product'].str.lower() == 'pink morsel'].copy()

# Remove $ symbol safely (no regex warnings) and convert to float
df_pink['price'] = df_pink['price'].str.replace('$', '', regex=False).astype(float)

# Calculate sales (price × quantity)
df_pink['sales'] = df_pink['price'] * df_pink['quantity']

# Select required columns and rename in one step (more readable)
df_output = df_pink[['sales', 'date', 'region']].rename(columns={
    'sales': 'Sales',
    'date': 'Date', 
    'region': 'Region'
})

# Save to output file
output_path = 'data/processed_sales_data.csv'
df_output.to_csv(output_path, index=False)

# Professional summary output
print("✓ Processing complete!")
print("✓ Filtered for Pink Morsels only")
print("✓ Created Sales field (Price × Quantity)")
print(f"✓ Output saved to {output_path}")
print(f"✓ Total rows processed: {len(df_output)}")
print("\nFirst 5 rows of output:")
print(df_output.head())
