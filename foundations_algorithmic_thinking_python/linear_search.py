def linear_search(data, target):
	for index, item in enumerate(data):
		if item == target:
			return index


data = [4, 5, 2, 7, 1, 8]
target = 1

result = linear_search(data, target)

if result == -1:
	print("Item not found.")
else:
	print(f"Item found at position {result}")
