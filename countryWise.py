import requests
import csv
import numpy as np
import pandas as pd
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON

fullData = []
url = 'https://query.wikidata.org/sparql'
sparql = SPARQLWrapper(url)
country = "Nepal"

df = pd.read_csv("politicianIDs.csv")

print("--------------------------------------------------------------")

print("Shape of the CSV : ", df.shape)
print("--------------------------------------------------------------")

print("--------------------------------------------------------------")
print("Dataset Head")
print(df.head())
print("--------------------------------------------------------------")

print("--------------------------------------------------------------")
print("Column names - ", df.columns.to_list())
columnNames = df.columns.to_list()
print("--------------------------------------------------------------")

codes = df[country].to_list()
columnData = [x for x in codes if str(x) != 'nan']

print(len(columnData))

for i in range(len(columnData)):
    sparql.setQuery("""
SELECT ?personLabel ?wdLabel ?ps_Label ?wdpqLabel ?pq_Label {
  VALUES (?person) {(wd:"""+columnData[i]+""")}

  ?person ?p ?statement .
  ?statement ?ps ?ps_ .

  ?wd wikibase:claim ?p.
  ?wd wikibase:statementProperty ?ps.

  OPTIONAL {
  ?statement ?pq ?pq_ .
  ?wdpq wikibase:qualifier ?pq .
  }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} ORDER BY ?wd ?statement ?ps_
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    fullData.append(results)

print(fullData)

personLabel = []
wdLabel = []
ps_Label = []
wdpqLabel = []
pq_Label = []

for i in fullData:
    op = i["results"]["bindings"]
    for j in op:
        personLabel.append(j["personLabel"]["value"])
        wdLabel.append(j["wdLabel"]["value"])
        ps_Label.append(j["ps_Label"]["value"])
        if 'wdpqLabel' in j.keys():
            wdpqLabel.append(j["wdpqLabel"]["value"])
        else:
            wdpqLabel.append(np.nan)
        if 'pq_Label' in j.keys():
            pq_Label.append(j["pq_Label"]["value"])
        else:
            pq_Label.append(np.nan)
    
dict = {'personLabel': personLabel, 'wdLabel': wdLabel, 'ps_Label': ps_Label, 'wdpqLabel': wdpqLabel, 'pq_Label': pq_Label}
dFrame = pd.DataFrame(dict)

dFrame.to_csv(country + '.csv')

