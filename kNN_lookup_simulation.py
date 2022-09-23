#TODO: Change code in order to make kNN queries

import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt
from classes import Chord, Node, Utils


#General Configuration
redundancy_param = 0

number_of_data = 1_000
number_of_samples_per_nodes = 100

min_m, max_m = 4, 8
min_k, max_k = 2, 6

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
        myChord.nodeJoin(newNode)

    # Inserting data
    df = pd.read_csv('data/data.csv', low_memory=False)
    for idx, row in df.iterrows():
        starting_node = 0
        myChord.insertData(row, starting_node)
        if idx == number_of_data:
            break
        Utils.print_progress_bar(iteration=idx+1, total=number_of_data, prefix="Inserting data: ", suffix="Complete", length=75)

    # Create empty datetime object to store total time
    # consumed in queries for the certain m iteration
    total_time = datetime.datetime.now() - datetime.datetime.now()
    
    for idx, row in df.iterrows():
        if idx == number_of_samples_per_nodes:
            break
        
        #TODO: Add for loop to iterate k
        #TODO: Find a way to plot the data
        startingNode = random.randint(0, number_of_nodes-1)
        hash_key = Utils.generateHash(row['AttainmentId'], myChord.m)
        start = datetime.datetime.now()
        result = myChord.kNNQuery(startingNode, hash_key, k)
        end = datetime.datetime.now()
        total_time = total_time +  end - start
    
    avg_total_time = total_time / number_of_samples_per_nodes
    avg_times.append(avg_total_time.microseconds)
    print(f'Avarage Time: {avg_total_time.microseconds}')
    print('\n\n')


# Creating Plot
plt.style.use('seaborn')
fig, ax = plt.subplots()
fig.set_size_inches(8.5, 5)

ax.plot(range(min_m,max_m), avg_times, color='r', label='Avarage Lookup Time')

ax.set_xlabel('m')
ax.set_ylabel('Avarage lookup time (μs)')
ax.set_title('Avarage lookup time per m value')
plt.legend()
plt.tight_layout()
plt.show()