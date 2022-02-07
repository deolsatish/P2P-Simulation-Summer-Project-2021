import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
from time import sleep
import json
import plotly.graph_objects as go
import random
import time
import pytz

#summation_exception_column_list is required to tell the code which features to exempt from Total Usage summation
summation_exception_column_list=['use','grid','solar','solar2','Total Usage','leg1v','leg2v','dataid','localminute','datetimeindex']
datetimecolumnname='datetimeindex'
unixdatetimecolumnname='UnixTimeStamp'


# This function is just so that I can use print statements and change default to 0, thus it sill not print
def printf(str, print_bool=1):
    if (print_bool):
        print(str)

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')

print(DATABASE_URL)

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



# This functions helps in reordering Columns
def reorder_columns(dataframe, col_name, position):
    """Reorder a dataframe's column.
    Args:
        dataframe (pd.DataFrame): dataframe to use
        col_name (string): column name to move
        position (0-indexed position): where to relocate column to
    Returns:
        pd.DataFrame: re-assigned dataframe
    """
    temp_col = dataframe[col_name]
    dataframe = dataframe.drop(columns=[col_name])
    dataframe.insert(loc=position, column=col_name, value=temp_col)
    return dataframe



def randomdategen(startdate,enddate):

    startyear=startdate.year
    startmonth=startdate.month
    startday=startdate.day

    endyear=enddate.year
    endmonth=enddate.month
    endday=enddate.day

    # startdate = datetime.datetime(2014,3,1,00,00,00)
    # enddate = datetime.datetime(2015,6,1,00,00,00)
    randomyear=random.randint(startyear,endyear)

    if(startmonth<endmonth):
        randommonth=random.randint(startmonth,endmonth)
    else:
        randommonth=random.randint(endmonth,startmonth)

    if(startday<endday):
        randomday=random.randint(startday,endday)
    else:
        randomday=random.randint(endday,startday)
    startrandomdate=datetime.datetime(randomyear,randommonth,randomday,00,00,00)
    

    endrandomdate=startrandomdate + datetime.timedelta(days=1)

    # if(randomday==31):
    #     randomday=0
    #     if(randommonth==12):
    #         randomyear=randomyear+1
    #     else:
    #         randommonth=randommonth+1

    # endrandomdate=datetime.datetime(randomyear,randommonth,(randomday+1),00,00,00)
    
    return startrandomdate,endrandomdate



def random1gen(tempdf):


    # selec='microwave1'
    # for x in range(len(database_list)):
    #     if selec in database_list[x].columns.to_list():
    #         tempdf=database_list[x].copy()

    startdate=tempdf.index.to_list()[0]
    enddate=tempdf.index.to_list()[-1]

    startdate,enddate=randomdategen(startdate,enddate)

    tempdf=tempdf[(tempdf.index >= str(startdate)) & (tempdf.index <= str(enddate))]




    return tempdf,startdate,enddate


def plotlydisplay(appdatabase):
    appdatabase.to_csv("temp.csv")

    fheaders=appdatabase.columns.to_list()
    fig = go.Figure()
    for i in range(len(fheaders)):
        fig.add_trace(go.Scatter(x=appdatabase.index.to_numpy(), y=appdatabase[fheaders[i]].to_numpy(),
                                    mode='lines',
                                    name=fheaders[i]))
    fig.show()



schoice=-1

if(schoice!=0):

    # print(" Main Options")
    # print("0. Quit")
    # print("1. Appliance Creation")
    # print("2. House Creation")
    # print("3. Visualize")

    # schoice=input("Enter choice (0-3) :")
    # schoice=int(schoice)

    schoice=os.getenv('SCHOICE')
    schoice=int(schoice)
    print(type(schoice))


    # if(schoice==0):
    #     break;    
        

   

    if(schoice==1):

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





        database_list = []

        csvfilenames, csvfilepaths = functioncsvfilenameandpath(folderpath)

        csvfilenames.sort()
        csvfilepaths.sort()

        printf(csvfilenames)

        for i in range(len(csvfilenames)):
            df = pd.read_csv(csvfilepaths[i], index_col=0, parse_dates=True)
            database_list.append(df)
            home_list.append(csvfilenames[i].replace('.csv', ''))




        for x in range(len(database_list)):
            df=database_list[x]
            database_list[x] = df.loc[:, (df != 0).any(axis=0)]
            # for i in range(len(database_list[homechoice].columns.to_list())):
            #     if(not((database_list[homechoice][i] == 0).all())):

        # Code to find out the common features between all houses
        intersectedheaders=database_list[2].columns.to_list()
        for i in range(len(database_list)):
            intersectedheaders=list(set.intersection(set(database_list[i].columns.to_list()),set(intersectedheaders)))
        intersectedheaders.sort()



        # Code to find out the common features between all houses
        unionheaders=database_list[2].columns.to_list()
        for i in range(len(database_list)):
            unionheaders=list(set.union(set(database_list[i].columns.to_list()),set(unionheaders)))
        unionheaders.sort()




        



        print(unionheaders)



        for i in range(len(database_list)):
            print(i,end=") ")
            print(csvfilenames[i],end=' : ')
            print(database_list[i].columns.to_list())




        import json
        f=open('metadata.json')
        jsonObject=json.load(f)
        print(jsonObject)
        print("------------------------------------------")

        simul=pd.DataFrame()




        fheaders=[]
        for app_no in range(len(jsonObject["appliances"])):
            fheaders.append(jsonObject["appliances"][app_no]["appliance_name"])
        print(fheaders)




        for x in fheaders:
            print(x,end=": ")
            for i in range(len(database_list)):
                if x in database_list[i].columns.to_list():
                    print('(',end='')
                    print(i,end='-')
                    
                    print(csvfilenames[i],end="")
                    print(')',end='-')
            print()



        directory="./appliances"

        if not os.path.exists(directory):
            os.makedirs(directory)

        for app_no in range(len(jsonObject["appliances"])):
            house_id=jsonObject["appliances"][app_no]["house_id"]
            for i in range(len(database_list)):
                if str(house_id) in csvfilenames[i]:            
                    house_id=i
                    break
            selec=jsonObject["appliances"][app_no]["appliance_name"]
            if(jsonObject["appliances"][app_no]["type"]=='continuous'):
                df=database_list[house_id][selec].to_frame()        
                df=df.sort_index()
                df=df.loc[:, (df != 0).any(axis=0)] # deletes empty columns
                # grouped=df.groupby(df.index.time).mean()        
                # df,startdate,enddate=random1gen(df)


                startdatestr=jsonObject["appliances"][app_no]["event_start_dt"]
                enddatestr=jsonObject["appliances"][app_no]["event_end_dt"]


                year, month, day, hour, minute, second = map(int, startdatestr.split('-'))
                startdate = datetime.datetime(year, month, day,hour,minute,second)


                year, month, day, hour, minute, second = map(int, enddatestr.split('-'))
                enddate = datetime.datetime(year, month, day,hour,minute,second)

                df=df[(df.index >= str(startdate)) & (df.index <= str(enddate))]



                if(not(df.empty)): # does not save empty dataframes
                    df.to_csv(directory+"/"+selec+".csv")
                
            if(jsonObject["appliances"][app_no]["type"]=='discrete'):
                df=database_list[house_id][selec].to_frame()        
                df=df.sort_index()
                df=df.loc[:, (df != 0).any(axis=0)] # deletes empty columns
                # grouped=df.groupby(df.index.time).mean()
                startdatestr=jsonObject["appliances"][app_no]["event_start_dt"]
                enddatestr=jsonObject["appliances"][app_no]["event_end_dt"]


                year, month, day, hour, minute, second = map(int, startdatestr.split('-'))
                startdate = datetime.datetime(year, month, day,hour,minute,second)


                year, month, day, hour, minute, second = map(int, enddatestr.split('-'))
                enddate = datetime.datetime(year, month, day,hour,minute,second)

                df=df[(df.index >= str(startdate)) & (df.index <= str(enddate))]


                if(not(df.empty)): # does not save empty dataframes
                    df.to_csv(directory+"/"+selec+".csv")



        homechoice=1

        df=database_list[homechoice].copy()
        df=df.sort_index()
        fheaders=df.columns.to_list()

        # grouped=df.groupby([df.index.hour, df.index.minute]).mean()

        grouped=df
        # grouped=df.groupby(df.index.time).median()


        # grouped=grouped.drop(columns=['leg1v','leg2v','dataid'])

        fheaders=grouped.columns.to_list()

        fheaders=['refrigerator1', 'heater1', 'clotheswasher1']


        fig = go.Figure()
        for i in range(len(fheaders)):
            fig.add_trace(go.Scatter(x=grouped.index.to_numpy(), y=grouped[fheaders[i]].to_numpy(),
                                        mode='lines',
                                        name=fheaders[i]))
        fig.show()










    elif(schoice==2):


        # This function is just so that I can use print statements and change default to 0, thus it sill not print
        def printf(str, print_bool=1):
            if (print_bool):
                print(str)


        # This is the file path for the normal dataset
        folderpath = './appliances'


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




        import json
        f=open('neighbourhood.json')
        jsonObject=json.load(f)


        import json
        x=open('metadata.json')
        metaObject=json.load(x)

        simul=pd.DataFrame()
        allcsv=pd.DataFrame()


        for neighbourhood_no in range(len(jsonObject["neighbourhood"])):

            ndirectory="./neighbourhoodResults/"+jsonObject["neighbourhood"][neighbourhood_no]["neighbourhood_name"]+str(datetime.datetime.timestamp(datetime.datetime.now()))

            if not os.path.exists(ndirectory):
                os.makedirs(ndirectory)
            

            for house_no in range(len(jsonObject["neighbourhood"][neighbourhood_no]["House"])):

                hdirectory=ndirectory+"/"+jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["House_Name"]

                if not os.path.exists(hdirectory):
                    os.makedirs(hdirectory)

    

                simul=pd.DataFrame()
                print("house No:")
                print(house_no)
                print("---------------------------------------")
                

                for app_no in range(len(jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"])):

                    # startbasetimex=jsonObject["neighbourhood"][0]["House"][0]["simulstartdate"]
                    # endbasetimex=jsonObject["neighbourhood"][0]["House"][0]["simulenddate"]

                    startbasetimex=jsonObject["neighbourhood"][neighbourhood_no]["simulstartdate"]
                    endbasetimex=jsonObject["neighbourhood"][neighbourhood_no]["simulenddate"]

                    year, month, day, hour, minute, second = map(int, startbasetimex.split('-'))
                    startbasedatetime = datetime.datetime(year, month, day,hour,minute,second)

                    year, month, day, hour, minute, second = map(int, endbasetimex.split('-'))
                    endbasedatetime = datetime.datetime(year, month, day,hour,minute,second)

                    

                    # print(jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"][app_no]["appliance_name"])
                    appObject=jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"][app_no]
              
                    mainfrequency=jsonObject["neighbourhood"][neighbourhood_no]["format"]["frequency"]

                    for meta_appno in range(len(metaObject["appliances"])):
                        if(metaObject["appliances"][meta_appno]["appliance_name"]==jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"][app_no]["appliance_name"]):
                            metaAppObject=metaObject["appliances"][meta_appno]



                    if(metaAppObject["type"]=="continuous"):
                        appdatabase=pd.read_csv(folderpath+"/"+appObject["data"], index_col=0, parse_dates=True)
                        appdatabase=appdatabase.sort_index()
                        tempdatabase=appdatabase.copy()
                        tempstart=datetime.datetime(startbasedatetime.year,startbasedatetime.month,startbasedatetime.day,00,00,00)
                        tempend=tempstart + datetime.timedelta(days=1)
                        newindex=pd.date_range(start=tempstart,end=tempend,freq=mainfrequency,tz='US/Central')
                        tempdatabase["datetimeindex"]=newindex
                        tempdatabase=tempdatabase.reset_index(drop=True)
                        tempdatabase=tempdatabase.set_index('datetimeindex')
                        tempdatabase=tempdatabase.sort_index()
                        # tempdatabase.plot()
                        # from matplotlib.pyplot import figure

                        # fig = plt.gcf()
                        # fig.set_size_inches(18.5, 10.5)
                        # plt.show()


                        plotlydisplay(tempdatabase)

                        simul=pd.concat([simul,tempdatabase],axis=1)



                    elif(metaAppObject["type"]=="discrete"):
                        appdatabase=pd.read_csv(folderpath+"/"+appObject["data"], index_col=0, parse_dates=True)
                        appdatabase=appdatabase.sort_index()
                        
                        # a_series = (appdatabase > appdatabase[appdatabase.columns.to_list()[0]].mode()[0]).any(axis=1)
                        # appdatabase = appdatabase.loc[a_series]
                        # appdatabase=random1gen(appdatabase)
                        

                        fullappdatabase=appdatabase.copy()

                        basedatetime=appdatabase.index.to_list()[0]

                        startdatetime=appdatabase.index.to_list()[0]
                        enddatetime=appdatabase.index.to_list()[-1]
                        

                        occ_list=jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"][app_no]["occurences"].split(',')
                        

                        occdatabaselist=[]

                        for x in occ_list:
                            tempdatabase=pd.DataFrame()
                            occhour,occminute,occsecond=x.split(':')
                            tempdatetime=enddatetime-startdatetime
                            occstartdatetime=datetime.datetime(startbasedatetime.year,startbasedatetime.month,startbasedatetime.day,int(occhour),int(occminute),int(occsecond))
                            occenddatetime=occstartdatetime+tempdatetime
                            newindex=pd.date_range(start=occstartdatetime,end=occenddatetime,freq=mainfrequency,tz='US/Central')
                            tempdatabase=appdatabase.copy()
                            tempdatabase["datetimeindex"]=newindex
                            tempdatabase=tempdatabase.reset_index(drop=True)
                            tempdatabase=tempdatabase.set_index('datetimeindex')
                            occdatabaselist.append(tempdatabase)


                        maindb=pd.concat(occdatabaselist)

                        col_name=fullappdatabase.columns.to_list()[0]



                        # startbasedatetime=startbasedatetime.replace(tzinfo=pytz.timezone('US/Central'))
                        # endbasetimex=endbasetimex.replace(tzinfo=pytz.timezone('US/Central'))

                        newindex=pd.date_range(start=startbasedatetime,end=endbasedatetime,freq=mainfrequency,tz='US/Central')
                        fullappdatabase=fullappdatabase.reset_index(drop=True)
                        fullappdatabase=pd.DataFrame()
                        fullappdatabase['datetimeindex']=newindex
                        
                        fullappdatabase=fullappdatabase.set_index('datetimeindex')


                        fullappdatabase[col_name]=metaAppObject["baseline"]
                        # fullappdatabase[col_name].values[:]=0

                        fullappdatabase=fullappdatabase.tz_convert('US/Central')

                        fullappdatabase=pd.concat([fullappdatabase,maindb])
                        # fullappdatabase=maindb

                        fullappdatabase = fullappdatabase[~fullappdatabase.index.duplicated(keep='last')]
                        


                        



                        fullappdatabase=maindb
                        fullappdatabase=fullappdatabase.sort_index()

                        # fullappdatabase.plot()
                        # from matplotlib.pyplot import figure

                        # fig = plt.gcf()
                        # fig.set_size_inches(18.5, 10.5)
                        # plt.show()

                        plotlydisplay(fullappdatabase)





                        
                                        

                        simul=pd.concat([simul,fullappdatabase],axis=1)
                        
                # 07:56:00

                
                # simul.plot()
                # from matplotlib.pyplot import figure

                # fig = plt.gcf()
                # fig.set_size_inches(18.5, 10.5)
                # plt.show()


                def convertunixto_datetime(x):
                    # x=datetime.datetime.strptime(x, '%y-%m-%d %H:%M:%S')
                    x=datetime.datetime.timestamp(x)
                    return x

                simul=simul.reset_index()

                simul[unixdatetimecolumnname]=simul[datetimecolumnname].apply(convertunixto_datetime)
                simul=simul.set_index(datetimecolumnname)


                simul['Total Usage']=0


                for column_name in simul.columns.to_list():
                    if(not(column_name in summation_exception_column_list)):
                        # Here we are adding all cloumns into Total Usage not in summation_exception_column_list
                        simul['Total Usage']+=simul[column_name]
                        print("Columns :"+str(column_name))

                simul=reorder_columns(dataframe=simul,col_name=unixdatetimecolumnname,position=1)


                plotlydisplay(simul)

                simul.to_csv(hdirectory+"/output.csv")



            

