# Importing
import copy
import numpy as np

## User definitions
# Important: the negative number will be the gap
initial = np.array([[1, 2, 4], [3, 5, 6], [-1, 7, 0]])
#initial = np.array([[-1, 0, 1], [3, 4, 2], [6, 7, 5]])
final = np.array([[0, 1, 2], [3, 4, 5], [6, 7, -1]])

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
# Verify if elements are unique
for i in range(number_of_elements):
	element = initial[tuple(indexes_of_inputs[i,:])]
	if np.sum(initial == element) != 1 or np.sum(final == element) != 1:
		print "Elements must be unique and existent in both final and initial states\n(Element " + str(element) + " does not comply this)"
		exit()
# Verify if there is an only gap
if np.sum(initial < 0) != 1:
	print "There must be an only gap"	
	exit()

## State space search algorithm
# Initial conditions for search
border = []
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
	gap_position_array = np.where(state < 0)
	current_gap_index = np.ndarray(shape=(problem_dimension), dtype=int)
	for i in range(problem_dimension):
		current_gap_index[i] = gap_position_array[i][0]
	# Try to apply the actions to get new states
	for i in range(actions.shape[0]):
		desired_gap_index = current_gap_index + actions[i,:]
		for j in range(indexes_of_inputs.shape[0]):
			# Checks if action is valid
			if (desired_gap_index == indexes_of_inputs[j,:]).all():
				# Moves the gap
				state_buffer = np.copy(state)
				history_buffer = copy.deepcopy(history)
				change_element = state_buffer[tuple(desired_gap_index)]
				state_buffer[tuple(desired_gap_index)] = state_buffer[tuple(current_gap_index)]
				state_buffer[tuple(current_gap_index)] = change_element
				#Avoids identical states
				found_identical = False
				for k in range(len(border)):
					if (border[k][0] == state_buffer).all():
						found_identical = True
						break
				if not found_identical:
					# Insert the state to border
					history_buffer.append(actions[i,:])
					border.append((state_buffer, history_buffer))
					if len(history_buffer) > n_movement:
						n_movement = len(history_buffer)
						print "Moviments number: " + str(n_movement)
				break
	# Next state
	the_next = border.pop(0)
	state = the_next[0]
	history = the_next[1]
