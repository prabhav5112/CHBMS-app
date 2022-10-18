# Import required libraries
import matplotlib.ticker as plticker,seaborn as sns,pandas as pd,numpy as np,matplotlib.pyplot as plt,math,pyplot_themes as themes
from datetime import date

# Initialise seaborn
sns.set()
# Declaring variables
j,i = 0,0
def plot_graphs(dark = 0):
	# Iterate through keys
	for key in keys:
		if dark % 2 == 0:
			themes.theme_dark()
			plt.rcParams['savefig.facecolor']= 'k'
		else:
			themes.theme_minimal()
			sns.set()
			plt.rcParams['savefig.facecolor']= 'white'
		fig,ax = plt.subplots(1,2,constrained_layout = True,figsize = (8,5))
		# Get the rows for each Facility as a datframe
		df = grouped.get_group(key)
		data = (df[df["Date"] == date.today()])[['Occupied','Available']].iloc[0]
		try:
			percent = [str("%.2f"%((x/sum(data))*100)) + "%" for x in data]
		except:
			data = (df[df["Date"] == date(2020,11,18)])[['Occupied','Available']].iloc[0]
			percent = [str("%.2f"%((x/sum(data))*100)) + "%" for x in data]
		outside, _ = ax[1].pie(data, radius=1, labels = percent, pctdistance=1-0.35/2,colors = ["C1","C2"])
		ax[1].set_title("Status as of "+ date.today().strftime("%B %d, %Y"))
		ax[1].legend(['Occupied','Available'],title="Beds",loc="lower right",bbox_to_anchor=(1, -0.2))
		print(key)
		plt.setp(outside, width=0.35, edgecolor='white')
		# Store a list of date as xticks values
		mths = np.array([x.strftime("%d-%b") for x in df["Date"].values])
		if df.shape[0] <= 15:
			step = 1
		else:
			step = math.ceil(df.shape[0]/15)
		months = np.array([""]*step)
		months = np.append(months, mths)
		months = months[::step]
		df.reset_index(drop = True,inplace = True)
		df[['Allocated','Occupied','Available']].plot(kind = "line",ax = ax[0],marker = ".",xlabel = "Date",ylabel = "Total Beds",legend = True,markevery = step)
		plt.setp(ax[0], xticklabels=months)
		# Give required conditions for xticks
		ax[0].tick_params(axis='x', labelrotation=90)
		# This locator puts ticks at regular intervals
		loc = plticker.MultipleLocator(base=step) 
		fig.suptitle(key)
		ax[0].xaxis.set_major_locator(loc)
		if dark % 2 == 0:
			plt.savefig("Graphs/" + key+ "_dark.png")
		else:
			plt.savefig("Graphs/" + key+ ".png")

def plot_figures(engine):
	global grouped,keys
	# Read from MySQL table into a dataframe
	engine.execute("commit")
	df = pd.read_sql('select * from Govt_quota', engine)
	# Group the rows of the Dataframe by Facility
	grouped = df.groupby(df.Facility)
	# Store the list of distinct Facilities 
	keys = list(pd.read_sql('select distinct(Facility) from Govt_quota', engine)["Facility"])
	for i in range(2):
		plot_graphs(i)
