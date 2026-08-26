from numpy import random
import mesa

class PopulationAgent(mesa.Agent) :
	def __init__(self,unique_id,model):
		super().__init__(unique_id,model)
		self.state = 'S'
		self.neighbour_agents = []
		self.memory = {}
		
	def step(self):
		#infection algorithm
		#if the agent is infected
		if self.state == 'I' :
			#iterates through agent list
			for b in self.neighbour_agents :
				#gets the agent at that coordinate position
				neighbour = self.model.grid.get_cell_list_contents([(b[0], b[1])])[0]
				if neighbour.state == 'S' : 
					#chance of infection
					randnum = (random.randint(1,10000)/10000)
					if randnum <= self.model.infectionRate :
						neighbour.state = 'I'			

class PopulationModel(mesa.Model):
	def __init__(self):
		self.travelRadius = 1
		self.initialInfections = 4
		self.infectionRate = 0.2
		self.recoveryRate = 0.01
		self.fatalityRate = 0.01
		self.timeStepsNum = 100
		self.width = 180
		self.height = 104
		self.pause = False

		#agents can't be within the same cell in the grid
		self.grid = mesa.space.SingleGrid(self.width, self.height, True)
		#defines scheduler that will activate all agents randomly at each time step
		self.schedule = mesa.time.RandomActivation(self)

	#defines a method to create population
	def init_population(self):
		#creates reference array of coordinates for agents to be added to
		refCoordinates = [[x,y] for y in range(0,self.height) for x in range(0,self.width)]

		#generates user-set amount of agent ids to be infected
		initialInfectedAgents = [random.randint(0,18720) for i in range(self.initialInfections)]

		#loop to place agents in grid and scheduler
		for d,i in enumerate(refCoordinates):
			a = PopulationAgent(d, self) 
			
			#if agent id in initial infected list
			if d in initialInfectedAgents : 
				a.state = 'I'

			#adds the agent to the scheduler
			self.schedule.add(a)
			#places agent within the grid 
			self.grid.place_agent(a, (i[0],i[1]))

	#defines a method to generate neighbouring agents list for each agent 
	def init_neighbour_agents(self) : 
		for a in self.grid: 
			#max and min x,y neighbour positions
			minxPos, maxxPos = a.pos[0]-self.travelRadius, a.pos[0]+self.travelRadius
			minyPos, maxyPos = a.pos[1]-self.travelRadius, a.pos[1]+self.travelRadius
			#coordinate validation
			if minxPos < 0 : minxPos = 0
			if maxxPos > self. width -1: 
				maxxPos = self.width - 1
			if minyPos < 0 : minyPos = 0
			if maxyPos > self.height -1: 
				maxyPos = self.height - 1

			#creates a list of all possible positions with range of the max and min x,y neighbour positions
			total_radius_positions = [[x,y] for x in range(minxPos,maxxPos+1) 
											for y in range(minyPos,maxyPos+1)]

			#removes the position of the agent it's finding the neighbours of 
			total_radius_positions.remove([a.pos[0],a.pos[1]])

			#assigns the list as an attribute
			a.neighbour_agents = total_radius_positions

	def step(self):
		#iterates through population
		#counts number of suceptible agents
		for a in self.grid:
			#assigns state to time-step number in dictionary
			a.memory[self.schedule.time] = a .state
			if a.state == 'I' : 
				#random chance
				randnum = (random.randint(1,10000)/10000)
				#avoids bias towards fatality or recovery by 50/50 chance
				if random.randint(0,9) < 5 :
					#chance of recovery
					if randnum <= self.recoveryRate :
						a.state = 'R'	
					else:
						#chanve of fatality
						if a.state != 'R' and randnum <= self.fatalityRate :
							a.state = 'F'
				#flipped so in this case fatality gets cehcked first
				else :
					if a.state != 'R' and randnum <= self.fatalityRate :
							a.state = 'F'
					else : 
						if randnum <= self.recoveryRate :
							a.state = 'R'	
		self.schedule.step()



 #latest change is switching randomint from 0 to 1 so if infectionrate or recoveryrate is set to 0, none recover or none are infected
