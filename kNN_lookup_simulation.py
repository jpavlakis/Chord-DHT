import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt
from classes import Chord, Node, Utils


#General Configuration
redundancy_param = 0
number_of_data = 1_000
total_lookups = 100
min_m, max_m = 4, 8
min_k, max_k = 2, 12
avg_times = []

for avg_times_idx, k in enumerate(range(min_k, max_k, 2)):

    print(f'\n\nProccess Started for k: {k}')

    avg_times.append(None)
    avg_times[avg_times_idx] = []

    for m in range(min_m, max_m):

        print(f'Value of m: {m}')

        # Creating Chord
        myChord = Chord.Chord(m, redundancy_param)

        # The number of nodes fill 50% of the overall capacity
        number_of_nodes = 2**(m-1)

        for i in range(number_of_nodes):
            newNode = Node.Node(Utils.generateIp(myChord.getNodes()))
            myChord.nodeJoin(newNode)

        # Inserting data
        df = pd.read_csv('data/data.csv', low_memory=False)
        for idx, row in df.iterrows():
            starting_node = 0
            myChord.insertData(row, starting_node)
            if idx == number_of_data:
                break

        # Create empty datetime object to store total time
        # consumed in queries for the certain m iteration
        total_time = datetime.datetime.now() - datetime.datetime.now()
        
        for _ in range(total_lookups):

            startingNode = random.choice(myChord.getNodes())
            hash_key = Utils.generateHash(row['AttainmentId'], myChord.m)
            start = datetime.datetime.now()
            result = myChord.kNNQuery(startingNode, hash_key, k, add_sleep=True)
            end = datetime.datetime.now()
            total_time = total_time +  end - start
        
        avg_total_time = total_time / total_lookups
        avg_times[avg_times_idx].append(avg_total_time.microseconds)
        print(f'Avarage Lookup Time: {avg_total_time.microseconds} μs')


# Creating Plot
plt.style.use('seaborn')
fig, ax = plt.subplots()
fig.set_size_inches(8.5, 5)

colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:cyan', 'tab:purple', 'tab:gray']

for avg_times_idx, k in enumerate(range(min_k, max_k, 2)):
    ax.plot(range(min_m, max_m), avg_times[avg_times_idx], color=colors[avg_times_idx], label=f'k: {k}')

ax.set_xlabel('m')
ax.set_ylabel('Avarage lookup time (μs)')
ax.set_title('Avarage k-NN Query lookup time per m value')
plt.legend()
plt.tight_layout()
plt.show()
