from classes import Chord, Node, Utils
import pandas as pd


def print_menu():
    print("=============== Chord-DHT MENU ===============")
    print()
    print("         1. Insert Node")
    print("         2. Delete Node")
    print("         3. Insert Key")
    print("         4. Delete Key")
    print("         5. Update Record")
    print("         6. Exact Match")
    print("         7. Range Query")
    print("         8. K-NN Query")
    print("         9. Print current state of Chord")
    print("\nPress x to exit.")

def print_current_state(chord):
    template = "{0:25} {1:25} {2:30} {3:25}"
    table_length = 93
    print()
    print('-' * table_length)
    print(template.format("Node Id", "Predecessor", "Successors", "Total data"))
    print('-' * table_length)

    for node in chord.nodes:
        print(template.format(str(node.getId()), str(node.getPredecessor().getId()), ', '.join([str(succId) for succId in node.getSuccessorsId()]), str(len(node.getData()))))
    print('-' * table_length)

def print_query_results(data):
    template = "{0:25} {1:14}"
    table_length = 39
    print('-' * table_length)
    print(template.format("Entry ID", "Data Hash Key"))
    print('-' * table_length)

    for data_entry in data:
        if isinstance(data_entry, list):
            for entry in data_entry:
                print(template.format(str(entry['AttainmentId']), str(entry['hash_key'])))
        elif isinstance(data_entry, dict):
            print(template.format(str(data_entry['AttainmentId']), str(data_entry['hash_key'])))
    print('-' * table_length)


def main():
    # === Generating Chord

    # General Configuration
    number_of_nodes = 25
    number_of_data = 100
    m = Utils.closest_power2_exponent(number_of_nodes)
    redundancy_param = 0

    myChord = Chord.Chord(m, redundancy_param)

    # Create nodes
    for i in range(number_of_nodes):
        Utils.print_progress_bar(iteration=i+1, total=number_of_nodes, prefix="Creating Chord: ", suffix="Complete", length=75)
        newNode = Node.Node(Utils.generateIp(myChord.nodes))
        myChord.nodeJoin(newNode)

    print_current_state(myChord)


    input("\n\nPress any key to continue for data insertion...\n")

    # === Inserting Data

    df = pd.read_csv('data/data.csv', low_memory=False)
    for idx, row in df.iterrows():
        starting_node = 0
        myChord.insertData(row, starting_node)
        if idx == number_of_data:
            break
        Utils.print_progress_bar(iteration=idx+1, total=number_of_data, prefix="Inserting data: ", suffix="Complete", length=75)

    print_current_state(myChord)

    input("\n\nPress any key to continue to the menu...\n")

    # ================ MAIN ================

    print_menu()
    choice = input(">> ")

    while choice != 'x':
        if choice == '1':
            print('\nNode Insertion initiated\n')
            if len(myChord.nodes) >= 2**m:
                print(f"\nMaximum number of nodes ({2**m}) for given m ({m}) is reached. No more nodes can be added to the Chord network.")
            else:
                newNode = Node.Node(Utils.generateIp(myChord.nodes))
                print(f"A new node has been generated with IP: {newNode.getIpAddress()}")
                myChord.nodeJoin(newNode)
                print(f"New node ID: {newNode.getId()}")
                print("New Chord structure:")
                print_current_state(myChord)


        elif choice == '2':
            print('\nNode Deletion initiated')
            nodeId_to_delete = input('\nGive the ID of the node you want to delete: ')
            myChord.nodeLeave(nodeId_to_delete)
            print("New Chord structure:")
            print_current_state(myChord)

        elif choice == '3':
            print('\nKey Insertion initiated\n')
            key_to_insert = input("Give new key to insert: ")
            print("Inserting key ...")
            myChord.insertKey(key_to_insert, 0)

        elif choice == '4':
            print('\nKey Deletion initiated\n')
            print('Examples of existing keys:')
            for idx, row in df.iterrows():
                starting_node = 0
                print(row['AttainmentId'])
                if idx==2:
                    break
            
            key_to_delete = input("\nGive key to delete: ")
            myChord.deleteKey(key_to_delete)

        elif choice == '5':
            print('\nNode Update initiated\n')
            print('Examples of existing keys:')
            for idx, row in df.iterrows():
                starting_node = 0
                print(row['AttainmentId'])
                if idx==2:
                    break
            update_key = input("\n\nGive the key of the record you want to update: ")
            myChord.updateRecord(update_key)
        
        elif choice == '6':
            print('\nExact Match Query initiated\n')
            print('Examples of existing keys:')
            for idx, row in df.iterrows():
                starting_node = 0
                print(row['AttainmentId'])
                if idx==2:
                    break
            
            search_key = input('\nGive the ID of the entry you want to search: ')
            result, nodeId = myChord.exactMatch(search_key)
            if nodeId != -1:
                print(f"\nKey {search_key} found in node {nodeId} with data:\n\n{result}")
            else:
                print(f'\nThere are no entries with ID {search_key} found.')
            
        elif choice == '7':
            print('\nRange Query initiated\n')
            starting_key = input("Give starting hash key: ")
            ending_key   = input("Give ending hash key:   ")
            
            returned_data = myChord.rangeQuery(myChord.nodes[0], int(starting_key), int(ending_key))
            print("\nResults:\n")
            print_query_results(returned_data)

        elif choice == '8':
            print('\nkNN Query initiated')
            reference_key = input("\nGive reference hash key: ")
            nearest_neighbors_num = input("Give number of Nearest Neighbors: ")
            
            nearest_neighbors = myChord.kNNQuery(myChord.nodes[0], int(reference_key), int(nearest_neighbors_num))
            if nearest_neighbors:
                print("\nResults:\n")
                print_query_results(nearest_neighbors)
            else:
                print("Please provide a smaller amount of NNs for the kNN query to work properly")

        elif choice == '9':
            print_current_state(myChord)

        else:
            pass

        input("\n\nPress any key to continue...\n\n")
        
        print_menu()
        choice = input(">> ")

if __name__=='__main__':
    main()
