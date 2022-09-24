from classes import FingerTable
from classes import Utils
from random import randint

class Chord:
    def __init__(self, m, redundancy_param):
        self.m = m
        self.redundancy_param = redundancy_param
        self.chordSize = 1 << m # 2^m
        self.nodes = []

    def insertData(self, row, index):

        # Defining unique key
        key = Utils.generateHash(row['AttainmentId'], self.m)
        # Building our data structur
        data = row.to_dict()
        data['hash_key'] = key
        targetNode = self.nodes[index].findSuccesor(key)
        targetNode.data.append(data)

        # Failure prevention mechanism
        # Adding redundancy of keys to the successor of the node
        current_node = targetNode
        for i in range(self.redundancy_param):
            nextNode = current_node.fingerTable.successors[0]

            #if its the first time create it with append else override
            if len(nextNode.getBackupData()) < self.redundancy_param:
                nextNode.backupData.append(targetNode.getData().copy())
            else:
                nextNode.getBackupData()[i] = targetNode.getData().copy()
            current_node = nextNode

    def insertKey(self, data_key, index):

        # Create empty dict with the same structure as the rest of the data
        data = dict((key, None) for key, value in self.nodes[0].getData()[-1].items())

        data['AttainmentId'] = data_key
        data['hash_key'] = Utils.generateHash(data_key, self.m)
        
        targetNode = self.nodes[index].findSuccesor(data['hash_key'])

        for entry in targetNode.getData():
            if entry['AttainmentId'] == data_key:
                print(f'\nKey {data_key} has already been inserted in node {targetNode.getId()}.')
                return

        targetNode.data.append(data)
        
        # Failure prevention mechanism
        # Adding redundancy of keys to the first successor of the node
        currentNode = targetNode
        for i in range(self.redundancy_param):
            nextNode = currentNode.fingerTable.successors[0]

            #if its the first time create it with append else override
            if len(nextNode.getBackupData()) < self.redundancy_param:
                nextNode.backupData.append(targetNode.getData().copy())
            else:
                nextNode.getBackupData()[i] = targetNode.getData().copy()
            currentNode = nextNode
        
        print(f"\nKey {data_key} added to node {targetNode.getId()} with data:\n\n{data}")

    def deleteKey(self, data_key):
        
        result, nodeId = self.exactMatch(data_key)
        if nodeId == -1:
            print(f'\nKey {data_key} does not exist.')
            return
        
        targetNode = self.nodes[self.getIndexFromId(nodeId)]
        
        # Delete from target node
        targetNode.data.remove(result)

        # If data stored as backup, delete it
        if result in targetNode.fingerTable.successors[0].getBackupData():
            targetNode.fingerTable.successors[0].backupData.remove(result)
        
        print(f'\nKey {data_key} has been deleted from node {targetNode.getId()}')

    
    def updateRecord(self, key):
       
        hashed_key = Utils.generateHash(key, self.m)
        print(f'The hash of the given key is: {hashed_key}')

        # Select random node to begin search
        random_nodeId = randint(0, len(self.nodes))
        targetNode = self.nodes[random_nodeId].findSuccesor(hashed_key)

        if(not targetNode.hasFailed):
            for data_entry in targetNode.getData():
                if(data_entry['hash_key'] == hashed_key):
                    print(f'Data entry found in node {targetNode.getId()}\n\n')
                    valid_input = False
                    while(not valid_input):
                        column = input('Give the column you want to edit: ')
                        if column == "AttainmentId":
                            print(f'Column {column} can\'t be changed.\n\n')
                        elif(column in data_entry):
                            new_value = input('Give the new value: ')
                            data_entry[column] = new_value
                            # Update backup data if it exists in backup storage
                            for backup_data_entry in targetNode.fingerTable.successors[0].getBackupData():
                                if(backup_data_entry['hash_key'] == hashed_key):
                                    backup_data_entry[column] = new_value
                            return
                        else:
                            print(f'Column {column} doesn\'t exist.\n\n')
        else:
            # Integrating the failure prevention mechanism
            # Search in first successor in case the entry is in backup storage
            targetNode = targetNode.fingeTable.successors[0]
            for data_entry in targetNode.getBackupData():
                if(data_entry['hash_key'] == hashed_key):
                    print(f'Data entry found in node {targetNode.getId()} backup storage.\n\n')
                    valid_input = False
                    while(not valid_input):
                        column = input('Give the column you want to edit: ')
                        if column == "AttainmentId":
                            print(f'Column {column} can\'t be changed.\n\n')
                        elif(column in data_entry):
                            new_value = input('Give the new value: ')
                            data_entry[column] = new_value
                            return
                        else:
                            print(f'Column {column} doesn\'t exist.\n\n')


    def nodeJoin(self, node):
        # Create node ID for the given Chord
        node.setId(self.m)
        
        # Making sure that we don't have double ids
        while node.getId() in (chord_node.getId() for chord_node in self.nodes):
            node.id = (node.id + 1) % 2**self.m

        # Insert ordered in Node's list 
        self.nodes.append(node)
        self.nodes.sort(key=lambda x: x.getId())

        # Create Finger Table 
        node.setFingerTable(FingerTable.FingerTable(self, node))
        node.updatePredeccessorFingerTable(self)

        # Find nodes that need Finger Table update
        nodesToUpdate = []
        for chordNode in self.nodes:
            for pow in range(self.m):
                estimSuccID = chordNode.getId() + (2**pow)
                estimSuccID = estimSuccID % self.chordSize
                if estimSuccID <= node.getId() + self.chordSize and estimSuccID + self.chordSize > node.predecessor.getId():
                    nodesToUpdate.append(self.nodes.index(chordNode))
        
        nodesToUpdate = list(dict.fromkeys(nodesToUpdate)) #Remove duplicates
        try:
            nodesToUpdate.remove(self.nodes.index(node)) #Remove the Newly added node
        except ValueError:
            pass
        
        for index in nodesToUpdate:
            self.nodes[index].updatePredeccessorFingerTable(self)

        # Here we transfer the corresponding data to the new node    
        firstSuccessor = node.fingerTable.successors[0]
        data_to_be_removed = []
        for current_data in firstSuccessor.getData():
            if node.getId() >= current_data['hash_key'] :
                node.data.append(current_data)
                data_to_be_removed.append(current_data)

        # Removing the nodes
        for dataForRemoval in data_to_be_removed:
            firstSuccessor.data.remove(dataForRemoval)

    # Used when we only want to create the 
    # finger tables at the end when all the nodes
    # are inserted.
    def massiveNodesJoin(self, nodes):

        for idx, node in enumerate(nodes):
            Utils.print_progress_bar(iteration=idx+1, total=len(nodes), prefix="Massive node join: ", suffix="Complete", length=75)
            # Create node ID for the given Chord
            node.setId(self.m)
            
            # Making sure that we don't have double ids
            while node.getId() in (chord_node.getId() for chord_node in self.nodes):
                node.id = (node.id + 1) % 2**self.m

            # Insert ordered in Node's list 
            self.nodes.append(node)
            self.nodes.sort(key=lambda x: x.getId())

            # Create Finger Table 
            node.setFingerTable(FingerTable.FingerTable(self, node))

        # Find nodes that need Finger Table update
        for idx, chordNode in enumerate(self.nodes):
            Utils.print_progress_bar(iteration=idx+1, total=len(self.nodes), prefix="Updating finger tables: ", suffix="Complete", length=75)
            chordNode.updatePredeccessorFingerTable(self)

    def nodeLeave(self, node_to_remove_ID): 
        node_index = self.getIndexFromId(node_to_remove_ID)
        node_to_remove_ID = int(node_to_remove_ID)
        # Move its data to the next node
        firstSuccessor = self.nodes[node_index].fingerTable.successors[0]
        firstSuccessor.data.extend(self.nodes[node_index].getData())

        # Begins the update of fingers
        self.nodes.pop(node_index)
            
        # Find nodes that need Finger Table update
        nodesToUpdate = []
        for chordNode in self.nodes:
            if node_to_remove_ID in (node.getId() for node in chordNode.fingerTable.successors) or chordNode.predecessor.getId() == node_to_remove_ID :
                nodesToUpdate.append(self.nodes.index(chordNode))
        
        for index in nodesToUpdate:
            self.nodes[index].updatePredeccessorFingerTable(self)
        
    def exactMatch(self, data_key, startingNode=0, add_sleep=False):
        # Hash the data key
        hashed_key = Utils.generateHash(data_key, self.m)
        #print('The hash of the given key is: ',hashedKey)

        # Select a random node to start search
        # Currently we use the first one
        targetNode = self.nodes[startingNode].findSuccesor(hashed_key, add_sleep)

        node_hasFailed = False
        if(targetNode.hasFailed):
            # Taking the next node
            node_hasFailed = True
            targetNode = targetNode.fingerTable.successors[0]
        else:
            # Searching the basic storage
            for data_entry in targetNode.getData():
                if data_entry['hash_key'] == hashed_key and data_entry['AttainmentId'] == data_key:
                    return data_entry, targetNode.getId()

    
        # Node failure handling mechanism
        if(node_hasFailed):
            for i in range(self.redundancy_param):
                if(targetNode.hasFailed):
                    # Taking the next node
                    targetNode = targetNode.fingerTable.successors[0]
                else:
                    for data_entry in targetNode.getBackupData()[i]:
                        if data_entry['hash_key'] == hashed_key and data_entry['AttainmentId'] == data_key:
                            return data_entry, targetNode.getId()
        
        # In case key not found in
        # basic storage or backup storage
        return {}, -1


    def rangeQuery(self, startSearchNode, start, stop, add_sleep=False):
        nodesOfInterest = []
        # Set the first node
        nodesOfInterest.append(startSearchNode.findSuccesor(start, add_sleep))

        if start > stop:           # Set the rest of nodes if query surpasses max cord size
            while(nodesOfInterest[-1].getId() <= self.chordSize):
                nodesOfInterest.append(nodesOfInterest[-1].finger(0))
            while(nodesOfInterest[-1].getId() <= stop):
                nodesOfInterest.append(nodesOfInterest[-1].finger(0))
        else:                    # Set the rest of nodes for normal query
            while(nodesOfInterest[-1].getId() < stop):
                nodesOfInterest.append(nodesOfInterest[-1].finger(0))

        # Initialize list with data to return
        data_of_interest = []

        # First node
        for record in nodesOfInterest[0].getData():
            if record['hash_key'] >= start and record['hash_key'] <= stop:
                data_of_interest.append(record)
        # Middle nodes  
        for node in nodesOfInterest[1:-2]:
                data_of_interest.append(node.getData())
        
        # Last node
        for record in nodesOfInterest[-1].getData():
            if record['hash_key'] >= start and record['hash_key'] <= stop:
                data_of_interest.append(record)
        
        return data_of_interest

    def kNNQuery(self, startSearchNode, hash_key, k, add_sleep=False):
        
        allNeighbors = []
        nearestNeighbors = []

        # First fetching the nodes of the hash_key successor
        # and its predecessor
        baseNode = startSearchNode.findSuccesor(hash_key, add_sleep)
        allNeighbors.extend(baseNode.getData())
        allNeighbors.extend(baseNode.predecessor.getData())
        
        if(len(allNeighbors) < k):
            return False

        # Then we extract the nearest neighbors
        for _ in range(k):
            nearestNode = min(allNeighbors, key=lambda x: abs(x['hash_key'] - hash_key))
            allNeighbors.remove(nearestNode)
            nearestNeighbors.append(nearestNode)

        return nearestNeighbors
        
    # Getters
    def getIdList(self):
        return [node.getId() for node in self.nodes]

    def getNodes(self):
        return self.nodes
    
    def getIndexFromId(self, nodeId):
        try:
            res = self.getIdList().index(int(nodeId))
        except ValueError:
            print(f"Node with ID {nodeId} does not exist.\n")
            res = -1
        return res

