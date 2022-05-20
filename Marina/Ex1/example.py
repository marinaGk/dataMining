import pandas as pd
from sqlalchemy import null

#create DataFrame with duplicate columns
df = pd.DataFrame({'team': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
                   'points': [25, 12, 15, 14, , 23, 25, 29],
                   'assists': [25, 12, 15, 14, 19, 23, 25, 29],
                   'rebounds': [11, 8, 10, 6, 6, 5, 9, 12]})

df.columns = ['team', 'points', 'points', 'rebounds']

#view DataFrame
print(df)

df = df.loc[:,~df.columns.duplicated()]
print(df)

df.info()

