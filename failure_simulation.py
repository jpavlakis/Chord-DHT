import matplotlib.pyplot as plt
import pandas as pd
from classes import Chord, Node, Utils


#General Configuration
number_of_nodes = 50
number_of_fails = 45

number_of_data = 5_000
number_of_lookup_data = 1_000

redundancy_param_max = 5
m = Utils.closest_power2_exponent(number_of_nodes)

fail_rate = [] # used for plotting

for redundancy_param in range(redundancy_param_max):

    print(f'Proccess Started for redundancy parameter: {redundancy_param}')

    # List of all nodes created
    nodes = []

    fail_rate.append(None)
    fail_rate[redundancy_param] = []

    # Creating Chord
    print('Creating Chord ...')
    myChord = Chord.Chord(m, redundancy_param)


    # Creating nodes
    print('Creating and inserting nodes to Chord ...')
    for i in range(number_of_nodes):
        newNode = Node.Node(Utils.generateIp(nodes))
        nodes.append(newNode)
        myChord.nodeJoin(newNode)


    # Inserting data
    df = pd.read_csv('data/data.csv', low_memory=False)
    for idx, row in df.iterrows():
        starting_node = 0
        myChord.insertData(row, starting_node)
        if idx == number_of_data:
            break
        Utils.print_progress_bar(iteration=idx+1, total=number_of_data, prefix="Inserting data: ", suffix="Complete", length=75, printEnd='\r')


    for fail_number in range(number_of_fails):

        # Node failure 
        nodes[fail_number].hasFailed = True
        successfull_lookups = 0
        for idx, row in df.iterrows():

            if idx == number_of_lookup_data:
                break

            result, nodeId = myChord.exactMatch(row['AttainmentId'])

            if(result):
                successfull_lookups+=1

        current_fail_rate = round(((number_of_lookup_data-successfull_lookups)/number_of_lookup_data)*100, 2)
        failed_nodes_percentage = round((fail_number + 1) / number_of_nodes * 100, 2)
        fail_rate[redundancy_param].append(current_fail_rate)
        print(f'\rNumber of failed nodes: {fail_number+1} out of {number_of_nodes} ({failed_nodes_percentage})% \t Fail percentage of lookups: {current_fail_rate}%', end='\r')
    else:
        print()
    
    
    print(f'Proccess finished for redundancy parameter: {redundancy_param}\n\n')


# Creating Plots
plt.style.use('seaborn')
fig, ax = plt.subplots()
# fig.set_size_inches(8.5, 5)

colors = ['tab:red', 'tab:blue', 'tab:green','tab:orange','tab:cyan','tab:gray', 'tab:purple']

for redundancy_param in range(redundancy_param_max):
    ax.plot(range(1, number_of_fails+1), fail_rate[redundancy_param], color=colors[redundancy_param], label=f'Redundancy Parameter: {redundancy_param}')

ax.set_xlabel('Num of Failed Nodes')
ax.set_ylabel('Lookup Failure %')
ax.set_title('Lookup Failure % per Failed Nodes')
plt.ylim(0, 100)
plt.xlim(1, number_of_fails)
plt.legend()
plt.tight_layout()
plt.show()