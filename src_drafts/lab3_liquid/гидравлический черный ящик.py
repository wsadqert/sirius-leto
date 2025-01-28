# Communicating Vessels Simulation
# This script simulates the behavior of communicating vessels based on the volume of liquid poured into the first vessel.

# Number of vessels
num_vessels = 5

# Areas of the vessels
areas = [1.0, 2.0, 5.0, 3.0, 4.0]

# Heights of the connecting tubes between vessels
tube_heights = [
	2.0,
	5.0,
	8.0,
	3.0,
	10000000000.0,
]


def calculate_volume(v, index):
	"""
	Calculate the total volume of liquid in the vessels up to the given index.

	Parameters:
	v (float): The volume of liquid poured into the first vessel.
	index (int): The index of the last vessel to consider.

	Returns:
	float: The total volume of liquid in the vessels up to the specified index.
	"""
	heights = [0] * num_vessels + [0]

	# Determine the height of liquid in each vessel
	for i in range(index, -1, -1):
		heights[i] = max(heights[i + 1], tube_heights[i])

	total_volume = 0
	for i in range(index + 1):
		total_volume += areas[i] * heights[i]

	return total_volume


def distribute_volume(v, index):
	"""
	Distribute the given volume of liquid among the vessels starting from the specified index.

	Parameters:
	v (float): The volume of liquid to distribute.
	index (int): The index of the vessel to start distribution from.

	Returns:
	float: The height of liquid in the first vessel after distribution.
	"""
	heights = [0] * num_vessels + [0]

	# Determine the height of liquid in each vessel
	for i in range(index, -1, -1):
		heights[i] = max(heights[i + 1], tube_heights[i])

	total_volume = 0
	for i in range(index + 1):
		total_volume += areas[i] * heights[i]

	v -= total_volume
	index += 1
	area_sum = 0
	initial_index = index

	while index != -1:
		if v == 0:
			break
		area_sum += areas[index]
		height_increase = v / area_sum

		# Prevent overflow to the previous vessel
		if index != 0 and heights[index] + height_increase > heights[index - 1]:
			height_increase = heights[index - 1] - heights[index]

		v -= height_increase * area_sum

		# Update the heights of the vessels
		for i in range(index, initial_index + 1):
			heights[i] += height_increase

		index -= 1

	return heights[0]


def calculate_height(v):
	"""
	Calculate the height of liquid in the first vessel based on the volume poured in.

	Parameters:
	v (float): The volume of liquid poured into the first vessel.
	"""
	# If the volume is less than the maximum capacity of the first vessel
	if v <= tube_heights[0] * areas[0]:
		print((v / areas[0]))
		return

	index = 0
	while index < num_vessels:
		if calculate_volume(v, index) > v:
			break
		index += 1
	index -= 1

	print(distribute_volume(v, index))


volume_input = float(input())
calculate_height(volume_input)
