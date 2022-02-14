import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import calendar
import os
import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from time import sleep




#This function is just so that I can use print statements and change default to 0, thus it sill not print
def printf(str,print_bool=1):
    if(print_bool):
        print(str)




# This is the file path for the normal dataset
folderpath='./PreppedData'
#This is the filepath for the dataset with Unix Timestamps as date and time
unixdatapath='./UnixData'

# This variable changes the code a bit to accomodate for the unix timestamps
# The code converts Unix Timestamps into datetime so that it we can sort the data by weeks and months as well
unixdatetimeformatbool=0

#Index+column is 0 because in the database the second column is dataid and the second column is date&time
index_column=0 

# Database_list is the variable which contains the array of dataframes(database) of each house 
database_list=[]
# home_list will contains the name of each house, it will read all the folder names within Data folder
home_list=[]

#This variable stores the features that are common for all houses so that we can compare them
intersectedheaders=[]

#This is just to initalize the startdate and enddate vairbles with datetime type
startdate=datetime.datetime.now
enddate=datetime.datetime.now


# In[ ]:


def functioncsvfilenameandpath(path='./'):
    # Path is the path where you want to search

    # this is the extension you want to detect
    extension = '.csv'

    csvfilepaths=[]
    csvfilenames=[]

    # print(path)

    for root, dirs_list, files_list in os.walk(path):
        for file_name in files_list:
            if os.path.splitext(file_name)[-1] == extension:
                file_name_path = os.path.join(root, file_name)
                if(file_name.find('')!=-1):
                    csvfilenames.append(file_name)
                    csvfilepaths.append(file_name_path)
                # print(file_name)
                # print(file_name_path)   # This is the full path of the filter file

    # printf(csvfilenames)
    # printf(csvfilepaths)   
    return csvfilenames,csvfilepaths


# In[ ]:


database_list=[]

csvfilenames,csvfilepaths=functioncsvfilenameandpath(folderpath)

csvfilenames.sort()
csvfilepaths.sort()

printf(csvfilenames)

for i in range(len(csvfilenames)):
    df=pd.read_csv(csvfilepaths[i], index_col=0, parse_dates=True)
    df=df.fillna(0)
    df=df.loc[:, (df != 0).any(axis=0)] # deletes empty columns
    database_list.append(df)
    home_list.append(csvfilenames[i].replace('.csv',''))


# #### This function is for Section 2. This combines all the data of the same features of all the houses into one dataframe. It returns an array of dataframes for different features

# In[ ]:



def initialize_housedatalist(fheaders=['grid','solar','solar2']):

    # This will delete all duplicated indexes
    for i in range(len(database_list)):
        database_list[i]=database_list[i].loc[~database_list[i].index.duplicated(), :]
        



    each_feature_database_list=[] # this contains a list of all specific columns from each database or each house

    for i in range(len(fheaders)):
        temp=[]
        for database in database_list:
            temp.append(database[fheaders[i]])
        each_feature_database_list.append(temp)

    dflist=[]

    for i in range(len(each_feature_database_list)):
        dftemp = pd.concat(each_feature_database_list[i], axis=1, keys=home_list)
        print("----")
        dftemp=dftemp.fillna(0)
        dflist.append(dftemp)
    return dflist


# ### Input Methods for choosing which house, which features and what should the timline of the graph should be

# In[ ]:


# this function propmts the user to choose a home
def choose_home(homechoice=2):
    print("Choose one of the homes selected to visualize its data")
    string1=""
    for i in range(len(home_list)):
        string1+=str(i)+". "+home_list[i]+"     \t"
    print("-------")
    homechoice=input(string1+"\n     |||||    Enter a single home (x):")
    if(len(homechoice)==0):
        homechoice=2
    homechoice=int(homechoice)

    print("Selected "+home_list[homechoice]+" as the home ")
    return homechoice


# This function prompts the use to choose features we want to visualize
def choose_features(homechoice):
    headers=database_list[homechoice].columns.to_list()
    print(" Choose which Features you want in your data:")

    for i in range(len(headers)):
        print(str(i)+"."+str(headers[i]))

    from time import sleep
    sleep(0.5)

    print("-------------------------------------------")
    featurechoiceinput = input("Enter all features you want as in 1,2,6,7 or x,x,x format or just press enter to select all features :")
    finput=featurechoiceinput.split(",")
    #print(finput)


    fheaders=[]

    if(not(finput[0]=='')):
        for i in finput:
            fheaders.append(headers[int(i)])
    
    if(not(fheaders)):
        #printf("Empty")
        fheaders=headers
    return fheaders


# This does the same thing It takes the features we want as argument
def choose_ifeatures(theaders):
    headers=theaders
    print(" Choose which Features you want in your data:")

    for i in range(1,len(headers)):
        printf(str(i)+"."+str(headers[i]))
    featurechoiceinput = input("Enter all features you want as in 1,2,6,7 or x,x,x format or just press enter to select all :")
    finput=featurechoiceinput.split(",")
    #print(finput)


    fheaders=[]

    if(not(finput[0]=='')):
        for i in finput:
            fheaders.append(headers[int(i)])
    
    if(not(fheaders)):
        #printf("Empty")
        fheaders=['use [kW]', 'gen [kW]','Excess Energy','Total Usage']
    return fheaders



# This method prompts the user to enter a start and end date
def choose_duration(startdate,enddate):
    try:
        date = input("Enter start date&time in YYYY-MM-DD-HH-MM-SS format")
        year, month, day, hour, minute, second = map(int, date.split('-'))
        startdate = datetime.datetime(year, month, day,hour,minute,second)
    except:
        print("Using default startdate");


    try:

        date = input("Enter end date&time in YYYY-MM-DD-HH-MM-SS format")
        year, month, day, hour, minute, second = map(int, date.split('-'))
        enddate = datetime.datetime(year, month, day,hour,minute,second)
    except:
        print("Using default enddate");
    return startdate,enddate





# ### Code to find out the common features between all houses

# In[ ]:


# Code to find out the common features between all houses
intersectedheaders=database_list[0].columns.to_list()
for i in range(len(database_list)):
    intersectedheaders=(set(intersectedheaders) & set(database_list[i].columns.to_list()))

# printf(intersectedheaders)


# ### Section 1: Visualizing individual houses 

# In[ ]:


mainchoice=1
while(mainchoice!=0):
    print("1. Adding new aggregated Columns")
    print("2. Visualizing individual houses")
    print("3. Visualizing apliances while comparing with different houses")

    mainchoice=int(input())

    if(mainchoice==1):

        quit=True
        homechoice=0
        while(homechoice!=-1):
            print("Choose one of the homes selected to visualize its data")
            print("if you want to exit loop enter -1")
            string1=""
            for i in range(len(home_list)):
                string1+=str(i)+". "+home_list[i]+"     \t"
            print("-------")
            homechoice=input(string1+"\n  if you want to exit loop enter -1   |||||    Enter a single home (x):")
            if(len(homechoice)==0):
                homechoice=2
            homechoice=int(homechoice)

            if(homechoice==-1):
                break

            print("Selected "+home_list[homechoice]+" as the home ")

            database=database_list[homechoice].copy()
            database.reset_index(inplace=True)


            printf(type(database.columns.to_list()),0)
            printf(database.columns.to_list(),0)

            headers=database.columns.to_list()



            print(" Choose which Features you want to add in your data:")

            for i in range(1,len(headers)):
                print(str(i)+". ",end='')
                print(str(headers[i]))
                print(end='')
            featurechoiceinput = input("Enter all features you want as in 1,2,6,7 or x,x,x format orall")
            finput=featurechoiceinput.split(",")
            print(finput)


            fheaders=[]

            if(not(finput[0]=='')):
                for i in finput:
                    fheaders.append(headers[int(i)])


            if(finput[0]==''):
                finput=0
            else:
                finput=1
            print(finput)


            if(finput==0):
                for i in headers:
                    if(i=='use [kW]' or i=='gen [kW]' or i=='Date & Time'):
                        ("")
                    else:
                        fheaders.append(i)
                        print(i)
                    

            faddheaders=fheaders

            print("-----------")
            print(fheaders)

            print("Choose new name of your summed column")
            columnname = input("Choose new name of your summed column")
            database_list[homechoice][columnname]=0

            for i in faddheaders:
                database_list[homechoice][columnname]+=database_list[homechoice][i]


        # 3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30-31-32

    elif(mainchoice==2):


        homechoice=0
        fheaders=['use [kW]', 'gen [kW]','Excess Energy','Total Usage']
        resampleoffset='D'




        # Taking inputs from user
        # Which house to view visualization
        # Which features to choose to view
        # Which offset to use for resampling

        homechoice=choose_home()


        tdatabase=database_list[homechoice].copy()

        # heaaders contain all the column names from that database


        # Just sorting the database according to the index
        tdatabase.sort_index()

        fheaders=choose_features(homechoice)



        os.system('clear')

        resampleoffset=input("Enter H(hourly) or W(weekly) or M(monthly) or Q(Quarterly) or 0(No Resampling) for resampling the database ")


        # Resampling the database
        if(len(resampleoffset)!=0 and resampleoffset!='0'):
            tdatabase=tdatabase.resample(resampleoffset).median()
            printf("Resampling Done",1)




        # Initializing startdate and enddate with the start from database and end of database
        startdate=tdatabase.index.to_list()[0]
        enddate=tdatabase.index.to_list()[-1]

        print("Start Date&Time of database :")
        print(startdate)
        print("End Date&Time of database :")
        print(enddate)


        # # Choosing which the time period to view the visualizations 
        # startdate,enddate=choose_duration(startdate,enddate)






        tdb=tdatabase[(tdatabase.index >= str(startdate)) & (tdatabase.index <= str(enddate))]

        tempdb=tdb[fheaders]

        tempdb=tempdb.sort_index()


        os.system('clear')


        choice=1


        while(choice!=0):

            timeperiod="Start date&time: "+str(startdate)+" and "+ " End date&time: "+str(enddate)
            timeword="Start-"+startdate.strftime('%A %d %B %Y')+" ____  End-"+enddate.strftime('%A %d %B %Y')



            optionlist=[
            "0. Quit",
            "1. Just data spread across a user input time period",
            "2. hourly median data across whole time period",
            "3. hourly median data for each month",
            "4. hourly median data for each year",
            "5. hourly median data for each month of each year",
            "6. hourly median data for each dayoftheweek across the whole duration",
            "7. hourly median data for each dayoftheweek across each month in duration ",
            "8. Weekly median data across whole use input time period"]



            from time import sleep
            sleep(0.5)



            for options in optionlist:
                print(options)
            

            from time import sleep
            sleep(0.5)



            



            directory="./Graphs/Option"
            for i in range(1,len(optionlist)):

                if not os.path.exists(directory+str(i)):
                    os.makedirs(directory+str(i))



            inputstr=""
            print("Working")
            choice=input(inputstr+"\n     Enter a single choice (x):")
            if(len(choice)==0):
                choice=0
            choice=int(choice)

            os.system('clear')


            try:
                print("Selcted Option")
                print(optionlist[choice])
            except:
                print("Incorrect Option")



            if(choice==1):
                title="Line plot of data spread across a user input time period ("+timeperiod+")"+" for house "+ home_list[homechoice]
                print(title)

                fig=go.Figure()
                for i in range(len(fheaders)):
                    
                    fig.add_trace(go.Scatter(x=tempdb.index.to_numpy(),y=tempdb[fheaders[i]].to_numpy(),
                                    mode='lines',
                                    name=fheaders[i]))
                fig.show()


                

            



            #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
            #This is link to pandas groupby documentation
            if(choice==2):


                print("This is choice 2")
                tempdatabase=tempdb.groupby(tempdb.index.hour).median()

                title=" 0-24 hours data calucalted by using median for each hour across user input time period ("+timeperiod+")"+" for house "+ home_list[homechoice]
                print(title)
                fig=go.Figure()
                for i in range(len(fheaders)):
                    
                    fig.add_trace(go.Scatter(x=tempdatabase.index.to_numpy(),y=tempdatabase[fheaders[i]].to_numpy(),
                                    mode='lines',
                                    name=fheaders[i]))
                fig.show()

                



            if(choice==3):
            
                monthlydatabase=tempdb.groupby(tempdb.index.month)

                for group_key, group_value in monthlydatabase:
                    group = monthlydatabase.get_group(group_key)
                    #print(group.head(4))
                    print("--------------------------------")
                    group=group.groupby(group.index.hour).median()


                    title="0-24 hour median data for month: "+str(calendar.month_name[group_key])+" for house "+ home_list[homechoice]+"("+timeperiod+")"
                    print(title)


                    fig=go.Figure()
                    for i in range(len(fheaders)):
                        
                        fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[fheaders[i]].to_numpy(),
                                        mode='lines',
                                        name=fheaders[i]))
                    fig.show()
                    




            if(choice==4):

                monthlydatabase=tempdb.groupby(tempdb.index.year)

                for group_key, group_value in monthlydatabase:
                    group = monthlydatabase.get_group(group_key)

                    print("--------------------------------")
                    group=group.groupby(group.index.hour).median()

                    title="0-24 hour median0-24 hour median data for year: "+str(group_key)+" for house "+ home_list[homechoice]+"("+timeperiod+")"
                    print(title)



                    fig=go.Figure()
                    for i in range(len(fheaders)):
                        
                        fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[fheaders[i]].to_numpy(),
                                        mode='lines',
                                        name=fheaders[i]))
                    fig.show()
                    

            
                        

            if(choice==5):


                yearlydatabase=tempdb.groupby(tempdb.index.year)

                for yearlygroup_key, yearlygroup_value in yearlydatabase:
                    yearlygroup = yearlydatabase.get_group(yearlygroup_key)
                    monthlydatabase=yearlygroup.groupby(yearlygroup.index.month)

                    for group_key,group_value in monthlydatabase:
                        group = monthlydatabase.get_group(group_key)
                        print("--------------------------------")
                        group=group.groupby(group.index.hour).median()

                        title=str(calendar.month_name[group_key])+" "+str(yearlygroup_key)+" Month's hourly data" +" "+home_list[homechoice] +"("+timeperiod+")"
                        print(title)


                        fig=go.Figure()
                        for i in range(len(fheaders)):
                            
                            fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[fheaders[i]].to_numpy(),
                                            mode='lines',
                                            name=fheaders[i]))
                        fig.show()
                        
        


            if(choice==6):    

                monthlydatabase=tempdb.groupby(tempdb.index.dayofweek)

                for group_key, group_value in monthlydatabase:
                    group = monthlydatabase.get_group(group_key)

                    print("--------------------------------")
                    group=group.groupby(group.index.hour).median()


                    title=str(calendar.day_name[group_key])+"'s 0-24 hour median data " +" "+home_list[homechoice]+"("+timeperiod+")"
                    print(title)



                    fig=go.Figure()
                    for i in range(len(fheaders)):
                        
                        fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[fheaders[i]].to_numpy(),
                                        mode='lines',
                                        name=fheaders[i]))
                    fig.show()
                    


            if(choice==7):    

                monthlydatabase=tempdb.groupby(tempdb.index.month)

                for monthlygroup_key, monthlygroup_value in monthlydatabase:
                    yearlygroup = monthlydatabase.get_group(monthlygroup_key)
                    dayofweekdatabase=yearlygroup.groupby(yearlygroup.index.dayofweek)

                    for group_key,group_value in dayofweekdatabase:

                        group = dayofweekdatabase.get_group(group_key)
                        print("--------------------------------")
                        group=group.groupby(group.index.hour).median()

                        title=str(calendar.day_name[group_key])+" "+str(calendar.month_name[monthlygroup_key])+" Month's 0-24 hour median data" +" "+home_list[homechoice]+"("+timeperiod+")"
                        print(title)


                        fig=go.Figure()
                        for i in range(len(fheaders)):
                            
                            fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[fheaders[i]].to_numpy(),
                                            mode='lines',
                                            name=fheaders[i]))
                        fig.show()
                        


            if(choice==8):

                temp=tempdb.resample('D').median()
            
                title="Line plot of resampled weekly data spread across a user input time period ("+timeperiod+")"+" for house "+ home_list[homechoice]
                print(title)

                fig=go.Figure()
                for i in range(len(fheaders)):
                    
                    fig.add_trace(go.Scatter(x=temp.index.to_numpy(),y=temp[fheaders[i]].to_numpy(),
                                    mode='lines',
                                    name=fheaders[i]))
                fig.show() 



        #1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18
        # 1
        # 2014-11-01-00-00-00

        #1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18
        # 1
        # 2014-11-01-00-00-00

        # 2019-06-10-00-00-00

        # 30,66,67,78

    elif(mainchoice==3):
        
        fheaders=['grid']
        resampleoffset='0'

        # Which features to choose to view
        # fheaders=choose_ifeatures(intersectedheaders)

        featurevdatabase=initialize_housedatalist(fheaders)


        # Just sorting the database according to the index
        for i in range(len(featurevdatabase)):
            featurevdatabase[i].sort_index()






        # Which offset to use for resampling
        resampleoffset=str(input("Enter H(hourly) or W(weekly) or M(monthly) or Q(Quarterly) or 0(No Resampling) for resampling the database "))


        # Initializing startdate and enddate with the start from database and end of database
        startdate=featurevdatabase[0].index.to_list()[0]
        enddate=featurevdatabase[0].index.to_list()[-1]


        # startdate = datetime.datetime(2014,3,1,00,00,00)
        # enddate = datetime.datetime(2015,6,1,00,00,00)


        # Choosing which the time period to view the visualizations 


        print("Start Date&Time of database :")
        print(startdate)
        print("End Date&Time of database :")
        print(enddate)


        startdate,enddate=choose_duration(startdate,enddate)



        # # Resampling the database
        if(len(resampleoffset)!=0 and resampleoffset!='0'):
            for i in range(len(featurevdatabase)):
                featurevdatabase[i]=featurevdatabase[i].resample(resampleoffset).median()
            print("Resampling Done")


        for i in range(len(featurevdatabase)):
            featurevdatabase[i]=featurevdatabase[i][(featurevdatabase[i].index >= str(startdate)) & (featurevdatabase[i].index <= str(enddate))]
            # print(featurevdatabase[i].head(3))




        choice=1


        while(choice!=0):



            timeperiod="Start date&time: "+str(startdate)+" and "+ " End date&time: "+str(enddate)
            timeword="Start-"+startdate.strftime('%A %d %B %Y')+" ____  End-"+enddate.strftime('%A %d %B %Y')


            optionlist=[
            "0. Quit",
            "1. Just data spread across a user input time period",
            "2. hourly median data across whole time period",
            "3. hourly median data for each month",
            "4. hourly median data for each year",
            "5. hourly median data for each month of each year",
            "6. hourly median data for each dayoftheweek across the whole duration",
            "7. hourly median data for each dayoftheweek across each month in duration "]


            from time import sleep
            sleep(0.5)



            for options in optionlist:
                print(options)
            

            from time import sleep
            sleep(0.5)


            directory="./HomeGraphs/Option"
            for i in range(1,len(optionlist)):

                if not os.path.exists(directory+str(i)):
                    os.makedirs(directory+str(i))



            inputstr=""
            choice=input(inputstr+"\n     Enter a single choice (x):")
            if(len(choice)==0):
                choice=0
            choice=int(choice)

            os.system('clear')


            try:
                print("Selcted Choice")
                print(optionlist[choice])
            except:
                print("Incorrect Choice")




            if(choice==1):


                for x in range(len(featurevdatabase)):
                    tempdb=featurevdatabase[x]
                    title=fheaders[x]+" data spread across a user input time period "
                    print(title)
                    fig=go.Figure()
                    for i in range(len(home_list)):
                        
                        fig.add_trace(go.Scatter(x=tempdb.index.to_numpy(),y=tempdb[home_list[i]].to_numpy(),
                                        mode='lines',
                                        name=home_list[i]))
                    fig.show()
                    


            if(choice==2):

                for x in range(len(featurevdatabase)):
                    tempdb=featurevdatabase[x]  

                    database=tempdb.groupby(tempdb.index.hour).median()

                    title="Resampled "+fheaders[x]+" hourly data spread across a user input time period "

                    print(title)
                    fig=go.Figure()
                    for i in range(len(home_list)):
                        
                        fig.add_trace(go.Scatter(x=database.index.to_numpy(),y=database[home_list[i]].to_numpy(),
                                        mode='lines',
                                        name=home_list[i]))
                    fig.show()
            


            if(choice==3):

                for x in range(len(featurevdatabase)):
                    tempdb=featurevdatabase[x]  
                
                    monthlydatabase=tempdb.groupby(tempdb.index.month)

                    for group_key, group_value in monthlydatabase:
                        group = monthlydatabase.get_group(group_key)
                        #print(group.head(4))
                        print("--------------------------------")
                        group=group.groupby(group.index.hour).median()
                        title=str(calendar.month_name[group_key])+" Month's hourly median "+fheaders[x]+" data"
                        print(title)
                        fig=go.Figure()
                        for i in range(len(home_list)):
                            
                            fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[home_list[i]].to_numpy(),
                                            mode='lines',
                                            name=home_list[i]))
                        fig.show()
                        


            if(choice==4):
                for x in range(len(featurevdatabase)):
                    tempdb=featurevdatabase[x]  

                    monthlydatabase=tempdb.groupby(tempdb.index.year)

                    for group_key, group_value in monthlydatabase:
                        group = monthlydatabase.get_group(group_key)

                        print("--------------------------------")
                        group=group.groupby(group.index.hour).median()


                        title=str(group_key)+" Month's hourly data "+fheaders[x] +" "
                        print(title)
                        fig=go.Figure()
                        for i in range(len(home_list)):
                            
                            fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[home_list[i]].to_numpy(),
                                            mode='lines',
                                            name=home_list[i]))
                        fig.show()
                        
                        

            if(choice==5):

                for x in range(len(featurevdatabase)):
                    tempdb=featurevdatabase[x]  


                    yearlydatabase=tempdb.groupby(tempdb.index.year)

                    for yearlygroup_key, yearlygroup_value in yearlydatabase:
                        yearlygroup = yearlydatabase.get_group(yearlygroup_key)
                        monthlydatabase=yearlygroup.groupby(yearlygroup.index.month)

                        for group_key,group_value in monthlydatabase:
                            group = monthlydatabase.get_group(group_key)
                            print("--------------------------------")
                            group=group.groupby(group.index.hour).median()


                            title=str(calendar.month_name[group_key])+str(yearlygroup_key)+" Month's hourly data "+fheaders[x]+""
                            print(title)
                            fig=go.Figure()
                            for i in range(len(home_list)):
                                
                                fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[home_list[i]].to_numpy(),
                                                mode='lines',
                                                name=home_list[i]))
                            fig.show()

            if(choice==6):

                for x in range(len(featurevdatabase)):
                    tempdb=featurevdatabase[x]      

                    monthlydatabase=tempdb.groupby(tempdb.index.dayofweek)

                    for group_key, group_value in monthlydatabase:
                        group = monthlydatabase.get_group(group_key)

                        print("--------------------------------")
                        group=group.groupby(group.index.hour).median()
                        title=str(calendar.day_name[group_key])+" Month's hourly data "+fheaders[x]+" for that duration" +" "
                        print(title)
                        fig=go.Figure()
                        for i in range(len(home_list)):
                            
                            fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[home_list[i]].to_numpy(),
                                            mode='lines',
                                            name=home_list[i]))
                        fig.show()

            if(choice==7):
                for x in range(len(featurevdatabase)):
                    tempdb=featurevdatabase[x]      

                    monthlydatabase=tempdb.groupby(tempdb.index.month)

                    for monthlygroup_key, monthlygroup_value in monthlydatabase:
                        yearlygroup = monthlydatabase.get_group(monthlygroup_key)
                        dayofweekdatabase=yearlygroup.groupby(yearlygroup.index.dayofweek)

                        for group_key,group_value in dayofweekdatabase:

                            group = dayofweekdatabase.get_group(group_key)
                            print("--------------------------------")
                            group=group.groupby(group.index.hour).median()

                            title=str(calendar.day_name[group_key])+" "+str(calendar.month_name[monthlygroup_key])+" Month's hourly data "+fheaders[x]+""

                            print(title)
                            fig=go.Figure()
                            for i in range(len(home_list)):
                                
                                fig.add_trace(go.Scatter(x=group.index.to_numpy(),y=group[home_list[i]].to_numpy(),
                                                mode='lines',
                                                name=home_list[i]))
                            fig.show()

        #1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18
        # 1
        # 2014-03-01-00-00-00


        


        
        

