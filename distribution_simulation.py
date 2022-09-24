from classes import Chord, Node, Utils
import pandas as pd
import matplotlib.pyplot as plt

number_of_nodes = 35
number_of_data = 20_000
redundancy_param = 0
m = Utils.closest_power2_exponent(number_of_nodes)

# Creating Chord
print('Creating Chord ...')
myChord = Chord.Chord(m, redundancy_param)

# Creating nodes
for i in range(number_of_nodes):
    Utils.print_progress_bar(iteration=i+1, total=number_of_nodes, prefix="Creating Chord: ", suffix="Complete", length=75)
    newNode = Node.Node(Utils.generateIp(myChord.getNodes()))
    myChord.nodeJoin(newNode)

# Inserting data
df = pd.read_csv('data/data.csv', low_memory=False)
for idx, row in df.iterrows():
    starting_nodeId = 0
    myChord.insertData(row, starting_nodeId)
    if idx == number_of_data:
        break
    Utils.print_progress_bar(iteration=idx+1, total=number_of_data, prefix="Inserting data: ", suffix="Complete", length=75)

# Creating Plot
data_count = [len(myChord.getNodes()[myChord.getIndexFromId(nodeId)].getData()) if nodeId in myChord.getIdList() else 0 for nodeId in range(0, 2**m - 1)]
print(data_count)

plt.style.use('ggplot')
fig, ax = plt.subplots()
fig.set_size_inches(9, 6)
ax.scatter(range(0, 2**m - 1), data_count)

ax.set_xlabel('Nodes')
ax.set_ylabel('Num of Data Entries')
ax.set_title('Data Entries per Node')

ylim_offset = 10 if max(data_count) < 1_000 else 100
plt.ylim(0, max(data_count) + ylim_offset)
plt.style.use('seaborn')
plt.tight_layout()
plt.show()
