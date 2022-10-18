# Import required modules
import pandas as pd,numpy as np,lxml,time,progressbar
from sqlalchemy import create_engine
from datetime import date

def create_MySQL_engine(user,password):
	#Setup a connection between MySQL and python
	engine = create_engine('mysql+mysqlconnector://{}:{}@localhost/project'.format(user,password), echo=False)

#Website from which data is scraped
url = "https://bbmpproject.in/chbms-reports/"

#Declare table names 
TAB_NAMES = ["Govt_quota","Pvt_argmt","Govt_hospitals","Govt_med_colleges","Pvt_hospitals","Pvt_med_colleges","Govt_CCC"]
SUB_TABS = ["Alloc","Occ","Ava"]
 

def alter_table(tname):
    que = "delete from {} where Date = \"{}\"".format(tname,date.today())
    engine.execute(que)
def write_db(replace = False):
    with progressbar.ProgressBar(max_value=15,redirect_stdout=True) as bar:
        j,bar_val = 0,0
        for df in bed_stats:  
            print("-"*20)
            #Store table name
            tname = TAB_NAMES[j]
            #Check if it is a multi index dataframe
            if type(df.columns) == pd.MultiIndex:
                i = 0
                for k in range(2,16,5):
                    #pdb.set_trace()
                    tname = TAB_NAMES[j]+"_"+SUB_TABS[i]
                    #Create a dataframe with required columns  
                    new = df.iloc[:,0:2].join(df.iloc[:,k:k+5])
                    #Convert the columns into single index
                    new.columns = new.columns.droplevel()
                    #Add date column to the dataframe
                    new['Date'] = date.today()
                    new.dropna(inplace = True)
                    #Change dataframe columns to those as in the table
                    new.columns = pd.read_sql("select * from {}".format(tname),engine).columns
                    #If existing data should be replaced
                    if replace:
                        alter_table(tname)
                    #Write to the MySQL database
                    print("Writing " + tname + " to the database")
                    new.to_sql(name = tname , con = engine, if_exists='append', index = False)
                    bar.update(bar_val)
                    i += 1
                    bar_val += 1
            #Else
            else:
                tname = TAB_NAMES[j]
                #Add date column to the dataframe
                df['Date'] = date.today()
                #Drop all NaN values from the dataframe
                df.dropna(inplace = True)            
                #Change dataframe columns to those as in the table
                try:
                    df.columns = pd.read_sql("select * from {}".format(tname),engine).columns            
                except Exception as e:
                    print(e)
                    pass
                #If existing data should be replaced
                if replace:
                    alter_table(tname)
                #Write to the MySQL database
                print("Writing " + tname + " to the database")
                df.to_sql(name = TAB_NAMES[j], con = engine, if_exists='append', index = False)
                bar.update(bar_val)
                bar_val += 1
            j += 1
    print("Done!!!")

#Check if today's data is already present in the database
def write_tables():
	if len(db_df.loc[db_df["Date"] == date.today()]) == 0:
		print("Adding data to the database.....")
		write_db()
	else:
		print("Replacing existing data.....")
		write_db(replace = True)
	engine.execute("commit")

# Try except block to handle any exceptions	
try:
	bed_stats = pd.read_html(url)
	db_df = pd.read_sql("select * from Govt_quota",engine)
except Exception as e:
	print("Encountered an error: {}".format(e))

