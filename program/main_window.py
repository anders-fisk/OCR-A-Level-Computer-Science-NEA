from population import PopulationModel
import tkmacosx as tkmacosx
import tkinter as tk
import random

window = tk.Tk()
window.title("Main Menu")
window.geometry("1440x900")

def draw_canvas(canvas) :
	#reference dictionary to link agent and square coords
	grid = {}
	#nested for loop for coordinates
	ix = -1
	iy = -1
	for y in range(3,900,5) :
		ix += 1
		iy = -1
		for x in range(3,520,5) :
			iy += 1
			#creates and packs squares
			rectangle = canvas.create_rectangle(y, x, y+5, x+5, fill="white") 
			grid[ix,iy] = rectangle
	return grid

def categorise_agents(model,canvas,squares) :
	#iterates through agents in the model
	for a in model.grid :
		#stops model if currenlty running
		if a.state == 'S' :
			canvas.itemconfig(squares[a.pos], fill='white')
		elif a.state == 'I' :
			canvas.itemconfig(squares[a.pos], fill='pink')
		elif a.state == 'R' : 
			canvas.itemconfig(squares[a.pos], fill='green')
		elif a.state == 'F' : 
			canvas.itemconfig(squares[a.pos], fill='blue')

def retrieve_input(self,model,inputText,inputBox):
	#retrieves the text from the text box, 1.0 is beginning, tk.END is end
	paramaterValue = inputText.get("1.0",tk.END)
	#deletes text from input box so isnt added on next time function is run
	inputText.delete("1.0",tk.END)
	#validates whether the value is an integer or float
	try: 
		paramaterValue = int(paramaterValue)
	except ValueError:
		paramaterValue = float(paramaterValue)

	#input validation as outlined via test plan
	match inputBox :
		#num of time-steps box
		case 1 :
			if paramaterValue > 0 and paramaterValue < 10000 and type(paramaterValue) == int: 
				model.timeStepsNum = paramaterValue
				clear(self,model,self.squareCanvas,self.squareGrid)
			elif paramaterValue < 0 or paramaterValue > 10000:
				create_popup('Value is out of range')
			else : 
				create_popup('Please enter a valid value')
		#number of initial infections
		case 2 :
			if paramaterValue > 0 and paramaterValue <= 18720 and type(paramaterValue) == int: 
				model.initialInfections = paramaterValue
				clear(self,model,self.squareCanvas,self.squareGrid)
			elif paramaterValue < 0 or paramaterValue > 18720:
				create_popup('Value is out of range')
			else : 
				create_popup('Please enter a valid value')
		#travel radius
		case 3 : 
			if paramaterValue > 0 and paramaterValue <= 5 and type(paramaterValue) == int: 
				model.travelRadius = paramaterValue
				clear(self,model,self.squareCanvas,self.squareGrid)
			elif paramaterValue < 0 or paramaterValue > 5:
				create_popup('Value is out of range')
			else : 
				create_popup('Please enter a valid value')
		#infection rate box
		case 4 :
			if paramaterValue >= 0.0 and paramaterValue <= 1.0 and type(paramaterValue) == float:
				model.infectionRate = paramaterValue
				clear(self,model,self.squareCanvas,self.squareGrid)
			elif paramaterValue < 0.0 or paramaterValue > 1.0:
				create_popup('Value is out of range')
			else : 
				create_popup('Please enter a valid value')
		#recovery rate box
		case 5 :
			if paramaterValue >= 0.0 and paramaterValue <= 1.0 and type(paramaterValue) == float:
				model.recoveryRate = paramaterValue
				clear(self,model,self.squareCanvas,self.squareGrid)
			elif paramaterValue < 0.0 or paramaterValue > 1.0:
				create_popup('Value is out of range')
			else : 
				create_popup('Please enter a valid value')
		#fatality rate box
		case 6 :
			if paramaterValue >= 0.0 and paramaterValue <= 1.0 and type(paramaterValue) == float:
				model.fatalityRate = paramaterValue
				clear(self,model,self.squareCanvas,self.squareGrid)
			elif paramaterValue < 0.0 or paramaterValue > 1.0:
				create_popup('Value is out of range')
			else : 
				create_popup('Please enter a valid value')

def create_button(ppage,ptext,pheight, pwidth): 
	#assigns constant and paramater values to a new button
	return tkmacosx.Button(ppage,borderless=1,font=("Helvetica", 30),text=ptext,height=pheight,width=pwidth,bg='#3399ff',fg='#FFFFFF') 

def create_popup(message):
	#cretes new window
	popup = tk.Toplevel(window)
	popup.title("Error")
	#sets paramater text in window
	label = tk.Label(popup, text=message)
	#aligns in center of screen
	label.pack(pady=10,padx=10)
	#adds a close button for the user
	close_button = tk.Button(popup, text="Close", command=popup.destroy)
	close_button.pack(pady=10)
	#specifies width,heigh of the popup window itself, then the coords to place the window within the larger simulation page 
	popup.geometry('178x90+631+405')

def get_page(items,pageNum,model):
	#stops model if currently running
	#iterates through items list and gets rid of each item from page
	[items[i].pack_forget() for i in range(len(items)) if i < 13 ]
	[items[i].destroy() for i in range(len(items)) if i > 13 ]
	#loads the specified page based on number paramater 
	if pageNum == 0:
		MainMenu()
	elif pageNum == 1 :
		FullSimulation(model)
	elif pageNum == 2:
		PreSets(model)
	elif pageNum == 3:
		Tutorial(model)

def time_loop(model,canvas,squares) :
	#when time-step called pause set to false so simulation starts
	model.pause = False
	#while time-steps do not exceed user set limit (while model is out of date) and pause is false
	while model.schedule.time != len(model.grid[0][0].memory) :
		for i in model.grid :
			i.state = i.memory[model.schedule.time]
		categorise_agents(model,canvas,squares)
		window.update()
		model.schedule.time += 1
	#while the model is up to date and not paused
	while model.schedule.time < model.timeStepsNum and model.pause == False: 
		#calls the model and agent steps methods
		model.step()
		#changes grid colour
		categorise_agents(model,canvas,squares)
		#updates GUI
		window.update()

def stop(model) :
	model.pause = True

def backward_time_step(self,model,canvas,squares) : 
	#means that the time-step time will be set to the previous
	self.model.schedule.time -= 1
	#pauses the model
	stop(model)
	for i in model.grid:
		#agent state will be set to previous time-step state
		i.state = i.memory[self.model.schedule.time]
	#updates colours
	categorise_agents(model,canvas,squares)
	window.update()

def forward_time_step(self,model,canvas,squares) :
	#if model is up to date
	if self.model.schedule.time == len(model.grid[0][0].memory) :
		model.step()
		#changes colours
		categorise_agents(model,canvas,squares)
		window.update()
	#if model is outdated 
	else : 
		#pauses model
		stop(model)
		self.model.schedule.time += 1
		for i in model.grid :
			#gets state of agents one ahead
			i.state = i.memory[self.model.schedule.time]
		#changes colours
		categorise_agents(model,canvas,squares)
		window.update()

def clear(self,model,canvas,squares) :
	#resets population and neighbouring agents i.e if travel radius changes
	model.init_neighbour_agents()
	#resets time of simulation to zero
	self.model.schedule.time = 0
	#stops simulation in progress
	stop(model)
	#randomly selects agents to be selected based on initial infections paramater
	initialInfectedAgents = [random.randint(0,18720) for i in range(model.initialInfections)]
	for i in model.grid :
		#resets memory dictionary so each agent has no memor of previous states 
		i.memory = {}
		#if agent is in initial infections list set state to infected, else set to susceptible
		if i.unique_id in initialInfectedAgents :
			i.state = 'I'
		else:
			i.state = 'S'

	#colours agents based on state
	categorise_agents(model,canvas,squares)
	#updates GUI
	window.update() 

class MainMenu :
	#initialises the objects on the page
	def __init__(self) :
		#assigns the model
		self.model = PopulationModel()

		#creates each button for the main menu page
		self.b1 = create_button(window,"Full Simulation",750,700)
		self.b2 = create_button(window,"Pre-Sets",385,700)
		self.b3 = create_button(window,"Tutorial",385,700)
		#adds each button to a list
		self.objects = [self.b1,self.b2,self.b3]

		#packs each button into page
		self.b1.pack(anchor='center',side='left',pady=20,padx=10)
		self.b2.pack(anchor='n',pady=20,padx=10)
		self.b3.pack(anchor='s',pady=20,padx=10)

		#runs get_page() method to run with objects list when button is clicked 
		self.b1.configure(command=lambda: get_page(self.objects,1,self.model))
		self.b2.configure(command=lambda: get_page(self.objects,2,self.model))
		self.b3.configure(command=lambda: get_page(self.objects,3,self.model))

class FullSimulation :
	def __init__(self,model) :
		#assigns model
		self.model = model
		#initiates neighbouring agents list for each agent
		model.init_population()
		model.init_neighbour_agents()

		#back button
		self.b1 = create_button(window,"X",50,50)
		#temporary assignment to clear function
		self.b1.configure(command=lambda: get_page(self.objects,0,model)) 

		#canvas
		self.squareCanvas = tk.Canvas(window,bg="#FFFFFF", height=521, width=901)

		#time-step buttons
		self.t1 = create_button(window,"<",50,50)
		self.t2 = create_button(window,">",50,50)

		#play/pause buttons buttons
		self.p1 = create_button(window,"▷",50,50)
		self.p2 = create_button(window,"⏸",50,50)

		#defines input boxes
		self.i1 = tk.Text(window,width=4,height=1.25,bg='#3399ff',fg='#FFFFFF',font=("Helvetica",40))
		self.i2 = tk.Text(window,width=4,height=1.25,bg='#3399ff',fg='#FFFFFF',font=("Helvetica",40))
		self.i3 = tk.Text(window,width=4,height=1.25,bg='#3399ff',fg='#FFFFFF',font=("Helvetica",40))
		self.i4 = tk.Text(window,width=4,height=1.25,bg='#3399ff',fg='#FFFFFF',font=("Helvetica",40))
		self.i5 = tk.Text(window,width=4,height=1.25,bg='#3399ff',fg='#FFFFFF',font=("Helvetica",40))
		self.i6 = tk.Text(window,width=4,height=1.25,bg='#3399ff',fg='#FFFFFF',font=("Helvetica",40))

		self.b1.pack(anchor='n',side='right',pady=5,padx=5)

		self.squareCanvas.pack(side='top',anchor='w',pady=45,padx=30)

		self.t1.pack(anchor='s',side='left',pady=60,padx=30)
		self.t2.pack(anchor='s',side='left',pady=60,padx=30)

		self.p1.pack(anchor='s',side='left',pady=60,padx=30)
		self.p2.pack(anchor='s',side='left',pady=60,padx=30)

		#assigns backwards time-step function to previous arrow button
		self.t1.configure(command=lambda: backward_time_step(self,model,self.squareCanvas,self.squareGrid))
		#assings forward time-step function to forward arrow button
		self.t2.configure(command=lambda: forward_time_step(self,model,self.squareCanvas,self.squareGrid))

		#assigns time-step function to play button
		self.p1.configure(command=lambda: time_loop(model,self.squareCanvas,self.squareGrid))
		#assigns pause function to pause button
		self.p2.configure(command=lambda: stop(model))

		#packs input boxes
		#have to be in reverse to be assigned correctly due to packing from the right 
		#fatality rate
		self.i6.pack(side='right',pady=60,padx=25)
		#recovery rate
		self.i5.pack(side='right',pady=60,padx=25)
		#infection rate
		self.i4.pack(side='right',pady=60,padx=25)
		#travel radius
		self.i3.pack(side='right',pady=60,padx=25)
		#initial infections
		self.i2.pack(side='right',pady=60,padx=25)
		#time steps num
		self.i1.pack(side='right',pady=60,padx=25)

		#text labels for user accessibility	
		self.i1text = tk.Label(window, text="Time Steps\n(1-10,000)")
		self.i1text.place(x=519, y=735)

		self.i2text = tk.Label(window, text="Initial Infections\n(1-18,720)")
		self.i2text.place(x=655, y=735)

		self.i3text = tk.Label(window, text="Travel Radius\n(1-5)")
		self.i3text.place(x=811, y=735)

		self.i4text = tk.Label(window, text="Infection Rate\n(0.0-1.0)")
		self.i4text.place(x=960, y=735)

		self.i5text = tk.Label(window, text="Recovery Rate\n(0.0-1.0)")
		self.i5text.place(x=1109, y=735)

		self.i6text = tk.Label(window, text="Fatality Rate\n(0.0-1.0)")
		self.i6text.place(x=1266, y=735)

		self.i7text = tk.Label(window, text="Key: White: Susceptible, Pink: Infected, Green: Recovered: Blue: Fatality")
		self.i7text.place(x=31, y=575)

		self.objects = [self.b1,self.t1,self.t2,self.p1,self.p2,self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,self.squareCanvas, 
						self.i1text,self.i2text,self.i3text,self.i4text,self.i5text,self.i6text,self.i7text]

		# #calls main menu class
		# self.b1.configure(command=lambda: get_page(self.objects,0,self.model))
		
		#binds retrieve input function to input box whenever enter key is pressed 
		self.i1.bind("<Return>",lambda event: retrieve_input(self,model,self.objects[5],1))
		self.i2.bind("<Return>",lambda event: retrieve_input(self,model,self.objects[6],2))
		self.i3.bind("<Return>",lambda event: retrieve_input(self,model,self.objects[7],3))
		self.i4.bind("<Return>",lambda event: retrieve_input(self,model,self.objects[8],4))
		self.i5.bind("<Return>",lambda event: retrieve_input(self,model,self.objects[9],5))
		self.i6.bind("<Return>",lambda event: retrieve_input(self,model,self.objects[10],6))

		#creates reference square grid
		self.squareGrid = draw_canvas(self.squareCanvas)
		#draws grid
		self.squareCanvas.pack()

class PreSets : 
	def __init__(self,model) :
		self.model = model
		self.b1 = create_button(window,"X",50,50)
		self.b1.pack(anchor='n',side='right',pady=5,padx=5)
		self.objects = [self.b1]

		self.b1.configure(command=lambda: get_page(self.objects,0,model))

class Tutorial:
	def __init__(self,model) :
		self.b1 = create_button(window,"X",50,50)
		self.b1.pack(anchor='n',side='right',pady=5,padx=5)
		self.objects = [self.b1]
		self.b1.configure(command=lambda: get_page(self.objects,0,model))

#loops the page so it's ineractable
main = MainMenu()


window.mainloop()

