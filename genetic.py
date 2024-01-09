from board import Board
import random
import numpy as np
import time

#Necessary to be able to update the board with wanted values
#Makes the board have all 0's in order to create the mutated board
def reset_board(board):
	for i in range(5):
		for j in range(5):
			board.get_map()[i][j] = 0
	return board

#Updates the board to the given state by using a blank board
def update_board(board,state):
	for num in range(len(state)):
		board.get_map()[num][int(state[num]) - 1] = 1
		

#Retrieves the numeric string associated with a board
#in order to make it easier to do the crossover
def get_numeric_string(state):
	pop = ''
	for row in range(5):
		for col in range(5):
			if(state.get_map()[row][col] == 1):
				pop += str(col + 1)
	#print(pop)
	return pop


#Part A of the algorithm
#Generates the intial states, 8 in this case
def generate_initial_states(numofstates):
	population = []
	for i in range(numofstates):
		state = Board(5)
		population.append(state)
	return population


#Part B
#Fitness function that determines the parents of the offsprings
#Creates a dictionary of the percentages that each state has a chance of being selected as a parent
#rounded to two decimal points
def fitness(population_fitness_scores,attacking_pairs):
    #check_percent = 0
    percentages = {}
    for state in population_fitness_scores:
        percentages.update({state:round((10 - population_fitness_scores.get(state))/attacking_pairs,2)})
        #check_percent += percentages.get(state)
    #print(percentages)
    #print(check_percent)
    return percentages
	

#Part C: Selection for reproduction
#Using the percentages for each state the program assigns it a letter value
#it randomly generates a number and if it falls under that range it selects that number like in the slides
#returns a list of the selected parents
def pair_selection(state_percentages):
    letters = ["A","B","C","D","E","F","G","H"]
    letter_percentages = {}
    letter_state = {}
    for letter,state in zip(letters,state_percentages):
        letter_percentages.update({letter: state_percentages.get(state)})
        letter_state.update({letter: state})
    pairs_selected = []
    for i in range(8):
        r = round(random.random(),2)
        #print(r)
        if r <=  letter_percentages.get("A"):
            pairs_selected.append("A")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B"):
            pairs_selected.append("B")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C"):
            pairs_selected.append("C")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C") +letter_percentages.get("D"):
            pairs_selected.append("D")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C") +letter_percentages.get("D") + letter_percentages.get("E"):
            pairs_selected.append("E")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C") +letter_percentages.get("D") + letter_percentages.get("E") + letter_percentages.get("F"):
            pairs_selected.append("F")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C") +letter_percentages.get("D") + letter_percentages.get("E") + letter_percentages.get("F") + letter_percentages.get("G"):
            pairs_selected.append("G")
        else:
            pairs_selected.append("H")
    #print(pairs_selected)

    states_selected = []
    for letter in pairs_selected:
        states_selected.append(letter_state.get(letter))
    #print(states_selected)
    return states_selected
        

            


#Part D: Crossover
#Splices the parents into the children by selecting a random index as the point to split at
#Creates the children from these parents and returns a list of children
def crossover(parents):
    random_index = random.randint(1,4)
    pairs = []
    for i in range(0, len(parents),2):
        pair = [parents[i],parents[i+1]]
        pairs.append(pair)
    #print("PAIRS",pairs)

    children = []
    for pair in pairs:
        child1 = pair[0][:random_index] + pair[1][random_index:]
        child2 = pair[1][:random_index] + pair[0][random_index:]
        children.append(child1)
        children.append(child2)
    #print(children)
    return children

#Part E
#Mutates the given chromosome by selecting a random index
#Once the random index is selected it is changed between the number 1 and 5 
#Once the string is changed we revert it back to a string and return the 
#new chromosome
def mutate(chromosome):
	#print("OG", chromosome)
	random_gene = random.randint(0,len(chromosome))
	for i in range(len(chromosome)):
		if i == random_gene:
			random_change = random.randint(1,5)
			modified = list(chromosome)
			modified[i] = random_change
			chromosome = ''
			for i in modified:
				chromosome += str(i)
	#print("mutated",chromosome)
	return chromosome


if __name__ == '__main__':
    start_time = time.perf_counter()
    solution = None

    
    #Creates the initial population
    initial_pop = generate_initial_states(8)

    while solution != 0:
        #Creates the numeric strings for each board
        numerics = []
        for gen in initial_pop:
            numerics.append(get_numeric_string(gen))
        #print(numerics)

        #Creates a relationship between the numeric string and board
        population_to_numerics = {}
        for string, state in zip(numerics,initial_pop):
            population_to_numerics.update({string: state})
        #print(population_to_numerics)

        #Creates a relation between the fitness score and numeric string
        #Also gathers the number of attacking pairs
        total_attacking_pairs = 0
        numeric_fitness = {}
        for string in numerics:
            numeric_fitness.update({string: population_to_numerics.get(string).get_fitness()})
            total_attacking_pairs += 10 - numeric_fitness.get(string)
        #print(numeric_fitness)
        #print(total_attacking_pairs)
        percentages_for_crossover = fitness(numeric_fitness,total_attacking_pairs)
        parents = pair_selection(percentages_for_crossover)
        #print(parents)
        children = crossover(parents)
        #print("CHILD",children)

        mutants = []
        for child in children:
            new_child = mutate(child)
            mutants.append(new_child)
        #print("Mutated children", mutants)

        for mutant in mutants:
            mutated_board = Board(5)
            reset_board(mutated_board)
            update_board(mutated_board, mutant)
            #mutated_board.show_map()
            solution = mutated_board.get_fitness()
            if solution == 0:
                mutated_board.show_map()
                print()
                break
    end_time = time.perf_counter()
    overall_time = end_time - start_time
    print("Running time:", overall_time, "ms")




