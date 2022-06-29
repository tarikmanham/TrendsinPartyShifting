import csv
import numpy as np
import pandas as pd
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON

fullData = []
url = 'https://query.wikidata.org/sparql'
sparql = SPARQLWrapper(url)

df = pd.read_csv("countryCode.csv")
df = df.sort_values("countryLabel")
columnData = df["countryCode"].to_list()
countryNames = df["countryLabel"].to_list()
# columnData = [x for x in codes if str(x) != 'nan']

print("The no of countries:", len(columnData))

df.head(5)

start = 180
end = 240

for i in range(start, end):
    sparql.setQuery("""
select distinct ?item ?itemLabel ?countryLabel ?itemDescription ?dob where {
  ?item  wdt:P106 wd:Q82955;
         wdt:P27 wd:"""+columnData[i]+""";
         wdt:P27 ?country;
         wdt:P569 ?dob.
  
    SERVICE wikibase:label {bd:serviceParam wikibase:language "en,nl" }
  }
ORDER BY DESC(?sitelinks)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print(results["results"]["bindings"])
    fullData.append(results["results"]["bindings"])
    print("Iteration", i+1, "done!")


dictt = {}
pdf1 = pd.DataFrame()
pdf2 = pd.DataFrame()
pdf3 = pd.DataFrame()
counter = start
for op in fullData:
    vals = []
    for j in range(len(op)):
        vals.append(op[j]["item"]["value"].split("/")[-1])

    # dictt[countryNames[counter]] = vals

    pdf1 = pdf3
    pdf2 = pd.DataFrame({countryNames[counter] : list(set(vals))})
    pdf3 = pd.concat([pdf1,pdf2],axis=1)
    counter += 1


# print(CC)
    
# dict = {'PoliticianID': CC}
# dFrame = pd.DataFrame(dictt)
# print(dictt)
pdf3.to_csv('5' + '.csv', index = False)

