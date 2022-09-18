import matplotlib.pyplot as plt
import pandas as pd
from classes import Chord, Node, Utils


#General Configuration
number_of_nodes = 50
number_of_fails = 45

number_of_data = 30_000
number_of_lookup_data = 1_000

safety_parameter_max = 5
m = Utils.closest_power2_exponent(number_of_nodes)

fail_rate = [] # used for plotting

for safety_parameter in range(safety_parameter_max):

    print(f'Proccess Started for safety parameter: {safety_parameter}')

    # List of all nodes created
    nodes = []

    fail_rate.append(None)
    fail_rate[safety_parameter] = []

    # Creating Chord
    print('Creating Chord ...')
    myChord = Chord.Chord(m, safety_parameter)


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

            if idx==number_of_lookup_data:
                break

            result, _ = myChord.exactMatch(row['AttainmentId'])

            if(result):
                successfull_lookups+=1

        current_fail_rate = round(((number_of_lookup_data-successfull_lookups)/number_of_lookup_data)*100,2)
        fail_rate[safety_parameter].append(current_fail_rate)
        print(f'Fail percentage of lookups: {current_fail_rate}%')
    
    
    print(f'Proccess finished for safety parameter: {safety_parameter}\n\n')


# Creating Plots
plt.style.use('seaborn')
fig, ax = plt.subplots()
fig.set_size_inches(8.5, 5)

colors = ['r', 'b', 'g','y','m','k','c']

for safety_parameter in range(safety_parameter_max):
    ax.plot(range(number_of_fails), fail_rate[safety_parameter], color=colors[safety_parameter], label=f'Safety Parameter: {safety_parameter}')

ax.set_xlabel('Num of Failed Nodes')
ax.set_ylabel('Failure %')
ax.set_title('Failure % per Failed Nodes')
plt.legend()
plt.tight_layout()
plt.show()