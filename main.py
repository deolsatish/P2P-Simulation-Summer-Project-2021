import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
from time import sleep
import json
import plotly.graph_objects as go


# This function is just so that I can use print statements and change default to 0, thus it sill not print
def printf(str, print_bool=1):
    if (print_bool):
        print(str)


# This is the file path for the normal dataset
folderpath = './PreppedData'
# This is the filepath for the dataset with Unix Timestamps as date and time
unixdatapath = './UnixData'

# This variable changes the code a bit to accomodate for the unix timestamps
# The code converts Unix Timestamps into datetime so that it we can sort the data by weeks and months as well
unixdatetimeformatbool = 0

# Index+column is 0 because in the database the second column is dataid and the second column is date&time
index_column = 0

# Database_list is the variable which contains the array of dataframes(database) of each house
database_list = []
# home_list will contains the name of each house, it will read all the folder names within Data folder
home_list = []

# This variable stores the features that are common for all houses so that we can compare them
intersectedheaders = []

# This is just to initalize the startdate and enddate vairbles with datetime type
startdate = datetime.datetime.now
enddate = datetime.datetime.now


def functioncsvfilenameandpath(path='./'):
    # Path is the path where you want to search

    # this is the extension you want to detect
    extension = '.csv'

    csvfilepaths = []
    csvfilenames = []

    # print(path)

    for root, dirs_list, files_list in os.walk(path):
        for file_name in files_list:
            if os.path.splitext(file_name)[-1] == extension:
                file_name_path = os.path.join(root, file_name)
                if (file_name.find('') != -1):
                    csvfilenames.append(file_name)
                    csvfilepaths.append(file_name_path)
                # print(file_name)
                # print(file_name_path)   # This is the full path of the filter file

    # printf(csvfilenames)
    # printf(csvfilepaths)
    return csvfilenames, csvfilepaths


database_list = []

csvfilenames, csvfilepaths = functioncsvfilenameandpath(folderpath)

csvfilenames.sort()
csvfilepaths.sort()

printf(csvfilenames)

for i in range(len(csvfilenames)):
    df = pd.read_csv(csvfilepaths[i], index_col=0, parse_dates=True)
    df = df.fillna(0)
    database_list.append(df)
    home_list.append(csvfilenames[i].replace('.csv', ''))


homechoice=0


for x in range(len(database_list)):
    df=database_list[x]
    database_list[x] = df.loc[:, (df != 0).any(axis=0)]
    # for i in range(len(database_list[homechoice].columns.to_list())):
    #     if(not((database_list[homechoice][i] == 0).all())):

df=database_list[0].copy()
df=df.sort_index()
fheaders=df.columns.to_list()

print(df.columns.to_list())

grouped=df.groupby([df.index.hour, df.index.minute])

fig = go.Figure()
for i in range(len(fheaders)):
    fig.add_trace(go.Scatter(x=grouped.index.to_numpy(), y=grouped[fheaders[i]].to_numpy(),
                                mode='lines',
                                name=fheaders[i]))
fig.show()


# class House:
#     def __init__(self, name, appliances_name, data, no_of_people):
#         self.name = name
#         self.appliances_name = appliances_name
#         self.data = data
#         self.no_of_people = no_of_people


# header = database_list[0].columns.to_list()

# h1data = database_list[0].copy()
# # h1data=h1data.reset_index()

# data = h1data.values.tolist()

# house1 = House(home_list[0], header, data, 1)

# result = h1data.to_json(orient="columns")
# parsed = json.loads(result)
# json.dumps(parsed, indent=4)

# h1 = {
#     "name": home_list[0],
#     "appliance_name": header,
#     "data": parsed,
#     "no_of_people": 1

# }

# with open("sample.json", "w") as outfile:
#     outfile.write(json.dumps(h1, indent=4))

# # h1load = json.load()


from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')

print(DATABASE_URL)