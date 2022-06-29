"""
Data Storage Format

{
    Name : [
                DOB,
                Place of Birth,
                Sex,
                {
                                .
                                .
                                .
                    Political Party i : [
                                            start time,
                                            end time
                                        ]
                                .
                                .
                                .
                }
           ]
    ]
}

"""

import datetime
from dateutil import parser
import numpy as np
import pandas as pd
from collections import OrderedDict
import os
from os import listdir
from os.path import isfile, join

def getName(xxx):
    return os.path.splitext(xxx)[0]

myPath = os.path.join(os.getcwd(), 'AllCountries')
# myPath = os.path.join(os.getcwd(), 'CountriesRanOnMukulRoyCode')

fileNames = [f for f in listdir(myPath) if isfile(join(myPath, f))]
reqdData = ['date of birth', 'member of political party', 'sex or gender', 'place of birth']

# print(fileNames)

for fileName in fileNames:

    df = pd.read_csv(myPath + '/' + fileName)


    print("Reading the file ", fileName)

    del df['Unnamed: 0']

    peopleInfo = {}

    for i in df.index:

        if(df['personLabel'][i] not in peopleInfo.keys()):
            peopleInfo[df['personLabel'][i]] = [None, None, None, {}]
        if(df['wdLabel'][i] in reqdData):
            ourLabelVal = df['ps_Label'][i]
            if(df['wdLabel'][i] == 'member of political party' and ( not pd.isnull(ourLabelVal) )):
                subKey = df['wdpqLabel'][i]
                subVal = df['pq_Label'][i]
                # If the corresponding political party was not added
                if(ourLabelVal not in peopleInfo[df['personLabel'][i]][3]):
                    peopleInfo[df['personLabel'][i]][3][ourLabelVal] = [None, None]
                if(subKey == 'start time' and (not pd.isnull(subVal) )):
                    peopleInfo[df['personLabel'][i]][3][ourLabelVal][0] = subVal
                if(subKey == 'end time' and (not pd.isnull(subVal) )):
                    peopleInfo[df['personLabel'][i]][3][ourLabelVal][1] = subVal

            elif(df['wdLabel'][i] == 'date of birth' and ( not pd.isnull(ourLabelVal) )):
                peopleInfo[df['personLabel'][i]][0] = ourLabelVal
            elif(df['wdLabel'][i] == 'sex or gender' and ( not pd.isnull(ourLabelVal) )):
                peopleInfo[df['personLabel'][i]][2] = ourLabelVal
            elif(df['wdLabel'][i] == 'place of birth' and ( not pd.isnull(ourLabelVal) )):
                peopleInfo[df['personLabel'][i]][1] = ourLabelVal

    # print(peopleInfo)

    # count = 0
    nameList = []
    typeOfData = []
    dataValue = []
    startDate = []
    endDate = []

    count = 0
    for i in peopleInfo:

        if(len(peopleInfo[i][3]) >= 3):
            count += 1

            # Adding DOB
            nameList.append(i)
            typeOfData.append("date of birth")
            dataValue.append(peopleInfo[i][0])
            startDate.append("")
            endDate.append("")

            # Adding POB
            nameList.append(i)
            typeOfData.append("place of birth")
            dataValue.append(peopleInfo[i][1])
            startDate.append("")
            endDate.append("")

            # Adding Sex
            nameList.append(i)
            typeOfData.append("sex or gender")
            dataValue.append(peopleInfo[i][2])
            startDate.append("")
            endDate.append("")

            # Adding Political Parties
            for j in peopleInfo[i][3]:
                nameList.append(i)
                typeOfData.append("member of political party")
                dataValue.append(j)
                startDate.append(peopleInfo[i][3][j][0])
                endDate.append(peopleInfo[i][3][j][1])

    dict = {'Name': nameList, 'Type-Of-Data': typeOfData, 'Data-Value': dataValue, 'Start-Date': startDate, 'End-Date': endDate}
    dFrame = pd.DataFrame(dict)

    dFrame.to_csv('CleanedCountries2/' + str(count) + '_' + getName(fileName) + '.csv', index = False)