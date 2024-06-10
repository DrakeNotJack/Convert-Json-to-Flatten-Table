import pandas as pd
from pandas import json_normalize
import json

data1 = pd.read_json("file_path")

def flatten_json(json_file, prefix=''):
    out = {}
    for key, value in json_file.items():
        if isinstance(value, dict):
            deeper = flatten_json(value, prefix + key + '.')
            out.update(deeper)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    deeper = flatten_json(item, prefix + key + f'[{i}].')
                    out.update(deeper)
                else:
                    out[prefix + key + f'[{i}]'] = item
        else:
            out[prefix + key] = value
    return out

df = pd.DataFrame()

for n in range(len(data1)):
    #print(n)

    #Suppose column1 contains json format data
    datapiece = data1['column1'][n]

    json_part = flatten_json(datapiece)
    
    #print(json_part)
    
    df_part = json_normalize(json_part)
    
    
    #print(len(df_part))
    
    df = pd.concat([df, df_part])
    
df