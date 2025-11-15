import json
import pandas as pd
import os

# Print gaps and title for terminal output
print("\n" * 3)
print("C. Fix JSON Data Inconsistencies")
print("-" * 40)
print("\n")

# Set working directory where your JSON file exists
data_folder = r'C:\Users\ub13-glab-015\Desktop\final_lab_exam'
os.chdir(data_folder)

print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Use actual JSON filename from your folder
json_file = 'auxiliary_metadata.json'

try:
    with open(json_file, 'r') as f:
        data = json.load(f)
    print(f"Loaded JSON data from '{json_file}'.\n")
except FileNotFoundError:
    print(f"Error: '{json_file}' not found. Please check filename and path.")
    exit()

# Convert to DataFrame for easier processing if JSON is list of dicts
df = pd.json_normalize(data)

# Standardize inconsistent field names
rename_map = {
    'status': 'conservation_status',
    'conservation': 'conservation_status',
    'habitats': 'habitat_type',
    'habitat': 'habitat_type',
}
df.rename(columns=rename_map, inplace=True)

# Fix diet typos (e.g., "omnivor" -> "omnivore")
diet_cols = [col for col in df.columns if 'diet' in col.lower()]
def fix_diet_typo(val):
    if isinstance(val, str):
        if val.lower() == 'omnivor':
            return 'omnivore'
    return val

for col in diet_cols:
    df[col] = df[col].apply(fix_diet_typo)

# Standardize habitat_type values (expand as needed)
habitat_map = {
    'rainforest': 'Rainforest',
    'rain forest': 'Rainforest',
    'savanna': 'Savanna',
    'grassland': 'Grassland',
    'woods': 'Forest',
    'forest': 'Forest',
}
df['habitat_type'] = df['habitat_type'].replace(habitat_map)

print("Sample data after fixing inconsistencies:")
print(df.head())

# Convert cleaned DataFrame back to JSON list of dicts
fixed_data = df.to_dict(orient='records')

# Save fixed JSON to new file
fixed_filename = 'fixed_data.json'
with open(fixed_filename, 'w') as f:
    json.dump(fixed_data, f, indent=4)

print(f"\nFixed JSON data saved to '{fixed_filename}'.\n")
