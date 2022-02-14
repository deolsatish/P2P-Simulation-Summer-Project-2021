import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
from time import sleep
import json
import plotly.graph_objects as go


#summation_exception_column_list is required to tell the code which features to exempt from Total Usage summation
summation_exception_column_list=['use','grid','solar','solar2','Total Usage','leg1v','leg2v','dataid','localminute','datetimeindex','UnixTimeStamp']
# This is for for storing datetime index
datetimecolumnname='datetimeindex'
# This is name of Unix TimeStamp in simulation csv's
unixdatetimecolumnname='UnixTimeStamp'
# This is name of column which is total sum of all total appliances
aggcolumnname='Total Usage'


# This function is just so that I can use print statements and change default to 0, thus it sill not print
def printf(str, print_bool=1):
    if (print_bool):
        print(str)

# importing dotenv and initializing code
from dotenv import load_dotenv
load_dotenv()



def functioncsvfilenameandpath(path='./'):
    """ Returns file name and path of all csv files in a path

    Args:
        Path File (default): './'
    
    Returns:
        csvfilenames: list of all csv files on that path
        csvfilepaths: list of all file paths of all csvs found in the path

    """
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





def plotlydisplay(appdatabase,rootdirectory,show=0):
    """ Displays database using plotly graph on a browser and automatically savs it in a html file, This is mainly used for databases with single appliance or column

    Args:

      appdatabase: pandas dataframe which we need to visualize

      rootdirectory: it is the directory where we need to store the html graph

      show: A boolean which decides if graph should be displayed or just saved

    Returns:
      No Returns
    """

    fheaders=appdatabase.columns.to_list()
    fig = go.Figure()
    for i in range(len(fheaders)):
        fig.add_trace(go.Scatter(x=appdatabase.index.to_numpy(), y=appdatabase[fheaders[i]].to_numpy(),
                                    mode='lines',
                                    name=fheaders[i]))

    if(show):
        fig.show()
    fig.write_html(rootdirectory+"/"+appdatabase.columns.to_list()[0]+".html") # This save the html to Open the graph

def plotlydisplayall(appdatabase,rootdirectory,show=0):
    """ Displays database using plotly graph on a browser and automatically savs it in a html file, but meant for a database with multiple appliances and columns or exactly for house database

    Args:

      appdatabase: pandas dataframe which we need to visualize

      rootdirectory: it is the directory where we need to store the html graph

      show: A boolean which decides if graph should be displayed or just saved

    Returns:
      No Returns
    """

    fheaders=appdatabase.columns.to_list()
    fig = go.Figure()
    for i in range(len(fheaders)):
        fig.add_trace(go.Scatter(x=appdatabase.index.to_numpy(), y=appdatabase[fheaders[i]].to_numpy(),
                                    mode='lines',
                                    name=fheaders[i]))

    if(show):
        fig.show()
    fig.write_html(rootdirectory+"/"+"houseoutput"+".html")



def matplotlibsaveindividual(appdatabase,rootdirectory):
    """ Saves a matplotlib created graph as a jpeg file, meant for single appliance or column

    Args:

      appdatabase: pandas dataframe which we need to visualize

      rootdirectory: it is the directory where we need to store the html graph

    Returns:
      No Returns
    """
    appdatabase.plot()
    from matplotlib.pyplot import figure

    fig = plt.gcf()
    title="Graph"
    plt.title(title)
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(rootdirectory+"/"+appdatabase.columns.to_list()[0]+".jpeg", dpi=100,facecolor='white', transparent=False)
    

def matplotlibsaveall(appdatabase,rootdirectory):
    """ Saves a matplotlib created graph as a jpeg file, meant for multiple applaicnes or columns or exactly for house database

    Args:

      appdatabase: pandas dataframe which we need to visualize

      rootdirectory: it is the directory where we need to store the html graph

    Returns:
      No Returns
    """
    appdatabase=appdatabase.copy()
    appdatabase=appdatabase.drop(columns=[aggcolumnname])
    appdatabase=appdatabase.drop(columns=[unixdatetimecolumnname])
    appdatabase.plot()
    from matplotlib.pyplot import figure

    fig = plt.gcf()
    title="Graph"
    plt.title(title)
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(rootdirectory+"/"+"houseoutput"+".jpeg", dpi=100,facecolor='white', transparent=False)




schoice=-1

if(schoice!=0):

    # gets schoice from .env file
    schoice=int(os.getenv('SCHOICE'))   

    if(schoice==1):

        # This is the file path for the normal dataset
        folderpath = './PreppedData'

        # Database_list is the variable which contains the array of dataframes(database) of each house
        database_list = []
        # home_list will contains the name of each house, it will read all the folder names within Data folder
        home_list = []

        # This variable stores the features that are common for all houses so that we can compare them
        intersectedheaders = []

        # This is just to initalize the startdate and enddate vairbles with datetime datatype
        startdate = datetime.datetime.now
        enddate = datetime.datetime.now

        # returns all csv file names and paths from folderpath
        csvfilenames, csvfilepaths = functioncsvfilenameandpath(folderpath)

        # It sorts csvfilename and csvfilepath lists
        csvfilenames.sort()
        csvfilepaths.sort()

        # Stores the csv or database of all houses listed in PreppedData
        for i in range(len(csvfilenames)):
            df = pd.read_csv(csvfilepaths[i], index_col=0, parse_dates=True)
            database_list.append(df)
            home_list.append(csvfilenames[i].replace('.csv', ''))



        # Deletes all columns which have zero values
        for x in range(len(database_list)):
            df=database_list[x]
            database_list[x] = df.loc[:, (df != 0).any(axis=0)]


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


        # Just Displays all the columns or appliances in each database
        for i in range(len(database_list)):
            print(i,end=") ")
            print(csvfilenames[i],end=' : ')
            print(database_list[i].columns.to_list())



        # Stores metadata.json in jsonObject variable 
        import json
        f=open('metadata.json')
        jsonObject=json.load(f)
        simul=pd.DataFrame()



        # fheaders contains a list of names of all applaicnes in metadata.json
        fheaders=[]
        for app_no in range(len(jsonObject["appliances"])):
            fheaders.append(jsonObject["appliances"][app_no]["appliance_name"])



        # Displays all houses which contain the corresponding appliance
        for x in fheaders:
            print(x,end=": ")
            for i in range(len(database_list)):
                if x in database_list[i].columns.to_list():
                    print('(',end='')
                    print(i,end='-')
                    
                    print(csvfilenames[i],end="")
                    print(')',end='-')
            print()


        # The path directory where we store the appliances csvs
        directory="./appliances"

        # Creates directory if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        for app_no in range(len(jsonObject["appliances"])): # Iterates through all appliances in metadata.json
            
            # house id is the house name of the house we extract the data from
            house_id=jsonObject["appliances"][app_no]["house_id"]

            # We check if that house_id exits and store its corresponding index in database_list or csvfilename list
            for i in range(len(database_list)):
                if str(house_id) in csvfilenames[i]:            
                    house_id=i
                    break

            # selec contains the current appliance name
            selec=jsonObject["appliances"][app_no]["appliance_name"]

            # Checks the appliance type and accordingly extracts the data
            if(jsonObject["appliances"][app_no]["type"]=='continuous'):

                # extracts all data of that applaince from that house
                df=database_list[house_id][selec].to_frame()
                # Sorts the data according to index        
                df=df.sort_index()
                df=df.loc[:, (df != 0).any(axis=0)] # deletes empty columns


                startdatestr=jsonObject["appliances"][app_no]["event_start_dt"]
                enddatestr=jsonObject["appliances"][app_no]["event_end_dt"]


                # Converts the dataformat from string to datetime datatype
                year, month, day, hour, minute, second = map(int, startdatestr.split('-'))
                startdate = datetime.datetime(year, month, day,hour,minute,second)
                year, month, day, hour, minute, second = map(int, enddatestr.split('-'))
                enddate = datetime.datetime(year, month, day,hour,minute,second)


                # Sorts the database according to condition that index is >= the eventstartdatetime and index is <= the eventenddatetime
                df=df[(df.index >= str(startdate)) & (df.index <= str(enddate))]

                # if database is empty then it does not save the database
                if(not(df.empty)): # does not save empty dataframes
                    # Saves database in directory (variable)
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



       

    elif(schoice==2):


        # This function is just so that I can use print statements and change default to 0, thus it sill not print
        def printf(str, print_bool=1):
            if (print_bool):
                print(str)


        # This is the file path for the normal dataset
        folderpath = './appliances'


        # Database_list is the variable which contains the array of dataframes(database) of each house
        database_list = []
        # home_list will contains the name of each house, it will read all the folder names within Data folder
        home_list = []

        # This variable stores the features that are common for all houses so that we can compare them
        intersectedheaders = []

        # This is just to initalize the startdate and enddate vairbles with datetime datatype
        startdate = datetime.datetime.now
        enddate = datetime.datetime.now

        # returns all csv file names and paths from folderpath
        csvfilenames, csvfilepaths = functioncsvfilenameandpath(folderpath)

        # It sorts csvfilename and csvfilepath lists
        csvfilenames.sort()
        csvfilepaths.sort()

        # Stores the csv or database of all houses listed in PreppedData
        for i in range(len(csvfilenames)):
            df = pd.read_csv(csvfilepaths[i], index_col=0, parse_dates=True)
            database_list.append(df)
            home_list.append(csvfilenames[i].replace('.csv', ''))



        # Deletes all columns which have zero values
        for x in range(len(database_list)):
            df=database_list[x]
            database_list[x] = df.loc[:, (df != 0).any(axis=0)]



        # Stores neighbourhood.json in jsonObject variable 
        import json
        f=open('neighbourhood.json')
        jsonObject=json.load(f)

        # Stores metadata.json in metaObject variable
        import json
        x=open('metadata.json')
        metaObject=json.load(x)

        simul=pd.DataFrame()
        allcsv=pd.DataFrame()
        house_name_list=[]
        house_csv_list=[]

        # Iterating through all neighbourhoods
        for neighbourhood_no in range(len(jsonObject["neighbourhood"])):

            simul=pd.DataFrame()
            allcsv=pd.DataFrame()
            house_name_list=[] # house_name_list contains a list of all houses in neighbourhood
            house_csv_list=[]
            print("Neighbourhood Number :")
            print(neighbourhood_no)
            print("---------------------------------------")

            # ndirectory is the neighbourhood directory or folder for each house 
            ndirectory="./neighbourhoodResults/"+jsonObject["neighbourhood"][neighbourhood_no]["neighbourhood_name"]+str(datetime.datetime.timestamp(datetime.datetime.now()))

            # Creates the directory if it does not exist
            if not os.path.exists(ndirectory):
                os.makedirs(ndirectory)

            # iterates theough all houses in the neighbourhood
            for house_no in range(len(jsonObject["neighbourhood"][neighbourhood_no]["House"])):

                # hdirectory is the folder path for that house in that neighbourhood
                hdirectory=ndirectory+"/"+jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["House_Name"]

                
                house_name_list.append(jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["House_Name"])

                # Creates the directory if it does not exist
                if not os.path.exists(hdirectory):
                    os.makedirs(hdirectory)

    

                simul=pd.DataFrame()
                print("     house No:")
                print("     ",end="")
                print(house_no)
                print("     ---")
                

                # iterates through all appliances in that house
                for app_no in range(len(jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"])):


                    # SToring Simulation start and simulation end dates
                    startbasetimex=jsonObject["neighbourhood"][neighbourhood_no]["simulstartdate"]
                    endbasetimex=jsonObject["neighbourhood"][neighbourhood_no]["simulenddate"]

                    # Converting the simul start and end dates into dattime datatype
                    year, month, day, hour, minute, second = map(int, startbasetimex.split('-'))
                    startbasedatetime = datetime.datetime(year, month, day,hour,minute,second)
                    year, month, day, hour, minute, second = map(int, endbasetimex.split('-'))
                    endbasedatetime = datetime.datetime(year, month, day,hour,minute,second)

                    # Storing corresponding json appliance object
                    appObject=jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"][app_no]

                    # Storing the main frequency of database gven in neighbourhood format section
                    mainfrequency=jsonObject["neighbourhood"][neighbourhood_no]["format"]["frequency"]

                    # Seacrhing for corrsponsding appliance jsonObject data from metadata.json
                    for meta_appno in range(len(metaObject["appliances"])):
                        if(metaObject["appliances"][meta_appno]["appliance_name"]==jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"][app_no]["appliance_name"]):
                            metaAppObject=metaObject["appliances"][meta_appno]

                    # Depending on the type of appliance data we have two different blocks of code

                    if(metaAppObject["type"]=="continuous"):
                        # Extracting applaince data from appliance folder from metadata data parameter
                        appdatabase=pd.read_csv(folderpath+"/"+appObject["data"], index_col=0, parse_dates=True)
                        appdatabase=appdatabase.sort_index()
                        tempdatabase=appdatabase.copy()
                        # We get startbasedatetime from simulation start datetime
                        # At this point we are just simulating 24 hours of data
                        # tempstart just signifies the start of that day
                        tempstart=datetime.datetime(startbasedatetime.year,startbasedatetime.month,startbasedatetime.day,00,00,00)
                        tempend=tempstart + datetime.timedelta(days=1) # tempend is just adding 1 extra day to tempstart
                        """
                        The major problem will be here, for now i know the timezone of the datetime in the database
                        Thus, I can manually specify it, but it wil become a problem if the timezone if different
                        """
                        # Creates new index using tempstart and tempend, it is a pd.series datatype
                        newindex=pd.date_range(start=tempstart,end=tempend,freq=mainfrequency,tz='US/Central')
                        tempdatabase["datetimeindex"]=newindex
                        tempdatabase=tempdatabase.reset_index(drop=True)
                        tempdatabase=tempdatabase.set_index('datetimeindex')
                        tempdatabase=tempdatabase.sort_index()
                        # We use the new series as a new index, but we are not chaning the data or column values

                        plotlydisplay(tempdatabase,hdirectory)
                        matplotlibsaveindividual(tempdatabase,hdirectory)

                        simul=pd.concat([simul,tempdatabase],axis=1)



                    elif(metaAppObject["type"]=="discrete"):
                        # Extracting applaince data from appliance folder from metadata data parameter
                        appdatabase=pd.read_csv(folderpath+"/"+appObject["data"], index_col=0, parse_dates=True)
                        appdatabase=appdatabase.sort_index()
                        
                        

                        fullappdatabase=appdatabase.copy()

                        basedatetime=appdatabase.index.to_list()[0]

                        startdatetime=appdatabase.index.to_list()[0]
                        enddatetime=appdatabase.index.to_list()[-1]
                        
                        # occ_list is the list of occurences or times when the appliance is used
                        occ_list=jsonObject["neighbourhood"][neighbourhood_no]["House"][house_no]["appliances"][app_no]["occurences"].split(',')
                        

                        occdatabaselist=[]

                        for x in occ_list:

                            tempdatabase=pd.DataFrame() # Creating new Dataframe
                            occhour,occminute,occsecond=x.split(':') # This is the time when the applaince is used
                            tempdatetime=enddatetime-startdatetime
                            # We use the time to convert into datetime using the simulation start time for the occurences startdatetime and enddatetime
                            occstartdatetime=datetime.datetime(startbasedatetime.year,startbasedatetime.month,startbasedatetime.day,int(occhour),int(occminute),int(occsecond))
                            occenddatetime=occstartdatetime+tempdatetime
                            # We create a new pd.series to use as the new index 
                            newindex=pd.date_range(start=occstartdatetime,end=occenddatetime,freq=mainfrequency,tz='US/Central')
                            tempdatabase=appdatabase.copy()
                            tempdatabase["datetimeindex"]=newindex
                            tempdatabase=tempdatabase.reset_index(drop=True) # Reset index turns index into column and id drop=True it instead deletes the column entirely
                            tempdatabase=tempdatabase.set_index('datetimeindex') # Setting new datetimeindex
                            occdatabaselist.append(tempdatabase) # occdatabaselist contains list of all the data related to the occurences


                        maindb=pd.concat(occdatabaselist) # Combining all the Occurences data

                        col_name=fullappdatabase.columns.to_list()[0] # We can get the column name which stores the appliance data

                        # This index series range is the simulation start and end datetime
                        newindex=pd.date_range(start=startbasedatetime,end=endbasedatetime,freq=mainfrequency,tz='US/Central')
                        fullappdatabase=fullappdatabase.reset_index(drop=True)
                        fullappdatabase=pd.DataFrame()
                        fullappdatabase['datetimeindex']=newindex
                        
                        fullappdatabase=fullappdatabase.set_index('datetimeindex')


                        # As the appliance is only used depending on the occurences, We need to define the baseline consumption
                        # When the appliance is not used.
                        fullappdatabase[col_name]=metaAppObject["baseline"]

                        # This is mainly because the dataset we use has a different timezone
                        fullappdatabase=fullappdatabase.tz_convert('US/Central')

                        # The maindb contains data related to the the appliance is used and the fullappdatabase contains data when 
                        # appliance is not used
                        fullappdatabase=pd.concat([fullappdatabase,maindb])
                    
                        # Because there are duplicates indexes and the data when appliance is used is at the end of the list
                        # in the database as well it will be at the end thus we use parameter keep=last
                        fullappdatabase = fullappdatabase[~fullappdatabase.index.duplicated(keep='last')]
                        
                        fullappdatabase=maindb
                        fullappdatabase=fullappdatabase.sort_index()


                        plotlydisplay(fullappdatabase,hdirectory)
                        matplotlibsaveindividual(fullappdatabase,hdirectory)

                        simul=pd.concat([simul,fullappdatabase],axis=1)
                        
                        
  


                def convertdatetime_unix(x):
                    """ Converts datetime to unix timestamp data

                    Args:

                    x: datetime datatype

                    Returns:

                    x: UnixTimestamp

                    """
                    x=datetime.datetime.timestamp(x)
                    return x

                # reset index cremoves index into a column
                simul=simul.reset_index()
                
                # We use a function which applied to every value in the series
                # we are converting the entire datetime into unixtimestamp and storing it as a new column
                simul[unixdatetimecolumnname]=simul[datetimecolumnname].apply(convertdatetime_unix)
                simul=simul.set_index(datetimecolumnname) # we are setting the old column which is datetime index as the index again


                simul[aggcolumnname]=0 # Creating new aggreagte column with default value 0 
                simul=simul.fillna(0) # it fills all Nan values with 0

                # For loop iterates through all columns and add the value to new aggreagte column
                for column_name in simul.columns.to_list():
                    if(not(column_name in summation_exception_column_list)):
                        # Here we are adding all cloumns into Total Usage not in summation_exception_column_list
                        simul[aggcolumnname]+=simul[column_name]
                        # print("Columns :"+str(column_name))
                
                # We are reordering our unixtimestamp column to first position beside index
                simul=reorder_columns(dataframe=simul,col_name=unixdatetimecolumnname,position=0)

                # This displays the graphs and stores it as html
                plotlydisplayall(simul,hdirectory)


                simul.to_csv(hdirectory+"/houseoutput.csv") # We are storing the csv which data regarding to specific house
                matplotlibsaveall(simul,hdirectory)
                house_csv_list.append(simul.copy()) # This contains the list of all houses specific simulation data


            allcsv=pd.concat(house_csv_list,keys=house_name_list) # all csv contains all the from different houses where there is an extra index or column which indicates which house it belongs to
     
            allcsv=allcsv.reset_index(level=0)
            allcsv=allcsv.sort_index()
            allcsv=allcsv.rename(columns={"level_0":"House_Name"})
        
            allcsv.to_csv(ndirectory+"/allhousesoutput.csv")
        
            # Mastercsv only contains HouseA Consumtion and HouseB consumption and Total Consumption
            mastercsv=pd.DataFrame()
            mastercolumnadd=[]
            masteraggcolname="All houses Consumption"
            mastercsv[masteraggcolname]=0 # creating new ALl House COnsumption Column
            mastercsv=mastercsv.fillna(0)

            # We are creating new houseA Total Consumption , House B totalConsumption .... data from house_csv_list
            # 
            for ct in range(len(house_name_list)):
                houseaggcolname=house_name_list[ct]+" "+"Total Consumption"
                mastercolumnadd.append(houseaggcolname)
                mastercsv[houseaggcolname]=house_csv_list[ct][aggcolumnname]
                # mastercsv[masteraggcolname]=mastercsv[houseaggcolname]+mastercsv[masteraggcolname]
                # print("Columns :"+str(houseaggcolname))
            # We are saying the initali data it contains is from houseA of house1, thus we can start for loop from index 1 instead of 0
            mastercsv[masteraggcolname]=mastercsv[mastercolumnadd[0]]
            for ct in range(1,len(mastercolumnadd)):
                mastercsv[masteraggcolname]=mastercsv[masteraggcolname]+mastercsv[mastercolumnadd[ct]]
            # This reorder the Total neighbourhood aggregate column
            mastercsv=reorder_columns(dataframe=mastercsv,col_name=masteraggcolname,position=len(mastercolumnadd))
            
            mastercsv.to_csv(ndirectory+"/mastercsv.csv") # this saves the mastercsv file

            


            # The next part of the code focuses on copying neighbourhood.json metadata.json, the appliances folder and the Prepped Data
            # It also creates an argument file which shows the arguments we used in that session
            odirectory=ndirectory+"/Configuration"


            

            if not os.path.exists(odirectory):
                os.makedirs(odirectory)

            import json

            jsonString = json.dumps(jsonObject,indent=4)
            jsonFile = open(odirectory+"/"+"neighbourhood.json", "w")
            jsonFile.write(jsonString)
            jsonFile.close()

            jsonString = json.dumps(metaObject,indent=4)
            jsonFile = open(odirectory+"/"+"metadata.json", "w")
            jsonFile.write(jsonString)
            jsonFile.close()

            f=open(odirectory+"/"+"argument.txt","a")
            txt="Choice Chosen for main menu Option: " + str(schoice) +"\n"
            f.write(txt)
            f.close()

            import os
            import shutil
            src_dir = "./PreppedData"
            dst_dir = odirectory + "/PreppedData"

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            for root, dirs, files in os.walk(src_dir):
                for f in files:
                    if f.endswith('.csv'):
                        shutil.copy(os.path.join(root,f), dst_dir)



            import os
            import shutil
            src_dir = "./appliances"
            dst_dir = odirectory + "/appliances"

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            for root, dirs, files in os.walk(src_dir):
                for f in files:
                    if f.endswith('.csv'):
                        shutil.copy(os.path.join(root,f), dst_dir)







            

