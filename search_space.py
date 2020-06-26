# Importing
import copy
import numpy as np
import time

## Modular functions
# Function that returns the position of an unique element in array form
def find_index_of_unique_element(array_of_search, element):
	position_object = np.where(array_of_search == element)
	position_result = np.ndarray(shape=(array_of_search.ndim), dtype=int)
	for i in range(array_of_search.ndim):
		position_result[i] = position_object[i][0]
	return position_result

### Script
## User definitions
# Important: the zero will be the gap
# Numbers must be from 0 to n_elements-1
initial = np.array([[3, 7, 5], [1, 0, 6], [2, 4, 8]])
final = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
algorithm = 1

## Initial check
# Verify if dimensions are equal
if initial.ndim != final.ndim:
	print "Initial and final states must have the same dimensions"
	exit()
else:
	# Assignment for recurrent call
	problem_dimension = initial.ndim
# Verify if shape is the same
for i in range(problem_dimension):
	if initial.shape[i] != final.shape[i]:
		print "Initial and final states must have the same shape"
		exit()
# Build the element indexes array
number_of_elements = 1
for i in range(problem_dimension):
	number_of_elements *= initial.shape[i]
indexes_of_inputs = np.ndarray(shape=(number_of_elements, problem_dimension), dtype=int)
for i in range(number_of_elements):
	index_ref = i
	for j in range(problem_dimension):
		indexes_of_inputs[i, j] = index_ref % initial.shape[j]
		index_ref = np.floor(index_ref/ initial.shape[j])
# Verify if elements are unique and correct
for i in range(number_of_elements):
	if np.sum(initial == i) != 1 or np.sum(final == i) != 1:
		print "Elements must be unique (from 0 to " + str(number_of_elements) + ") and existent in both final and initial states"
		exit()

## State space search algorithm
# Initial conditions for search
border = []
visited = []
state = initial
history = []
# Build the actions array
actions = np.ndarray(shape=(2*problem_dimension, problem_dimension), dtype=int)
actions.fill(0)
for i in range(2*problem_dimension):
	if i % 2 == 0:
		actions[i,int(np.floor(i/2))] = 1
	else:
		actions[i,int(np.floor(i/2))] = -1
# Search loop
timestamp_start = time.clock()
n_movement = 0
while not (state == final).all():
	# Find the gap
	current_gap_index = find_index_of_unique_element(state,0)
	# Try to apply the actions to get new states
	for i in range(actions.shape[0]):
		desired_gap_index = current_gap_index + actions[i,:]
		valid_index = True;
		# Checks if action is valid
		for j in range(problem_dimension):
			if (desired_gap_index[j] < 0 or desired_gap_index[j] >= initial.shape[j]):
				valid_index = False
				break
		if valid_index:
			# Moves the gap
			state_buffer = np.copy(state)
			history_buffer = copy.deepcopy(history)
			change_element = state_buffer[tuple(desired_gap_index)]
			state_buffer[tuple(desired_gap_index)] = state_buffer[tuple(current_gap_index)]
			state_buffer[tuple(current_gap_index)] = change_element
			#Calculates id
			identifier = 0
			for k in range(number_of_elements):
				identifier = identifier*number_of_elements + state_buffer[tuple(indexes_of_inputs[k,:])]
			#Avoids identical states
			found_identical = False
			for k in range(len(visited)):
				if visited[k] == identifier:
					found_identical = True
					break
			if not found_identical:
				rank_sum = len(history_buffer)
				if algorithm != 0:
					# Rank the state according distance of elements
					for k in range(number_of_elements):
						element_index_now = find_index_of_unique_element(state_buffer, k)
						element_index_fin = find_index_of_unique_element(final, k) #TODO: look-up table
						rank_sum += np.sum(np.abs(element_index_now-element_index_fin))
				# Insert the state to border and visited
				history_buffer.append(actions[i,:])
				border.append((state_buffer, history_buffer, rank_sum))
				visited.append(identifier)
	# Next state
	if algorithm == 0:
		# Pops from a queue
		the_next = border.pop(0)
	else:
		# Initializes with worst rank
		the_best_rank = 0
		for i in range(problem_dimension):
			the_best_rank += 2*(initial.shape[i] - 1)
		the_best_rank = the_best_rank * number_of_elements + 1
		# Finds the best
		for i in range(len(border)):
			if the_best_rank > border[i][2]:
				the_best_rank = border[i][2]
				the_best_index = i
		the_next = border.pop(the_best_index)
	#Updates variables
	state = the_next[0]
	history = the_next[1]
	if len(history) > n_movement:
		n_movement = len(history)
		print "Movements counter: " + str(n_movement) + " - Visited: " + str(len(visited))
#Prints the solution
print "Solution found in " + str(time.clock()-timestamp_start) + " seconds (" + str(len(history)) + " steps):"
for i in range(len(history)):
	print history[i]
