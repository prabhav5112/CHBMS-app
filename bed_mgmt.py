# Import required modules,as many in one line
import matplotlib.pyplot as plt,tkinter as tk,mysql.connector as sqltor,pandas as pd,numpy as np,math,pyplot_themes as themes
# Import tkinter modules
from tkinter import font,ttk,messagebox
# Import PIL modules
from PIL import ImageTk,Image
# Import datetime modules
from datetime import date,timedelta,datetime
# Import getpass module from getpass
from getpass import getpass
# Import create engine from sqlalchemy
from sqlalchemy import create_engine
# Initialise n, empty dictionary, empty list
d,n,lst,disp_graph,theme = {},0,[],1,"dark"
if theme == "dark":
	fg_color,bg_color = "white","gray15"
elif theme == 'light':
	fg_color,bg_color = "black","white"
bg_themes = {"dark":{"tv_even": "seashell4","tv_odd" : "cadet blue","fg": "black","stv_even":"thistle4","stv_odd":"slate gray"},"light":{"tv_even": "light blue","tv_odd" : "LightSeaGreen","fg": "black","stv_even":"powder blue","stv_odd":"SteelBlue2"}}
# Constants used in the program
TABNAMES = ["Govt_hospitals","Govt_med_colleges","Pvt_hospitals","Pvt_med_colleges","Govt_CCC"]
WIDTH,HEIGHT = 900,480
WIDTH_IMG = 600

# Accept username
user = input("Enter MySQL username: ")
# Accept password for sql user
password = getpass()
# Connect to the MySQL database using mysql.connector
cnx=sqltor.connect(host="localhost",user=user,password=password,database="project")
# Declare cursor object
cursor=cnx.cursor()
# While the resultset is empty
while lst == []:
	# Select all fields from Govt_quota where Date = today's date
	cursor.execute("select * from Govt_quota where Date = '{}'".format(date.today()+ timedelta(days = n)))
	# Fetch all records
	lst = cursor.fetchall()
	# Create label with the date of the records fetched
	txtlabel = " As of " + (date.today()+ timedelta(days = n)).strftime("%d-%b-%Y") + " (for those updated) *"
	# If no records were fetched
	if lst == []:
		# Decrement n by 1
		n -= 1
# Retrieve schema of Govt_quota table from MySQL database
cursor.execute("desc Govt_quota")
# Select column names from the resultset
columns = [x[0] for x in cursor.fetchall()]
# Remove date column
columns = columns[:-1]
# Establish conection with MySQL database using create_engine
engine = create_engine('mysql+mysqlconnector://{}:{}@localhost/project'.format(user,password), echo=False)
# Lambda function which gives the name of Facility of selected item in treeview
selectedItem = lambda tv: (tv.item(tv.focus())['values'][1])
# Lambda function which creates a Tkinter compatible image when a path is passed to it as an argument
tkImage = lambda path :  ImageTk.PhotoImage(Image.open(path))
# plot_bed_stats function which plots the graphs of individual hospitals
def plot_bed_stats(df,parent):
	# Import required modules
	import matplotlib.ticker as plticker, seaborn as sns
	# Initialise seaborn
	sns.set()
	# Change cursor to loading cursor
	window.config(cursor = "watch")
	# If dark theme is chosen
	if theme == 'dark':
			themes.theme_dark()
			plt.rcParams['savefig.facecolor']= 'k'
	else:
		themes.theme_minimal()
		sns.set()
		plt.rcParams['savefig.facecolor']= 'white'
	fig,ax = plt.subplots(1,2,constrained_layout = True,figsize = (8,5))
	# Try block
	try:
		# Check if today's data is present in the dataframe
		if parent not in ('Private Medical Colleges'):
			dt = date.today()
		else:
			dt = date(2020, 11, 18)
		data = np.array((df[df["Date"] == dt])[['Occupied','Available']].iloc[0])
	# Catch any errors
	except:
		# Change cursor to pointer
		window.config(cursor = "")
		# Show a warning 
		messagebox.showwarning(title=" Error", message="Unable to find today's data")
		# Return 
		return 
	# Percentage of available,occupied beds
	percent = [str("%.2f"%((x/sum(data))*100)) + "%" for x in data]
	# Plot the pie graph
	outside, _ = ax[1].pie(data, radius=1 ,labels = percent,colors = ["C1","C2"])
	# Declare legend for pieplot
	ax[1].legend(['Occupied','Available'],title="Beds",loc="lower right",bbox_to_anchor=(1, -0.2))
	# Set title for the pieplot
	ax[1].set_title("Status as of "+ dt.strftime("%B %d, %Y"))
	# Make it a donut plot
	plt.setp(outside, width=0.35, edgecolor='white')
	# Initialise mths array with dates
	mths = np.array([x.strftime("%d-%b") for x in df["Date"].values])
	# Check if the dataframe has 15 or lesser rows
	if df.shape[0] <= 15:
		# Initialise step to 1
		step = 1
	# If it has more than 15 rows
	else:
		# Initialise step based on number of rows in the dataframe
		step = math.ceil(df.shape[0]/15)
	# Add two empty values for data representation
	months = np.array([""]*step)
	months = np.append(months, mths)
	# Extract only 
	months = months[::step]
	# Set xticklabels as months
	plt.setp(ax[0], xticklabels=months)
	# Place ticks every step units
	loc = plticker.MultipleLocator(step) 
	# Set loc as the major locator for x axis
	ax[0].xaxis.set_major_locator(loc)
	# Plot the line graph
	axl = df[['Allocated','Occupied','Available']].plot(kind = "line",ax = ax[0],marker = ".",xlabel = "Date",ylabel = "Total Beds",legend = True,markevery = step)
	# Declare legend for line graph
	axl.legend(loc = "best")
	# Rotate x axis ticks by 90 deg
	ax[0].tick_params(axis='x', labelrotation=90)
	# Set a title for the figure
	fig.suptitle(df["DCHC"][0])
	# Save the fiigure
	plt.savefig("Graphs/"+df["DCHC"][0]+".png")
	plt.close(fig)
	# Initialise path to the location where the graph is saved
	path = "Graphs/{}".format(df["DCHC"][0]+".png")
	# Return path variable
	del _,ax,axl,data,df,fig,loc,months,mths,outside,percent,step
	return path

def select_subtree_Item(a):
	# Check that a subtree row was clikced
	if (subtree.item(subtree.focus())['values']) != '':
		# Initialise curItem to the row that was clicked
		curItem = selectedItem(subtree)
	# If a tree row was clicked
	else:
		# Break out of the function
		return
	# Check which row was selected in the tree
	parent = selectedItem(tree)
	# If CCC row was selected
	if parent == "Government Covid Care Centers [CCC]":
		# Initialise query for Govt_CCC table
		query = "select `Government CCC`,`Total Allocated Beds for C+ Patients` as Allocated, `Occupied Beds for C+ Patients` as Occupied,`Net Available Beds for C+ Patients` as Avaialble,Date from Govt_CCC where `Government CCC` = '{}'".format(curItem)
	# If any other row was selected
	else:
		# Initialise query for all other tables
		if parent in ('Private Medical Colleges'):
			query = "select {0}_Alloc.DCHC,{0}_Alloc.Total,{0}_Occ.Total,{0}_Ava.Total, {0}_Ava.Date from {0}_Alloc inner join {0}_Ava on {0}_Alloc.Date = {0}_Ava.Date inner join {0}_Occ on {0}_Occ.Date = {0}_Alloc.Date where {0}_Alloc.DCHC = '{1}' and {0}_Ava.DCHC = '{1}' and {0}_Occ.DCHC = '{1}' and {0}_Occ.Date <= '2020-11-18'".format(d[parent],curItem)
		else:
			query = "select {0}_Alloc.DCHC,{0}_Alloc.Total,{0}_Occ.Total,{0}_Ava.Total, {0}_Ava.Date from {0}_Alloc inner join {0}_Ava on {0}_Alloc.Date = {0}_Ava.Date inner join {0}_Occ on {0}_Occ.Date = {0}_Alloc.Date  where {0}_Alloc.DCHC = '{1}' and {0}_Ava.DCHC = '{1}' and {0}_Occ.DCHC = '{1}'".format(d[parent],curItem)
	# Initialise cols as the columns of dataframe
	cols = ["DCHC","Allocated","Occupied","Available","Date"]
	# Execute the MySQL query
	cursor.execute(query)
	# Store the resultset as a dataframe
	df = pd.DataFrame(cursor.fetchall())
	# Change the columns of dataframe to cols
	df.columns = cols
	# If graphs have to be displayed
	if disp_graph == 1:
		# 
		try:
			# Save Tkinter compatible image
			img = tkImage(plot_bed_stats(df,parent))
			# Update image on canvas
			canvas.itemconfig(can_img,image = img)
			
		except:
			# Do nothing
			pass
	# Delete the dataframe
	del df
	# Change cursor to pointer
	window.config(cursor = "")
	del a,cols,curItem,parent,query
	# Execution stops here
	window.mainloop()

def write_child_node(tname):
	# Declare lst as global variables so that we can make changes to it
	global lst,subtree
	# If subtree is populated
	if len(subtree.get_children()) > 0:
		# Delete all rows from subtree
		subtree.delete(*subtree.get_children())
	# Commit any changes made
	cursor.execute("commit")
	# If CCC row is selected
	if tname == "Govt_CCC":
		# Initialse que for Govt_CCC table
		que = "select * from Govt_CCC where Date = '{}'".format(date.today()+ timedelta(days = n))
	# If any other row is selected
	else:
		# Initialse que for other tables
		if tname in ('Pvt_med_colleges'):
			que = "select {0}_Alloc.DCHC,{0}_Alloc.Total,{0}_Occ.Total,{0}_Ava.Total, {0}_Ava.Date from {0}_Alloc inner join {0}_Ava on {0}_Alloc.DCHC = {0}_Ava.DCHC inner join {0}_Occ on {0}_Occ.DCHC = {0}_Alloc.DCHC  where {0}_Alloc.Date = '{1}' and {0}_Ava.Date = '{1}' and {0}_Occ.Date = '{1}'".format(tname,date(2020,11,18))
		else:
			que = "select {0}_Alloc.DCHC,{0}_Alloc.Total,{0}_Occ.Total,{0}_Ava.Total, {0}_Ava.Date from {0}_Alloc inner join {0}_Ava on {0}_Alloc.DCHC = {0}_Ava.DCHC inner join {0}_Occ on {0}_Occ.DCHC = {0}_Alloc.DCHC  where {0}_Alloc.Date = '{1}' and {0}_Ava.Date = '{1}' and {0}_Occ.Date = '{1}'".format(tname,date.today()+ timedelta(days = n))
	# Execute the query
	cursor.execute(que)
	# Initiaise i to 0 which will be used as a step
	i = 0
	# Fetch all records
	lst = cursor.fetchall()
	# Write headings of subtree
	write_tree(subtree,True)
	# Iterate through the elements of lst
	for line in lst:
		# Remove the laste element of line
		line = list(line)[:-1]
		# If CCC row was not selected
		if tname != "Govt_CCC":
			# Insert i+1 at index 0
			line.insert(0,i+1)
		# If i is even
		if i% 2 == 0:
			# Add line to subtree with odd tag
			subtree.insert("","end",values = line,tag = "child_odd")
		# If i is odd
		else:
			# Add line to subtree with even tag
			subtree.insert("","end", values = line,tag = "child_even")
		# Increment i by 1
		i += 1
	# Configure the tags of subtree
	subtree.tag_configure('child_odd', background = bg_themes[theme]["stv_odd"]) 
	subtree.tag_configure('child_even',background = bg_themes[theme]["stv_even"])
	# Pack the label 
	label.pack(side = 'top',fill = 'x',anchor = tk.N)
	# Pack the scrollbar
	verscrlbar.pack(side = 'right',fill = 'both') 
	# Bind select_subtree_Item with subtree so that it calls the function when a row is selected
	subtree.bind("<<TreeviewSelect>>", select_subtree_Item)
	# Pack the subtree
	subtree.pack(side ='top',fill = 'both',expand = True,anchor = tk.N)
	# del i,line,que,tname

def update_row(tv,general = True):
	if general == True:
		cursor.execute("select * from Govt_quota where Date = '{}'".format(date.today()+ timedelta(days = n)))
		lst = cursor.fetchall()
	else:
		print(general)
		que = "select {0}_Alloc.DCHC,{0}_Alloc.Total,{0}_Occ.Total,{0}_Ava.Total, {0}_Ava.Date from {0}_Alloc inner join {0}_Ava on {0}_Alloc.DCHC = {0}_Ava.DCHC inner join {0}_Occ on {0}_Occ.DCHC = {0}_Alloc.DCHC  where {0}_Alloc.Date = '{1}' and {0}_Ava.Date = '{1}' and {0}_Occ.Date = '{1}'and {0}_Alloc.DCHC = '{2}' and {0}_Ava.DCHC = '{2}' and {0}_Occ.DCHC = '{2}'".format(general[0],date.today()+ timedelta(days = n),general[1])
		# Execute the query
		cursor.execute(que)
		# Fetch all records
		lst = list(cursor.fetchall()[0][:-1])
	sel,selected = tv.focus(),True
	if general == True:
		tv.item(sel,values = lst[int(sel[3])-1])
	else:
		lst.insert(0,int(sel[3]))
		tv.item(sel,values = lst)
def admin_input(event,window,frm,parent):
	# Remove the frame frm
	frm.pack_forget()
	# Initialise the geometry of the window
	window.geometry("250x170")
	# COnfigure background colour of the window
	window.configure(bg = "grey")
	# Set a title for the window
	window.title("Hospital Details")
	var = d[selectedItem(tree)],selectedItem(subtree),parent
	def func():
		global lst
		try:
			# Initilaise l to store integer values of input
			l = [int(entry.get()) for entry in entries]
			# Check if Allocated = Occupied + Available
			if l[0] == l[1] + l[2]:
				# Destroy the window
				window.destroy()
				# Prompt that their input has been validated
				messagebox.showinfo(title = "Input",message = "Verified!")
				sub_tabs = ["Alloc","Allocated","Occ","Occupied","Ava","Available"]
				for i in range(0,len(sub_tabs),2):
					cursor.execute("select sum(Total) from {} where Date = '{}' and DCHC = '{}'".format(var[0] + "_" + sub_tabs[i], date.today(),var[1]))
					tot = int(cursor.fetchall()[0][0])
					cursor.execute("update {} set `{}` = {}, Total = Gen + HDU + ICU + `ICU  Ventl` where DCHC = '{}' and Date = '{}'".format(var[0] + "_" + sub_tabs[i],tab_name,l[i//2],var[1],date.today()))
					cursor.execute("select sum(Total) from {} where Date = '{}' and DCHC = '{}'".format(var[0] + "_" + sub_tabs[i], date.today(),var[1]))
					newtot = int(cursor.fetchall()[0][0])
					tot = newtot-tot
					cursor.execute("update Govt_quota set {0} = {0} + {2} where Facility = '{1}' and Date = '{3}'".format(sub_tabs[i+1],selectedItem(tree),tot,date.today()))
					cnx.commit()
			else:
				raise TypeError
		# If any errors were encountered
		except Exception as e:
			print(e)
			# Show a warning
			messagebox.showwarning(title = "Error",message = "Invalid input")
		update_row(tree)
		update_row(subtree,list(var)[:2])
	# Initialise a tk frame
	frame = tk.Frame(window,bg = fg_color)
	# Initialise btn_values,entries
	btn_values,entries = ["Allocated","Occupied","Available"],[]
	dct = {'1':"Gen",'2':"HDU",'3':"ICU",'4':"ICU  Ventl"}
	tab_name = dct[parent.get()]
	que = "select {0}_Alloc.DCHC,{0}_Alloc.{3},{0}_Occ.{3},{0}_Ava.{3}, {0}_Ava.Date from {0}_Alloc inner join {0}_Ava on {0}_Alloc.Date = {0}_Ava.Date inner join {0}_Occ on {0}_Occ.Date = {0}_Alloc.Date  where {0}_Alloc.DCHC = '{1}' and {0}_Ava.DCHC = '{1}' and {0}_Occ.DCHC = '{1}' and {0}_Alloc.Date = '{2}'".format(var[0],var[1],date.today(),tab_name)
	print(que)
	cursor.execute(que)
	l = cursor.fetchall()
	# print(l)
	cur_stats = (l[0][1:4])
	# Run through a loop which runs thrice
	for i in range(3):
		# Initalise tk label with the btn_value
		tk.Label(frame,text = btn_values[i] + " (" + str(cur_stats[i]) + ")").pack(fill = 'x')
		# Initialise tk entry
		e = tk.Entry(frame)
		# Pack the entry box
		e.pack(fill = 'x')
		# Append the entry to the list entries
		entries.append(e)
	# Initialise tk button and pack it
	button = tk.Button(frame,text = "Done" ,padx = 20,pady = 10,command = lambda : func(),font = 'calibri 10').pack()
	# Pack the frame
	frame.pack(fill = 'both')
	# Execution stops here
	window.mainloop()

def admin_config(a):
	if selectedItem(tree) in ('Private Medical Colleges','Governement Covid Care Centres [CCC]'):
		return
	# Initialise a new window
	master = tk.Toplevel() 
	# Configure the geometry of the window
	master.geometry("145x145") 
	master.title("Hospital details")
	master = center_align(master)
	# Inialise a StringVar
	v = tk.StringVar(master, "0") 
	# Initialise a frame
	frame = tk.Frame(master)
	# Store the types of beds as valus and index as key in a dictionary
	values = {"General" : ["1","Gen"],"HDU" : ["2","HDU"],"ICU" : ["3","ICU"],"ICU Ventilator": ["4","ICU  Ventl"]} 
	# Iterate through the items in values
	for (text, value) in values.items(): 
		# Initialise a radiobutton and pack it
		ttk.Radiobutton(frame, text = text, variable = v,value = value[0],command = lambda : admin_input(a,master,frame,v)).pack(side = tk.TOP, ipady = 5)
	# Pack the frame
	frame.pack(fill = 'both')
	# Execution stops here
	master.mainloop() 
	
# Change the background and foreground colours for all elements based on theme
def theme_change():
	style = ttk.Style()
	i = 0
	frame.configure(bg = 'gray15')
	global theme,fg_color,bg_color
	if theme == "light":
		theme = "dark"
	else:
		theme = "light"
	if theme == "dark":
		fg_color,bg_color = "white","gray15"
	elif theme == 'light':
		fg_color,bg_color = "black","white"
	window.config(bg = bg_color)
	for el in all_children(window):
		try:
			el['bg'] = bg_color
			el['fg'] = fg_color
			if el['text'] != '* - Login(admin)-->Edit-->Refresh data':
				el.pack()
		except:
				elem = str(el)
				if elem in (".!frame3.!treeview",".!frame4.!treeview"):
					style.configure('Treeview', rowheight=40,fieldbackground=bg_color)
					style.configure("Treeview.Heading",background = bg_color,foreground  = "tan4",padding = 10)
					tree.tag_configure('even', background = bg_themes[theme]['tv_even'],foreground = bg_themes[theme]['fg']) 
					tree.tag_configure('odd', background = bg_themes[theme]['tv_odd'],foreground = bg_themes[theme]['fg'])
					try:
						write_child_node(d[selectedItem(tree)])
					except:
						pass
				elif "menu" in elem and i == 0:
					i = 1
					menu(menubar)
	messagebox.showinfo(title = "Themes",message = "Plot themes will update on refresh!")
	del el,elem,i,style

def selectItem(a):
	# Store the selected row in curItem
	curItem = selectedItem(tree)
	# Initialise path depending upon the selected row
	if theme == "light":
		path = "Graphs/{}.png".format(curItem)
	else:
		path = "Graphs/{}_dark.png".format(curItem)
	# Subtree title
	label['text'] = curItem
	try:
		# Initialise img as a tk comaptible image
		img = tkImage(path)
		# If the graphs have to be displayed
		if disp_graph == 1:
			# Update image on canvas
			canvas_copy = canvas.itemconfig(can_img,image = img)
			# Image title
			img_label['text'] = "Day-to-day trend and today's status"
			# Pack the img_label
			img_label.pack(side = 'top')
			# Pack the img_frame
			img_frame.pack(side = 'right',fill = 'both')
			# Execution stops here
			window.mainloop()
	# If any errors were encountered
	except:
		# Do nothing
		pass
# Lambda function display which writes a child node
display = lambda a : write_child_node(TABNAMES[tree.item(tree.focus())['values'][0]-1])


def display_graph(val):
	# Make disp_graph a global variable
	global disp_graph
	# If user wants to hide graphs
	if "Show" in val:
		# Change text
		button['text'] = "Hide Graphs"
		# Change disp_graph to 1
		disp_graph = 1
		# Pack the canvas
		canvas.pack(side = "top",anchor = tk.N,fill = 'both')
		# Pack the img_frame
		img_frame.pack()
		# Pack the bottomframe
		bottomframe.pack(expand = True,fill = 'both',side = 'left',anchor = tk.N)

	else:
		# Change text
		button['text'] = "Show Graphs"
		# Change disp_graph to 0
		disp_graph = 0
		# Drop img_frame
		img_frame.forget()
		# Configure bottomframe
		bottomframe.pack_configure(expand = True,fill = 'both',side = 'top',anchor = tk.N)
# Lambda functon refresh which is called when a user selects a row
refresh = lambda a : (display(a), selectItem(a))

def update_data():
	# Change cursor to loading cursor
	window.config(cursor = "watch")
	# Update the cursor
	window.update_idletasks()
	import project_backend,ind_trends
	# Make lst, global variables
	global lst,n
	if n != 0:
		# Forget refresh_label
		refresh_label.pack_forget()
		# Reset n to zero
		n = 0
	# Execute the commands in a try except block to catch any errors
	try:
		engine = project_backend.create_MySQL_engine(user,password)
		project_backend.write_tables()
		ind_trends.plot_figures(engine)
	except Exception as e:
		print("Encountered an error:",e)
	# Execute a query
	cursor.execute("select * from Govt_quota where Date = '{}'".format(date.today()+ timedelta(days = -1)))
	# Fetch all records
	lst = cursor.fetchall()
	# Update the date
	dt['text'] = " As of " + date.today().strftime("%d-%b-%Y") + "*"
	# Pack the dt label
	dt.pack()
	# Change cursor to pointer
	window.config(cursor = "")

def logout():
	# Change the text to login
	admin_login_button['text'] = "Login"
	# Remove edit menu potion
	menubar.delete(3,3)
	# Reconfigure admin_button command
	subtree.unbind('<Double-1>')
	admin_login_button.configure(command = admin)

def admin():
	# If user wants to login
	if admin_login_button['text'] == 'Login':
	
		def func(event = ""):
			# Use passwd, admin_window from outer function
			nonlocal passwd,admin_window,user_name
			# If the right password is entered
			if passwd.get() == "12345" and user_name.get() == "admin":
				# Change login button text
				admin_login_button['text'] = "Log Out"
				# Configure the button command
				admin_login_button.configure(command = lambda : logout())
				# Add edit option in the menu
				edit = tk.Menu(menubar, tearoff=0,background = bg_color,foreground = fg_color)
				menubar.add_cascade(label="Edit", menu=edit)
				# Add refresh data option
				edit.add_command(label ='Refresh data', command = lambda : update_data()) 
				# Bind double click to admin_config
				subtree.bind('<Double-1>', admin_config)
				now = datetime.now()
				with open("login_history.txt","a") as f:
					f.write(user_name.get() + '\t' +  str(date.today()) + "\t" + now.strftime("%H:%M:%S") + '\n')
				# Destroy the window
				admin_window.destroy()
				# Update the main window
				window.update()
			# If password has not been entered
			elif passwd.get() == "":
				# Show a warning
				tk.messagebox.showwarning(title="Authentication error", message="Password field is empty")
			else:
				# Show an error message
				tk.messagebox.showerror(title="Authentication error", message="Incorrect password or username")
		# Initialise StringVars
		username,passwd = tk.StringVar(),tk.StringVar()
		# Open a new window
		admin_window = tk.Toplevel()
		# Make the window non resizable
		admin_window.resizable(False, False)
		# Set a title for the window
		admin_window.title("Authenticate")
		# Configure the geometry of the window
		admin_window.geometry("300x168")
		# Initialise path
		path = "{}.jpeg".format("bed_stats_bg")
		# Initialise img as a tk comaptible image
		bg_tkimg = tkImage(path)
		# Initialise tk label
		bg_img  = tk.Label(admin_window,image=bg_tkimg)
		# Place bg_img on screen
		bg_img.place(x=0, y=0, relwidth=1, relheight=1)
		# Initialise window elements
		bg_frame = tk.Frame(admin_window,relief = "flat",height = 150,width = 200)
		uname = tk.Label(admin_window,text = 'Username',padx = 10,relief = "raised")
		password = tk.Label(admin_window,text = 'Password',padx = 10,relief = "raised")
		passwd_entry = tk.Entry(admin_window,textvariable = passwd,font = ('calibre',10,'normal'),show = '*',relief = "sunken") 
		user_name = tk.Entry(admin_window,textvariable = username,font = ('calibre',10,'normal'),relief = "sunken") 
		login_button = tk.Button(admin_window,text = "Login",command = func,padx = 20,bg = "limegreen")
		# Place uname on screen
		uname.place(in_ = bg_frame,relx = 0.05,rely = 0.1)
		# Place user_name on screen
		user_name.place(in_ = uname,rely = 1,relx = 0)
		# Place password on screen
		password.place(in_ = bg_frame,relx = 0.05,rely = 0.45)
		# Place passwd on screen
		passwd_entry.place(in_ = password,rely = 1,relx = 0)
		# Place login_button on screen
		login_button.place(in_ = bg_frame,rely = 0.75,relx = 0.25)
		# Place bg_frame on screen
		bg_frame.place(in_ = bg_img,relx = 0.2,rely = 0.05)
		# Bind func with enter key
		admin_window.bind('<Return>', func)
		# Execution stops here
		admin_window.mainloop()

# Sort a treeview column
def treeview_sort_column(tv, col, reverse):

	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	if col != "Facility":
		l = list(map(lambda x: [int(x[0]),x[1]], l))
	l.sort(reverse=reverse)
	for index, (val, k) in enumerate(l):

		tv.move(k, '', index)

	tv.heading(col, command=lambda _col=col: treeview_sort_column(tv, _col, not reverse))
	
# Function to bakcup the MySQL database
def bkup():
	import os
	# Change directory to Sql_Bkup
	os.mkdir("Sql_Bkup")
	os.chdir("Sql_Bkup")
	# Create sql file and save it with today's date
	os.system("mysqldump -u {} project -p > Project_db_{}.sql".format(user,date.today().strftime("%b_%d")))
	# Go back to parent directory
	os.chdir("..")
	# Confirm
	print("Done")

# List all the elements present in the current window	
def all_children (window) :
	_list = window.winfo_children()
	for item in _list :
		if item.winfo_children() :
			_list.extend(item.winfo_children())
	return _list
	
# Write the elements to a treeview
def write_tree(tv,head_only = False):
	# Iterate through the columns
	for col in columns:
		# Give the headings for the columns
		tv.heading(col, text = col,command=lambda _col=col: treeview_sort_column(tv, _col, False))
		# If the column is not Facility
		if col != "Facility":
			# Center align the values
			tv.column(col,anchor = tk.CENTER,width = 15)
		# For Facility column
		else:
			# Specify width of column
			tv.column(col,width = 300)
	# If rows have to be written
	if not head_only:
		# Initialise d_tags
		d_tags = {0:"even",1:"odd"}
		step = 0
		cursor.execute("select * from Govt_quota where Date = '2020-11-18' and Facility in ('Private Medical Colleges')")
		l = cursor.fetchall()
		# Iterate through lst
		for i,el in enumerate(lst):
			# Update dictionary
			d[el[1]] = TABNAMES[i]
			# Insert row into tree
			# tv.insert("","end",i, values = el,tag = d_tags[i%2])
			if 0 not in el:
				tv.insert("",i, values = el,tag = d_tags[i%2])
			else:
				tv.insert("",i, values = l[step],tag = d_tags[i%2])
				step += 1
		# Configure the tags
		# tv.tag_configure('even', background='light blue') 
		tv.tag_configure('even', background = bg_themes[theme]['tv_even'],foreground = bg_themes[theme]['fg']) 
		# tv.tag_configure('odd', background='LightSeaGreen') 
		tv.tag_configure('odd', background = bg_themes[theme]['tv_odd'],foreground = bg_themes[theme]['fg']) 
		# Pack the tree
		tv.pack(side ='top',fill = 'x',expand = True)

# Get logs on request
def get_logs():
	win = tk.Toplevel()
	d_tags = {0:"even",1:"odd"}
	cols = ["User","Date","Time"]
	logs_tree = ttk.Treeview(win, columns=cols, show='headings')
	verscrlbar = ttk.Scrollbar(win,orient ="vertical",command = logs_tree.yview)
	for col in cols:
		# Give the headings for the columns
		logs_tree.heading(col, text = col)
		logs_tree.column(col,anchor = tk.CENTER,width = 150)
	# If rows have to be written
	with open("login_history.txt","r") as f:
		txt = f.readlines()
	for i,line in enumerate(txt):
		logs_tree.insert("",i, values = line,tag = d_tags[i%2])
	logs_tree.tag_configure('even', background = bg_themes[theme]['tv_even'],foreground = bg_themes[theme]['fg']) 
	logs_tree.tag_configure('odd', background = bg_themes[theme]['tv_odd'],foreground = bg_themes[theme]['fg']) 
	verscrlbar.pack(fill = "y",side = "right")
	logs_tree.pack()
	win = center_align(win)

# Close the app 
def close_app():
	# Close matplotlib
	plt.close('all')
	# Destroy the window
	window.destroy()
	
# Center align a window
def center_align(wdw):
	w = wdw.winfo_reqwidth()
	h = wdw.winfo_reqheight()
	ws = wdw.winfo_screenwidth()
	hs = wdw.winfo_screenheight()
	x = (ws - w)/2.15
	y = (hs - h)/2
	wdw.geometry('+%d+%d' % (x, y))
	return wdw

# Function which handles the about us section
def about():
	# Create a new window
	win = tk.Toplevel()
	# Choose background colours based on theme
	if theme ==  "dark":
		fgcolor = bdcolor = "DarkSlateGray4"
	else:
		fgcolor = bdcolor = "dark green"
	win['bg'] = bg_color
	# Update the title of the window
	win.title("About")
	# Initalise a frame on which all blocks will be displayed
	frame = tk.Frame(win,bg = bg_color,highlightbackground = bdcolor, highlightthickness = 5)
	# Initialise the labels
	t = tk.Label(frame,text='\nProvides the availability status of\nCOVID-19 beds in hospitals in Bengaluru',bg = bg_color,fg = fgcolor,font = (None ,12,"bold")).pack()
	credits = tk.Label(frame,text = '\nby\nPrabhav B Kashyap & Ranganath M R\n',font = (None ,10,"bold"),bg = bg_color,fg = fgcolor).pack()
	# Pack the frame
	frame.pack()
	# Center align the window
	win = center_align(win)
# Initialise tk window
window = tk.Tk()
# Configure window background
window.config(bg = bg_color)
# Set title for the window
window.title("Home Page")
# Configure the window geometry
window.geometry("1920x1080")
# Icon image
p1 = tkImage("{}.jpeg".format("bed_stats_bg")) 
# Configure iconphoto
window.iconphoto(False, p1) 
# Configure close button
window.protocol("WM_DELETE_WINDOW", close_app)
# Initialise window elements
frame = tk.Frame(window)
heading = tk.Frame(window,bg = bg_color)
bottomframe = tk.Frame(window,bg = bg_color,height = 800)
label = tk.Label(bottomframe,text = '',padx = 10,bg = bg_color,fg = fg_color,pady = 10)
img_frame = tk.Frame(window,bg = bg_color,width = 800)
img_label = tk.Label(img_frame,text = '',padx = 10,bg = bg_color,fg = fg_color,pady = 10)
canvas = tk.Canvas(img_frame, bg = bg_color,height = 660,width = WIDTH)
title = tk.Label(heading,text = "Bengaluru: COVID-19 Hospital Bed Status",pady = 20,font = ("KacstTitle" ,20,"bold"),bg = bg_color,fg = fg_color)
admin_login_button = tk.Button(heading,text = "Login",command = admin,padx = 10,bg = bg_color,fg = fg_color )
# Pack the heading
heading.pack(fill = 'both')
# Configure the labels
label.config(font=("None", 12,"bold"))
img_label.config(font=("None", 12,"bold"))
# Pack the label
img_label.pack(fill = 'x',expand = True)
# Pack login button
admin_login_button.pack(side = "right",anchor = tk.NE)
# Initialise refresh label,dt
dt = tk.Label(window,text = txtlabel,bg = bg_color,fg = fg_color)
# Pack the window title
title.pack(side = 'top')
# Pack the label dt
dt.pack()
# If today's data is not found in the database
if n != 0:
	refresh_label = tk.Label(window,text = '* - Login(admin)-->Edit-->Refresh data',padx = 10,bg = bg_color,fg = fg_color,font = (None ,10))
	# Pack the refresh label
	refresh_label.pack(anchor = 'e')
# Initialise a tk frame
frame = tk.Frame(window)
# Pack the frame
frame.pack(fill = 'x',side = 'top',anchor = tk.N)
# Initialise a main treeview
tree = ttk.Treeview(frame, columns=columns, show='headings',height = len(TABNAMES))
# Initialise a sub treeview
subtree = ttk.Treeview(bottomframe, columns=columns, show='headings')
# Bind refresh with tree so that it calls the function when a row is selected
tree.bind("<<TreeviewSelect>>", refresh)
# Bind refresh with tree so that it calls the function when a row is double clicked
tree.bind('<Double-1>', refresh)
# Initialise a tk menu
menubar = tk.Menu(window,bg = bg_color,fg = fg_color)
# Initialise file menu in the menubar
file = tk.Menu(menubar,tearoff = 0)
help = tk.Menu(menubar,tearoff = 0)
menubar.add_cascade(label ='File', menu = file) 
menubar.add_cascade(label ='Help', menu = help) 
def menu(menubar,configure = False):
	# Initialise file menu in the menubar
	file.delete(0,5)
	help.delete(0,1)
	# Add various options
	file.add_command(label ='Change theme', command = theme_change,background = bg_color,foreground = fg_color) 
	file.add_command(label ='Admin logins', command = get_logs,background = bg_color,foreground = fg_color) 
	file.add_command(label = "Backup",command = bkup,background = bg_color,foreground = fg_color ) 
	# Add a seperator
	file.add_separator(background = bg_color) 
	# Add exit option
	file.add_command(label ='Exit', command = close_app,background = bg_color,foreground = fg_color)
	help.add_command(label ='About         ', command = about,background = bg_color,foreground = fg_color) 
	# Configure window to have menubar
	window.config(menu = menubar)
menu(menubar,True)

# Configure styles
style = ttk.Style()
style.configure('Treeview', rowheight=40,fieldbackground=bg_color)
style.configure("Treeview.Heading",background = bg_color,foreground  = "tan4",padding = 10) 
# Initialise a tk button for hiding/showing graphs
button = tk.Button(window,text = "Hide Graphs",command = lambda : display_graph(button['text']),padx = 10 ,bg = bg_color,fg = fg_color)
# Pack the button
button.pack(side = "bottom",anchor = "s")
# Initialise a vertical scrollbar
verscrlbar = ttk.Scrollbar(bottomframe,orient ="vertical",command = subtree.yview)
# Pack bottomframe
bottomframe.pack(side = "left",anchor = tk.N,fill = "both",expand = True)
# Add scrollbar to subtree
subtree.configure(yscrollcommand = verscrlbar.set)
# Pack the label
label.pack(side = 'top',fill = 'x',anchor = tk.N)
# Create an image on canvas
can_img = canvas.create_image((450,300),image = None)
# Pack the canvas
canvas.pack(side = "right",expand = True,fill = 'both',anchor = tk.NE)
# Update tree
write_tree(tree)
# Execution stops here
window.mainloop()
print('Exit')
