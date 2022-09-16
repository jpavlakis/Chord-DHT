from classes import Chord, Node, Utils
import pandas as pd


# === Generating Chord

# General Configuration
number_of_nodes = 20
number_of_data = 100
m = 6
safety_parameter = 0

myChord = Chord.Chord(m, safety_parameter)

# All the nodes that have been created
nodes = []

# Create nodes
for i in range(number_of_nodes):
    newNode = Node.Node(Utils.generateIp(nodes))
    nodes.append(newNode)
    myChord.nodeJoin(newNode)

for node in myChord.nodes:
        print(f"NodeID: {node.id} \tPredecessor: {node.predecessor.id} \t Successors: {node.getSuccessorsId()}")


input("\n\nPress any key to continue for data insertion...")

# === Inserting Data

df = pd.read_csv('data/data.csv', low_memory=False)
for idx, row in df.iterrows():
    starting_node = 0
    myChord.insertData(row, starting_node)
    if idx == number_of_data:
        break
    Utils.print_progress_bar(iteration=idx+1, total=number_of_data, prefix="Inserting data: ", suffix="Complete", length=75, printEnd='\r')

for node in myChord.nodes:
        print(f"NodeID: {node.id} \tPredecessor: {node.predecessor.id} \t Successors: {node.getSuccessorsId()} \t Data count: {len(node.data)}")

input("\n\nPress any key to continue to the menu...\n")

# ================ MAIN ================

print("========== MENU ==========")
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
choice = input(">> ")

while choice!='x':
    if int(choice)==1:

        newNode = Node.Node(Utils.generateIp(nodes))
        print(f"A new node has been generated with ip: {newNode.ipAddress}")
        print("Inserting Node...")
        print("Updating finger tables...")
        myChord.nodeJoin(newNode)
        print(f"New node id: {newNode.id}")
        print("New chord structure:")
        for node in myChord.nodes:
            print(f"NodeID: {node.id} \tPredecessor: {node.predecessor.id} \t Successors: {node.getSuccessorsId()} \t Data count: {len(node.data)}")


    if int(choice)==2:

        deleted_key = input('Give the id of the node you want to delete: ')
        myChord.nodeLeave(deleted_key)
        print("New chord structure:")
        for node in myChord.nodes:
            print(f"NodeID: {node.id} \tPredecessor: {node.predecessor.id} \t Successors: {node.getSuccessorsId()} \t Data count: {len(node.data)}")


    if int(choice)==3:

        print('Examples of existing keys:')
        df = pd.read_csv('data/data.csv', low_memory=False)
        for idx, row in df.iterrows():
            starting_node = 0
            print(row['AttainmentId'])
            if idx==2:
                break
        update_key = input("Give the key of the record you want to update: ")
        myChord.updateRecord(update_key)


    if int(choice)==4:

        print('Examples of existing keys:')
        df = pd.read_csv('data/data.csv', low_memory=False)
        for idx, row in df.iterrows():
            starting_node = 0
            print(row['AttainmentId'])
            if idx==2:
                break
        search_key = input('Give the id of the entry you want to search: ')
        result, _ = myChord.exactMatch(search_key)
        if(result):
            print(result)
        else:
            print('Given id not found.')

    if int(choice)==5:

        print('Range Query Started.')
        starting_key = input("Give starting key: ")
        ending_key = input("Give ending key: ")
        returned_data = myChord.rangeQuery(myChord.nodes[0], int(starting_key), int(ending_key))
        print("Results:")
        for node in returned_data:
            print(f"Data id after hashing: {node['hash_key']}  Original key before hashing: {node['AttainmentId']}")
    
    if int(choice)==6:

        print('K-NN Query Started.')
        reference_key = input("Give reference key: ")
        nearest_neighbors_num = input("Give nearest neighbors num: ")
        nearest_neighbors = myChord.kNNQuery(myChord.nodes[0], int(reference_key), int(nearest_neighbors_num))
        print("Results: ")
        if nearest_neighbors:
            for node in nearest_neighbors:
                print(f"Data id after hashing: {node['hash_key']}  Original key before hashing: {node['AttainmentId']}")
        else:
            print("Please provide a smaller n for the K-NN query to work properly")
        
    if int(choice)==7:
        print("Inserting key ...")
        key_to_be_added = input("Give new key to add: ")
        myChord.insertKey(key_to_be_added, 0)
        result, nodeId = myChord.exactMatch(key_to_be_added)
        print(f"Results:\nKey added to node {nodeId} with data:\n{result}")

        
    if int(choice)==8:
        print("Deleting key ...")
        key_to_be_deleted = input("Give key to delete: ")
        myChord.deleteKey(key_to_be_deleted)


    if int(choice)==9:
        for node in myChord.nodes:
            print(f"NodeID: {node.id} \tPredecessor: {node.predecessor.id} \t Successors: {node.getSuccessorsId()} \t Data count: {len(node.data)}")


    input("Press any key to continue...\n\n")
    print("========== MENU ==========")
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
    choice = input(">> ")

