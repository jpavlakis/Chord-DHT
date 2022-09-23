import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt
from classes import Chord, Node, Utils


#General Configuration
redundancy_param = 0

total_lookups = 100

min_m, max_m = 4, 8

avg_times = []

for m in range(min_m, max_m):
    

    print(f'Value of m: {m}')
    
    # List of all nodes created
    nodes = []

    # Creating Chord
    print('Creating Chord ...')
    myChord = Chord.Chord(m, redundancy_param)

    # The number of nodes fill 50% of the overall capacity
    number_of_nodes = 2**(m-1)

    print('Creating and inserting nodes to Chord ...')
    for i in range(number_of_nodes):
        Utils.print_progress_bar(iteration=i+1, total=number_of_nodes, prefix="Creating Chord: ", suffix="Complete", length=75)
        newNode = Node.Node(Utils.generateIp(myChord.nodes))
        nodes.append(newNode)

    # Creating the finger tables ones
    myChord.massiveNodesJoin(nodes)

    df = pd.read_csv('data/data.csv', low_memory=False)
    
    # Create empty datetime object to store total time
    # consumed in queries for the certain m iteration
    total_time = datetime.datetime.now() - datetime.datetime.now()

    for idx, row in df.iterrows():
        if idx == total_lookups:
            break

        startingNode = random.randint(0, number_of_nodes-1)
        start = datetime.datetime.now()
        result, _ = myChord.exactMatch(row['AttainmentId'], startingNode, add_sleep=True)
        end = datetime.datetime.now()
        total_time = total_time +  end - start
    
    avg_total_time = total_time / total_lookups
    avg_times.append(avg_total_time.microseconds)
    print(f'Avarage Time: {avg_total_time.microseconds}')
    print('\n\n')


# Creating Plot
plt.style.use('ggplot')
fig, ax = plt.subplots()
fig.set_size_inches(8.5, 5)

ax.plot(range(min_m,max_m), avg_times, color='tab:cyan')

ax.set_xlabel('m')
ax.set_ylabel('Avarage lookup time (μs)')
ax.set_title('Avarage lookup time per m value')
plt.legend()
plt.tight_layout()
plt.show()