import os
import pandas as pd
import json

# Print title and gap for clarity
print("\n" * 3)
print("D. Demerge All Datasets - Merge on Normalized Animal Names")
print("-" * 60)
print("\n")

# Set working directory to where your files exist
data_folder = r'C:\Users\ub13-glab-015\Desktop\final_lab_exam'
os.chdir(data_folder)

print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Load primary dataset (zoo.csv)
zoo_df = pd.read_csv('zoo.csv')
print("\nLoaded zoo.csv - sample data:")
print(zoo_df.head())

# Load auxiliary metadata JSON file
with open('auxiliary_metadata.json', 'r') as f:
    aux_data = json.load(f)
aux_df = pd.json_normalize(aux_data)
print("\nLoaded auxiliary_metadata.json - sample data:")
print(aux_df.head())

# Normalize animal names (lowercase) in both dataframes for accurate merge
zoo_df['animal_name_norm'] = zoo_df['animal_name'].str.lower()
aux_df['animal_name_norm'] = aux_df['animal_name'].str.lower()

# Merge datasets on normalized animal names (left join preserves all zoo data)
merged_df = pd.merge(
    zoo_df,
    aux_df.drop(columns=['animal_name']),  # drop duplicate animal_name column from aux_df
    how='left',
    on='animal_name_norm',
    suffixes=('_zoo', '_aux')
)

print("\nMerged dataset sample (left join):")
print(merged_df.head())

# Identify animals from zoo.csv missing in auxiliary metadata
missing_in_aux = merged_df[merged_df.isnull().any(axis=1)][['animal_name', 'animal_name_norm']].drop_duplicates()
print("\nAnimals present in zoo.csv but missing from auxiliary data:")
print(missing_in_aux)

# Clean up by dropping 'animal_name_norm'
merged_df.drop(columns=['animal_name_norm'], inplace=True)

# Save merged dataset to CSV
merged_filename = 'merged_zoo_aux.csv'
merged_df.to_csv(merged_filename, index=False)
print(f"\nMerged dataset saved to '{merged_filename}'.\n")
