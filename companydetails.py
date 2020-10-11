import pandas as pd


name=[]
oen=[]
ret=[]


df=pd.read_csv(r'C:/Users/Lenovo/Desktop/blockchain/data/Merge_stock.csv')
#print(df.head())
print(df.shape)
print(df.columns)

df2=df.sample(n=5)
#df2=df2.drop('Country',axis=1)
print(df2)
for index,row in df2.iterrows():
    
        name.append(row['Name'])
    
        oen.append(row['Open'])
    
        ret.append(row['Return%'])
print(name)
print(oen)
print(ret)
  