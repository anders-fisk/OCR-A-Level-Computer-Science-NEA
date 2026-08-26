
from numpy import random
import mesa

class PopulationAgent(mesa.Agent) :
	def __init__(self,unique_id,model):
		super().__init__(unique_id,model)
		self.state = 'S'
		self.neighbour_agents = []
		
	def step(self):
		#prints agent id and state
		print(f'I am agent{self.unique_id} and my state is {self.state}')
		#assigns a list of neighbour agents, agent itself isnt included

class PopulationModel(mesa.Model):
	def __init__(self, travelRadius):
		self.travelRadius = travelRadius
		self.width = width
		self.height = height

		#agents can't be within the same cell in the grid
		self.grid = mesa.space.SingleGrid(self.width, self.height, True)
		#defines scheduler that will activate all agents simultaenously at each time step
		self.schedule = mesa.time.SimultaneousActivation(self)

		#creates reference array of coordinates for agents to be added to
		refCoordinates = [[x,y] for y in range(0,self.height) for x in range(0,self.width)]

		#loop to place agents in grid and scheduler
		for i in refCoordinates:
			a = PopulationAgent(refCoordinates.index(i), self)
			#adds the agent to the scheduler
			self.schedule.add(a)
			#places agent within the grid 
			self.grid.place_agent(a, (i[0],i[1]))

		for i in self.grid: 
			print(f'Finding the neighbouring agents for agent {i.unique_id} at {i.pos[0]},{i.pos{1}}')
			#max and min x,y neighbour positions
			minxPos, maxxPos = a.pos[0]-self.travelRadius, a.pos[0]+self.travelRadius
			minyPos, maxyPos = a.pos[1]-self.travelRadius, a.pos[1]+self.travelRadius

			#coordinate validation
			if minxPos < 0 : minxPos = 0
			if maxxPos > self. width: maxxPos = self.width
			if minyPos < 0 : minyPos = 0
			if maxyPos > self.width: maxyPos = self.height

			#creates a list of all possible positions with range of the max and min x,y neighbour positions
			total_radius_positions = [[x,y] for x in range(minxPos,maxxPos+1) 
											for y in range(minyPos,maxyPos+1)]

			#removes the position of the agent it's finding the neighbours of 
			total_radius_positions.remove([a.pos[0],a.pos[1]])
			#assigns the list as an attribute
			a.neighbour_agents = total_radius_positions
			print(f'Here are the neighbouring agents: {total_radius_positions}')

	def step(self):
		#advances the model by one time-step by calling the PopulationAgent class step method
		self.schedule.step()

t = PopulationModel(1)


