import pandas as pd
# A = ['Apple', 'Dog']
# B = ['Cat', 'OWL', 'PEACOCK']
# df1 = pd.DataFrame({'A':A})
# df2 = pd.DataFrame({'B':B})
# pd.concat([df1,df2],axis=1).to_csv('myfile.csv', index = False)

df1 = pd.read_csv("1.csv")
df2 = pd.read_csv("2.csv")
df = pd.concat([df1,df2],axis=1)
df3 = pd.read_csv("3.csv")
df = pd.concat([df,df3],axis=1)
df4 = pd.read_csv("4.csv")
df = pd.concat([df,df4],axis=1)
df5 = pd.read_csv("5.csv")
df = pd.concat([df,df5],axis=1)
df6 = pd.read_csv("6.csv")
df = pd.concat([df,df6],axis=1).to_csv('myfile.csv', index = False)