import csv
import numpy as np
import pandas as pd
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON

fullData = []

con = "France"
code = "Q142"

url = 'https://query.wikidata.org/sparql'
sparql = SPARQLWrapper(url)

start = 1700
end = 2010

for i in range(start, end):
    sparql.setQuery("""
SELECT DISTINCT ?item WHERE {
  ?item p:P106 ?statement0.
  ?statement0 (ps:P106/(wdt:P279*)) wd:Q82955.
  ?item p:P27 ?statement1.
  ?statement1 (ps:P27) wd:"""+code+""".
  ?item p:P569 ?statement_2.
  ?statement_2 psv:P569 ?statementValue_2.
  ?statementValue_2 wikibase:timePrecision ?precision_2.
  FILTER(?precision_2 >= 11 )
  ?statementValue_2 wikibase:timeValue ?P569_2.
  FILTER(?P569_2 > "+"""+str(i)+"""-01-01T00:00:00Z"^^xsd:dateTime)
  ?item p:P569 ?statement_3.
  ?statement_3 psv:P569 ?statementValue_3.
  ?statementValue_3 wikibase:timePrecision ?precision_3.
  FILTER(?precision_3 >= 11 )
  ?statementValue_3 wikibase:timeValue ?P569_3.
  FILTER(?P569_3 < "+"""+str(i+1)+"""-01-01T00:00:00Z"^^xsd:dateTime)
}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results["results"]["bindings"])
    fullData += results["results"]["bindings"]
    print("Iteration", i+1, "done!")

print(fullData)
dictt = {}
pdf1 = pd.DataFrame()
vals = []

for op in fullData:
    vals.append(op["item"]["value"].split("/")[-1])

pdf2 = pd.DataFrame({con : list(set(vals))})

pdf2.to_csv(con + '.csv', index = False)