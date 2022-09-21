from classes import Chord, Node, Utils
import pandas as pd


def print_menu():

    print("========== Chord-DHT MENU ==========")
    print("1. Insert Node")
    print("2. Delete Node")
    print("3. Update Node")
    print("4. Exact Match")
    print("5. Range Query")
    print("6. K-NN Query")
    print("7. Insert Key")
    print("8. Delete Key")
    print("9. Print current state of Chord")
    print("Press x to exit.")

# === Generating Chord

# General Configuration
number_of_nodes = 25
number_of_data = 100
m = Utils.closest_power2_exponent(number_of_nodes)
redundancy_param = 0

myChord = Chord.Chord(m, redundancy_param)

# Create nodes
for i in range(number_of_nodes):
    newNode = Node.Node(Utils.generateIp(myChord.nodes))
    myChord.nodeJoin(newNode)

for node in myChord.nodes:
        print(f"NodeID: {node.getId()} \tPredecessor: {node.getPredecessor().getId()} \t Successors: {node.getSuccessorsId()}")


input("\n\nPress any key to continue for data insertion...")

# === Inserting Data

df = pd.read_csv('data/data.csv', low_memory=False)
for idx, row in df.iterrows():
    starting_node = 0
    myChord.insertData(row, starting_node)
    if idx == number_of_data:
        break
    Utils.print_progress_bar(iteration=idx+1, total=number_of_data, prefix="Inserting data: ", suffix="Complete", length=75)

for node in myChord.nodes:
        print(f"NodeID: {node.getId()} \tPredecessor: {node.getPredecessor().getId()} \t Successors: {node.getSuccessorsId()} \t Data count: {len(node.getData())}")

input("\n\nPress any key to continue to the menu...\n")

# ================ MAIN ================

print_menu()
choice = input(">> ")

while choice!='x':
    if int(choice)==1:
        if len(myChord.nodes) >= 2**m:
            print("Maximum number of nodes for given m is reached. No more nodes can be added to the Chord.")
        else:
            newNode = Node.Node(Utils.generateIp(myChord.nodes))
            print(f"A new node has been generated with IP: {newNode.ipAddress}")
            print("Inserting Node...")
            print("Updating finger tables...")
            myChord.nodeJoin(newNode)
            print(f"New node id: {newNode.id}")
            print("New chord structure:")
            for node in myChord.nodes:
                print(f"NodeID: {node.getId()} \tPredecessor: {node.getPredecessor().getId()} \t Successors: {node.getSuccessorsId()} \t Data count: {len(node.data)}")


    elif int(choice)==2:
        deleted_key = input('\nGive the id of the node you want to delete: ')
        print('Deleting Node ...')
        myChord.nodeLeave(deleted_key)
        print("New chord structure:")
        for node in myChord.nodes:
            print(f"NodeID: {node.getId()} \tPredecessor: {node.getPredecessor().getId()} \t Successors: {node.getSuccessorsId()} \t Data count: {len(node.data)}")


    elif int(choice)==3:
        print('\nUpdating node ...')
        print('Examples of existing keys:')
        df = pd.read_csv('data/data.csv', low_memory=False)
        for idx, row in df.iterrows():
            starting_node = 0
            print(row['AttainmentId'])
            if idx==2:
                break
        update_key = input("\n\nGive the key of the record you want to update: ")
        myChord.updateRecord(update_key)


    elif int(choice)==4:
        print('\nExact match ...')
        print('Examples of existing keys:')
        df = pd.read_csv('data/data.csv', low_memory=False)
        for idx, row in df.iterrows():
            starting_node = 0
            print(row['AttainmentId'])
            if idx==2:
                break
        search_key = input('\nGive the id of the entry you want to search: ')
        result, nodeId = myChord.exactMatch(search_key)
        if nodeId != -1:
            print(f"\nKey {search_key} found in node {nodeId} with data:\n\n{result}")
        else:
            print(f'\nThere are no entries with id {search_key} found.')

    elif int(choice)==5:

        print('Range Query ...')
        starting_key = input("Give starting key: ")
        ending_key = input("Give ending key: ")
        returned_data = myChord.rangeQuery(myChord.nodes[0], int(starting_key), int(ending_key))
        print("Results:")
        for node in returned_data:
            print(f"Data id after hashing: {node['hash_key']}  Original key before hashing: {node['AttainmentId']}")
    
    elif int(choice)==6:

        print('K-NN Query ...')
        reference_key = input("\nGive reference key: ")
        nearest_neighbors_num = input("Give nearest neighbors num: ")
        nearest_neighbors = myChord.kNNQuery(myChord.nodes[0], int(reference_key), int(nearest_neighbors_num))
        print("\n\nResults: ")
        if nearest_neighbors:
            for node in nearest_neighbors:
                print(f"Data id after hashing: {node['hash_key']}  Original key before hashing: {node['AttainmentId']}")
        else:
            print("Please provide a smaller amount of NNs for the K-NN query to work properly")
        
    elif int(choice)==7:
        key_to_be_added = input("Give new key to add: ")
        print("Inserting key ...")
        myChord.insertKey(key_to_be_added, 0)

        
    elif int(choice)==8:
        key_to_be_deleted = input("Give key to delete: ")
        print("Deleting key ...")
        myChord.deleteKey(key_to_be_deleted)


    elif int(choice)==9:
        for node in myChord.nodes:
            print(f"NodeID: {node.getId()} \tPredecessor: {node.getPredecessor().getId()} \t Successors: {node.getSuccessorsId()} \t Data count: {len(node.data)}")

    else:
        pass

    input("\n\nPress any key to continue...\n\n")
    
    print_menu()
    choice = input(">> ")

