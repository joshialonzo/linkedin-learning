def selection_sort(xs: list) -> None:
	for i in range(len(xs) - 1):
		# find the minimum value in the unsorted region
		min_index = i

		for j in range(i + 1, len(xs)):
			# update min_index if the value at j is lower than current minimum value
			if xs[j] < xs[min_index]:
				min_index = j

		# after finding the minimum value in the unsorted region, swap with the first unsorted value
		xs[i], xs[min_index] = xs[min_index], xs[i]


xs = [3, 2, 1, 5, 4]
print(xs)
selection_sort(xs)
print(xs)


print(all(xs[i] <= xs[i + 1] for i in range(len(xs) - 1)))
