import math
import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt
from classes import Chord,Node,Utils


#General Configuration
safety_parameter = 0

number_of_samples_per_nodes = 40

min_m = 4
max_m = 8

avg_times = []

for m in range(min_m, max_m):
    
    print(f'Value of m: {m}')

    # List of all nodes created
    nodes = []

    # Creating Chord
    print('Creating Chord ...')
    myChord = Chord.Chord(m, safety_parameter)

    # The number of nodes fill 50% of the overall capacity
    number_of_nodes = int(math.ceil(2**(m-1)))

    print('Creating and insering nodes to Chord ...')
    for i in range(number_of_nodes):
        Utils.print_progress_bar(iteration=i+1, total=number_of_nodes, prefix="Creating Chord: ", suffix="Complete", length=75, printEnd='\r')
        newNode = Node.Node(Utils.generateIp(nodes))
        nodes.append(newNode)

    # Creating the finger tables ones
    myChord.massiveNodesJoin(nodes)

    df = pd.read_csv('data/data.csv', low_memory=False)
    
    total_time = datetime.datetime.now() - datetime.datetime.now()

    for index, row in df.iterrows():
        if index==number_of_samples_per_nodes:
            break

        starting_node = random.randint(0,number_of_nodes-1)
        start = datetime.datetime.now()
        result, _ = myChord.exactMatch(row['AttainmentId'], starting_node, True)
        end = datetime.datetime.now()
        total_time = total_time +  end - start
        #print(end - start)
    
    avg_total_time = total_time/number_of_samples_per_nodes
    avg_times.append(avg_total_time.microseconds)
    print(f'Avarage Time: {avg_total_time.microseconds}')
    print('\n\n')



plt.style.use('seaborn')
fig, ax = plt.subplots()
fig.set_size_inches(8.5, 5)

ax.plot(range(min_m,max_m), avg_times, color='r', label='Avarage Lookup Time')

ax.set_xlabel('m')
ax.set_ylabel('Avarage lookup time (ms)')
ax.set_title('Avarage lookup time per m value')
plt.legend()
plt.tight_layout()
plt.show()