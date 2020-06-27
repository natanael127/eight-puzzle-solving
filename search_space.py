# Importing
import copy
import numpy as np
import time
import bisect

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
initial = np.array([[0, 7, 6], [1, 3, 5], [4, 8, 2]])
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
# Build the element positions array
element_index_fin = np.ndarray(shape=(number_of_elements, problem_dimension), dtype=int)
for i in range(number_of_elements):
	element_index_fin[i,:] = find_index_of_unique_element(final, i)
# Verify if elements are unique and correct
for i in range(number_of_elements):
	if np.sum(initial == i) != 1 or np.sum(final == i) != 1:
		print "Elements must be unique (from 0 to " + str(number_of_elements) + ") and existent in both final and initial states"
		exit()

## State space search algorithm
# Initial conditions for search
border = []
visited = []
rank_list = []
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
				heuristic_rat = len(history_buffer)
				index_to_insert = len(border)
				if algorithm != 0:
					# Rank the state according distance of elements
					for k in range(number_of_elements):
						element_index_now = find_index_of_unique_element(state_buffer, k)
						heuristic_rat += np.sum(np.abs(element_index_now-element_index_fin[k]))
					index_to_insert = bisect.bisect(rank_list, heuristic_rat)
				# Insert the state to border and visited
				history_buffer.append(actions[i,:])
				border.insert(index_to_insert, (state_buffer, history_buffer))
				rank_list.insert(index_to_insert, heuristic_rat)
				visited.append(identifier)
	# Updates variables
	del rank_list[0]
	the_next = border.pop(0)
	state = the_next[0]
	history = the_next[1]
	if len(history) > n_movement:
		n_movement = len(history)
		print "Movements counter: " + str(n_movement) + " - Visited: " + str(len(visited))
#Prints the solution
print "Solution found in " + str(time.clock()-timestamp_start) + " seconds, visiting " + str(len(visited)) + " states (" + str(len(history)) + " actions):"
for i in range(len(history)):
	print history[i]
