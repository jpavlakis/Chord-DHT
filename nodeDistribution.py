from classes import Chord, Node, Utils
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

number_of_nodes = 64
number_of_data = 20000
safety_parameter = 0
m = 6

# Creating Chord
print('Creating Chord ...')
myChord = Chord.Chord(m, safety_parameter)

# List of all nodes created
nodes = []

# Creating nodes
print('Creating and inserting nodes to Chord ...')
for i in range(number_of_nodes):
    newNode = Node.Node(Utils.generateIp(nodes))
    nodes.append(newNode)
    myChord.nodeJoin(newNode)

# Inserting data
print('Inserting data ...')
df = pd.read_csv('data/data.csv', low_memory=False)
for index, row in tqdm(df.iterrows(), total=number_of_data):
    # startingNode = random.randint(0,number_of_nodes-1)
    starting_node = 0
    myChord.insertData(row, starting_node)
    if index == number_of_data:
        break

data_count = []

for node in myChord.nodes:
    data_count.append(len(node.data))
print(data_count)

fig, ax = plt.subplots()
fig.set_size_inches(9, 6)
ax.scatter(range(0, number_of_nodes), data_count)

ax.set_xlabel('Nodes')
ax.set_ylabel('Num of Data Entries')
ax.set_title('Data Entries per Node')
plt.ylim(0, max(data_count)+10)
plt.style.use('seaborn')
plt.tight_layout()
plt.show()