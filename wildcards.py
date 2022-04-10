import re
import pickle


with open('bin/binary.pkl', "rb") as file:
    data = pickle.load(file)
    file.close()

print(data[0])
print(data[1])

for device in range(len(data[0])):
    if re.search('input_.+', data[0][device][1]):
        print(data[0][device][1])

    if re.search('output_.+', data[0][device][1]):
        print(data[0][device][1])

'''
for connections in range(len(data[1])):
    print(data[1][connections][1])
'''
