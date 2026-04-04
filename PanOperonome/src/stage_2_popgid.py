import pandas as pd
import os


# 1. Set paths dynamically

base_dir = os.environ.get("PROJ_BASE", os.path.dirname(os.path.dirname(__file__)))

path_to_pg_file = os.path.join(base_dir, "data", "reference", "PG.xlsx")
npo_homo_input = os.path.join(base_dir, "data", "reference", "nPO_homo.xlsx")
final_output = os.path.join(base_dir, "output", "nPO_pgid.xlsx")


# 2. Build dictionary from PG.xlsx

print("Reading PG.xlsx to build dictionary...")
pg_df = pd.read_excel(path_to_pg_file)
pg_id_map = {}

for index, row in pg_df.iterrows():
    pg_id = row.iloc[0]
    for localtag in row.iloc[1:]:
        if pd.isna(localtag) or str(localtag).strip() == '-':
            continue
            
        if '|' in str(localtag):
            for tag in str(localtag).split('|'):
                pg_id_map[tag.strip()] = pg_id
        else:
            pg_id_map[str(localtag).strip()] = pg_id

if "-" in pg_id_map:  
    del pg_id_map["-"]

print(f"Dictionary built. Total mapped genes: {len(pg_id_map)}")


# 3. Execute replacement and output file

print(f"Replacing tags in {os.path.basename(npo_homo_input)}...")
df_homo = pd.read_excel(npo_homo_input)

columns_to_drop = ['Single/Mul', 'single', 'multi', 'sum'] 
existing_cols_to_drop = [col for col in columns_to_drop if col in df_homo.columns]

if existing_cols_to_drop:
    df_homo = df_homo.drop(columns=existing_cols_to_drop)
    print(f"Automatically removed unnecessary columns: {existing_cols_to_drop}")

def partial_replace(cell_value, mapping_dict):
    cell_str = str(cell_value)
    if cell_str == 'nan' or cell_str == '-':
        return cell_value
        
    for key, value in mapping_dict.items():   
        if key in cell_str:  
            cell_str = cell_str.replace(key, value)  
    return cell_str 

if hasattr(df_homo, 'map'):
    df_homo = df_homo.map(lambda cell: partial_replace(cell, pg_id_map))
else:
    df_homo = df_homo.applymap(lambda cell: partial_replace(cell, pg_id_map))

df_homo.to_excel(final_output, index=False)
print(f"Stage 2: File generated successfully at: {final_output}")
