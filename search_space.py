# Importing
import copy
import numpy as np

## User definitions
# Important: the zero will be the gap
# Numbers must be from 0 to n_elements-1
initial = np.array([[1, 2, 4], [3, 5, 6], [8, 7, 0]])
final = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

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
n_movement = 0
while not (state == final).all():
	# Find the gap
	gap_position_array = np.where(state == 0)
	current_gap_index = np.ndarray(shape=(problem_dimension), dtype=int)
	for i in range(problem_dimension):
		current_gap_index[i] = gap_position_array[i][0]
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
				# Insert the state to border and visited
				history_buffer.append(actions[i,:])
				border.append((state_buffer, history_buffer))
				visited.append(identifier)
	# Next state
	the_next = border.pop(0)
	state = the_next[0]
	history = the_next[1]
	if len(history) > n_movement:
		n_movement = len(history)
		print "Movements counter: " + str(n_movement) + " - Queue size: " + str(len(border))
#Prints the solution
print "Solution:"
for i in range(len(history)):
	print history[i]
