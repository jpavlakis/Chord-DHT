from classes import Chord, Node, Utils
import pandas as pd
import matplotlib.pyplot as plt

number_of_nodes = 64
number_of_data = 20_000
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
df = pd.read_csv('data/data.csv', low_memory=False)
for idx, row in df.iterrows():
    # startingNode = random.randint(0,number_of_nodes-1)
    starting_node = 0
    myChord.insertData(row, starting_node)
    if idx == number_of_data:
        break
    Utils.print_progress_bar(iteration=idx+1, total=number_of_data, prefix="Inserting data: ", suffix="Complete", length=75, printEnd='\r')

# Creating Plot
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