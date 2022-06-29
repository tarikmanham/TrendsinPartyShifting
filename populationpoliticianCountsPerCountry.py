import numpy as np
import pandas as pd
import csv

fullData = []

df1 = pd.read_csv("countOfTotalPoliticiansPerCountry.csv")
df2 = pd.read_csv("populationCountsOfCountries.csv")

dictt = {}

for ind in df1.index:
    # Country - [Total Population : Politician Count]
    dictt[df1['Country'][ind]] = [0, df1['Count'][ind]]

for ind in df2.index:
    if(df2['Country'][ind] in dictt.keys()):
        dictt[df2['Country'][ind]][0] = df2['Population'][ind]


print(dictt)

cols = ['Country', 'Population Count', 'Politician Count']
country = []
pops = []
pols = []

for k, v in dictt.items():
    country.append(k)
    pops.append(v[0])
    pols.append(v[1])

dict = {cols[0]: country, cols[1]: pops, cols[2]: pols}

newDF = pd.DataFrame(dict)

newDF.to_csv('population_politician_count.csv', index=False)

