# %%
import json
from msilib.schema import CompLocator
import pandas as pd
import os
records =[("escpresso", "$5" ),('cappucino','$10')]
df= pd.DataFrame.from_records(records,columns=['items','price'])

# %% 
print(df)
# %%
sample_JSON = os.path.join('collection','artworks','a','000','a00001-1035.json')
JSON_ROOT = os.path.join('collection','artworks')

def get_record_from_file(file_path, KEYS_TO_USE):
    with open(file_path) as f:
        content = json.load(f)
    reocord=[]
    for field in KEYS_TO_USE:
        reocord.append(content[field])
    return tuple(reocord)
        
KEYS_TO_USE = ['id','all_artists','title','medium','acquisitionYear','height','width']



# %%
sample_record = get_record_from_file(sample_JSON, KEYS_TO_USE)
# %%
print(sample_record)
# %%
def read_artworks_from_json(keys_to_use):
    artworks=[]
    for root,_,files in os.walk(JSON_ROOT):
        for f in files:
            if f.endswith('json'):
                try:
                    reocord = get_record_from_file(os.path.join(root,f),keys_to_use)
                except:
                    pass
                finally:  
                    artworks.append(reocord)
                
    df = pd.DataFrame(artworks,columns=keys_to_use)
    df.set_index('id', inplace=True)
    return df
# %%
df2= read_artworks_from_json(KEYS_TO_USE)

# %%
# %%
print(df2.head())
# %%
artists = df2['all_artists']
print(len(artists))
pd.unique(artists)
print(len(pd.unique(artists)))
# %%
df2.to_csv('tat.csv')
# %%