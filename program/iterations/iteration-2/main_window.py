import tkmacosx as tkmacosx
import tkinter as tk
import time

window = tk.Tk()
window.title("Main Menu")
window.geometry("1440x900")

def draw_canvas(canvas) :
	#nested for loop for coordinates
	for y in range(3,900,5) :
		for x in range(3,520,5) :
			#creates and packs squares
			rectangle = canvas.create_rectangle(y, x, y+5, x+5, fill="white") 
	canvas.pack()

def retrieve_input(inputText,inputBox):
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
		case 1 :
			if paramaterValue > 0 and paramaterValue < 5001 and type(paramaterValue) == int: 
				print(f'{paramaterValue} is valid')
			else :
				print(f'{paramaterValue} is not valid')
		case 2 :
			if paramaterValue > 0 and paramaterValue < 5000 and type(paramaterValue) == int: 
				print(f'{paramaterValue} is valid')
			else :
				print(f'{paramaterValue} is not valid')
		case 3 : 
			if paramaterValue > 0 and paramaterValue < 11 and type(paramaterValue) == int: 
				print(f'{paramaterValue} is valid')
			else :
				print(f'{paramaterValue} is not valid')
		case 4 | 5 | 6 :
			if paramaterValue > 0.0 and paramaterValue < 1.0 and type(paramaterValue) == float:
				print(f'{paramaterValue} is valid')
			else :
				print(f'{paramaterValue} is not valid')

def createButton(ppage,ptext,pheight, pwidth): 
	#assigns constant and paramater values to a new button
	return tkmacosx.Button(ppage,borderless=1,font=("Helvetica", 30),text=ptext,height=pheight,width=pwidth,bg='#3399ff',fg='#FFFFFF') 

def getPage(items,pageNum):
	#iterates through items list and gets rid of each item from page
	[items[i].pack_forget() for i in range(len(items))]
	#loads the specified page based on number paramater 
	if pageNum == 0:
		MainMenu()
	elif pageNum == 1 :
		FullSimulation()
	elif pageNum == 2:
		PreSets()
	elif pageNum == 3:
		Tutorial()

class MainMenu :
	#initialises the objects on the page
	def __init__(self) :

		#creates each button for the main menu page
		self.b1 = createButton(window,"Full Simulation",750,700)
		self.b2 = createButton(window,"Pre-Sets",385,700)
		self.b3 = createButton(window,"Tutorial",385,700)
		#adds each button to a list
		self.objects = [self.b1,self.b2,self.b3]

		#packs each button into page
		self.b1.pack(anchor='center',side='left',pady=20,padx=10)
		self.b2.pack(anchor='n',pady=20,padx=10)
		self.b3.pack(anchor='s',pady=20,padx=10)

		#runs getPage() method to run with objects list when button is clicked 
		self.b1.configure(command=lambda: getPage(self.objects,1))
		self.b2.configure(command=lambda: getPage(self.objects,2))
		self.b3.configure(command=lambda: getPage(self.objects,3))

class FullSimulation :
	def __init__(self) :
		#back button
		self.b1 = createButton(window,"X",50,50)

		#canvas
		self.squareCanvas = tk.Canvas(window,bg="#FFFFFF", height=521, width=901)

		#time-step buttons
		self.t1 = createButton(window,"<",50,50)
		self.t2 = createButton(window,">",50,50)

		#play/pause buttons buttons
		self.p1 = createButton(window,"▷",50,50)
		self.p2 = createButton(window,"⏸",50,50)

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

		#packs input boxes
		#have to be in reverse to be assigned correctly due to packing from the right 
		#fatality rate
		self.i6.pack(anchor='s',side='right',pady=60,padx=25)
		#recovery rate
		self.i5.pack(anchor='s',side='right',pady=60,padx=25)
		#infection rate
		self.i4.pack(anchor='s',side='right',pady=60,padx=25)
		#travel radius
		self.i3.pack(anchor='s',side='right',pady=60,padx=25)
		#initial infections
		self.i2.pack(anchor='s',side='right',pady=60,padx=25)
		#population size
		self.i1.pack(anchor='s',side='right',pady=60,padx=25)

		self.objects = [self.b1,self.t1,self.t2,self.p1,self.p2,self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,self.squareCanvas]

		#calls main menu class
		self.b1.configure(command=lambda: getPage(self.objects,0))

		#binds retrieve input function to input box whenever enter key is pressed 
		self.i1.bind("<Return>",lambda event: retrieve_input(self.objects[5],1))
		self.i2.bind("<Return>",lambda event: retrieve_input(self.objects[6],2))
		self.i3.bind("<Return>",lambda event: retrieve_input(self.objects[7],3))
		self.i4.bind("<Return>",lambda event: retrieve_input(self.objects[8],4))
		self.i5.bind("<Return>",lambda event: retrieve_input(self.objects[9],5))
		self.i6.bind("<Return>",lambda event: retrieve_input(self.objects[10],6))

		#creates reference square grid
		draw_canvas(self.squareCanvas)

class PreSets : 
	def __init__(self) :
		self.b1 = createButton(window,"X",50,50)
		self.b1.pack(anchor='n',side='right',pady=5,padx=5)
		self.objects = [self.b1]

		self.b1.configure(command=lambda: getPage(self.objects,0))

class Tutorial:
	def __init__(self) :
		self.b1 = createButton(window,"X",50,50)
		self.b1.pack(anchor='n',side='right',pady=5,padx=5)
		self.objects = [self.b1]
		self.b1.configure(command=lambda: getPage(self.objects,0))

MainMenu()
#loops the page so its interactable
window.mainloop()

