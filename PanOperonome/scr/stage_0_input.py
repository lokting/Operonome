import os
import pandas as pd

# 1. Set paths dynamically based on the project root
base_dir = os.environ.get("PROJ_BASE", os.path.dirname(os.path.dirname(__file__)))

path_to_pg_file = os.path.join(base_dir, "data", "reference", "new_PG.xlsx")
base_input_dir = os.path.join(base_dir, "data", "input")
output_folder = os.path.join(base_dir, "output", "temp_po_out")

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. Automatically detect strains from the input directory
strains = [f.replace('_operon-gene.xlsx', '') for f in os.listdir(base_input_dir) if f.endswith('_operon-gene.xlsx')]
print(f"Automatically detected {len(strains)} strains: {strains}")

if not strains:
    print("Warning: No *_operon-gene.xlsx files found in the input directory!")
    exit(1)

# 3. Build PG dictionary
print("Reading PG dictionary...")
pg_df = pd.read_excel(path_to_pg_file)
pg_id_map = {}

for _, row in pg_df.iterrows():
    pg_id = row.iloc[0]
    for localtag in row.iloc[1:].dropna():
        tags = str(localtag).split('|') if '|' in str(localtag) else [str(localtag)]
        for tag in tags:
            pg_id_map[tag.strip()] = pg_id

def replace_localtag_with_pgid_strict(localtags, pg_id_map):
    """Replace local tags with PG IDs based on the dictionary."""
    if pd.isna(localtags): return localtags
    replaced = []
    for tag in str(localtags).split(','):
        tag = tag.strip()
        replaced.append(pg_id_map.get(tag, pg_id_map.get(tag + "*", tag)))
    return ','.join(replaced)

# 4. Batch generate _PanOperon_new.xlsx
for strain in strains:
    input_file = os.path.join(base_input_dir, f'{strain}_operon-gene.xlsx')
    if not os.path.exists(input_file): continue
    
    print(f"Generating: {strain}_PanOperon_new.xlsx")
    operon_df = pd.read_excel(input_file)
    operon_df['gene'] = operon_df['localtag'].apply(lambda x: replace_localtag_with_pgid_strict(x, pg_id_map))
    
    output_path = os.path.join(output_folder, f'{strain}_PanOperon_new.xlsx')
    operon_df.to_excel(output_path, index=False)

print("Stage 0: All input files prepared successfully!")
