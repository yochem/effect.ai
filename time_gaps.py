import caption
from asr import ASR

data = ASR('asr/sample01.asrOutput.json').groups()
print(data)
# storage lists


def time_gaps(data, threshold):
	"""
	Iterates trough data, and compares time between every word, if difference is not to high append second word to same list,
	when the time diffenrece is to high, append second word to new list.

	Inputs:
	data: ASR data faile
	threshold: how much time between words for splitting thermal

	Output: Big list that contains smaller lists that are splitted from eachother at points where
	the time between two words was to big

	"""
	result = []
	store = []
	#store first word
	store.append(data[0])

	#splitter
	for i in range(0, len(data)-1):
		first = data[i].end
		second = data[i+1].start
		first = float(first)
		second = float(second)
		if second-first<threshold:
			store.append(data[i+1])
		else:
			result.append(store)
			store= []
			store.append(data[i+1])
	return result

# Visualize results
for i in range(0, len(result)):
	print(result[i])
	print('                ')
