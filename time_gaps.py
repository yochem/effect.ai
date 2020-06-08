"""
This is where the magic happens.
"""
import caption
from asr import ASR

data = ASR('asr/sample01.asrOutput.json').groups()
print(data)
# storage lists
result = []
store = []
threshold = 1.5 # treshold time
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

# Visualize results
for i in range(0, len(result)):
	print(result[i])
	print('                ')
