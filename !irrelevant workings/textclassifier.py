import pandas as pd
import random

p = 0.01  # 1% of the lines
# keep the header, then take only 1% of lines
# if random from [0,1] interval is greater than 0.01 the row will be skipped
df = pd.read_csv(
         'query_file.csv',
         header=0, 
         skiprows=lambda i: i>0 and random.random() > p
)

df['category_id'] = df['Label'].factorize()[0]
category_id_df = df[['Label', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'Label']].values)
df.head()