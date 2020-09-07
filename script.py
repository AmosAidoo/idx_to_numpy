def idx_to_numpy(path):
	import numpy as np

	file  = open(path, "rb")

	# First two bytes are zeros
	magic_number = file.read(4)

	# Grab the datatype
	idx = 0
	dtype = [np.ubyte, np.byte, np.short, np.int, np.single, np.double]

	datatype = magic_number[2]
	if datatype == 0x08:
		idx = 0
	elif datatype == 0x09:
		idx = 1
	elif datatype == 0x0B:
		idx = 2
	elif datatype == 0x0C:
		idx = 3
	elif datatype == 0x0D:
		idx = 4
	else:
		idx = 5

	number_of_dimensions = magic_number[3]

	dimensions = []

	# Grab the sizes in each dimension
	for i in range(number_of_dimensions):
		dimensions.append(int.from_bytes(file.read(4), byteorder="big"))
	
	# Unroll dimensions 1 ... n-1
	unrolled_size = 1
	for i in range(1, number_of_dimensions):
		unrolled_size *= dimensions[i]
	
	# Initialize numpy array
	data = np.zeros([dimensions[0], unrolled_size], dtype=dtype[idx])

	# Read the data
	for i in range(dimensions[0]):
		data_item = list(file.read(unrolled_size))
		data[i] = data_item

	file.close()
	return data