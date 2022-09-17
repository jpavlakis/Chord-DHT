from classes import FingerTable
from classes import Utils

class Chord:
    def __init__(self, m, safety_parameter):
        self.m = m
        self.safety_parameter = safety_parameter
        self.chordSize = 1 << m # 2^m
        self.nodes = []

    def insertData(self, row, index):

        # Defining unique key
        key = Utils.hashing(row['AttainmentId'], self.m)
        # Building our data structur
        data = row.to_dict()
        data['hash_key'] = key
        targetNode = self.nodes[index].findSuccesor(key)
        targetNode.data.append(data)

        # Failure prevention mechanism
        # Adding redundancy of keys to the successor of the node
        current_node = targetNode
        for i in range(self.safety_parameter):
            nextNode = current_node.fingerTable.successors[0]

            #if its the first time create it with append else override
            if len(nextNode.backupData) < self.safety_parameter:
                nextNode.backupData.append(targetNode.data.copy())
            else:
                nextNode.backupData[i] = targetNode.data.copy()
            current_node = nextNode

    def insertKey(self, data_key, index):

        # Create empty dict with the same structure as the rest of the data
        data = dict((key, None) for key, value in self.nodes[0].data[-1].items())

        data['AttainmentId'] = data_key
        data['hash_key'] = Utils.hashing(data_key, self.m)
        
        targetNode = self.nodes[index].findSuccesor(data['hash_key'])
        targetNode.data.append(data)
        
        # Failure prevention mechanism
        # Adding redundancy of keys to the successor of the node
        currentNode = targetNode
        for i in range(self.safety_parameter):
            nextNode = currentNode.fingerTable.successors[0]

            #if its the first time create it with append else override
            if len(nextNode.backupData) < self.safety_parameter:
                nextNode.backupData.append(targetNode.data.copy())
            else:
                nextNode.backupData[i] = targetNode.data.copy()
            currentNode = nextNode

    def deleteKey(self, data_key):
        
        result, nodeId = self.exactMatch(data_key)
        targetNode = self.nodes[self.getIndexFromId(nodeId)]
        for entry in targetNode.data:
            if result['hash_key'] == Utils.hashing(data_key, self.m) and result['AttainmentId'] == data_key:
                previous_data_len = len(targetNode.data)
                targetNode.data.remove(entry)
                new_data_len = len(targetNode.data)
                print(f'Key {data_key} has been deleted from node {targetNode.id}.')
                print(f'Previous Data count: {previous_data_len} \t New Data count: {new_data_len}')

    
    def updateRecord(self, key):
       
        hashed_key = Utils.hashing(key, self.m)
        print(f'The hash of the given key is: {hashed_key}')

        # Select a random node to start search
        # Currently we use the first one
        targetNode = self.nodes[0].findSuccesor(hashed_key)

        for dataEntry in targetNode.data:
            if(dataEntry['hash_key']==hashed_key):
                print('Data entry found.')
                valid_input = False
                while(not valid_input):
                    column = input('Give the column you want to edit: ')
                    if(column in dataEntry):
                        new_value = input('Give the new value: ')
                        dataEntry[column] = new_value
                        return
                    else:
                        print('That column does not exist.')

        # Integrating the failure prevention mechanism
        for _ in range(self.safety_parameter):
            if(targetNode.hasFailed):
                # Taking the next node
                print('Node has failed I move to the next one')
                targetNode = targetNode.fingeTable.successors[0]
            else:
                for dataEntry in targetNode.data:
                    if(dataEntry['hash_key']==hashed_key):
                        print('I fount it! ')
                        valid_input = False
                        while(not valid_input):
                            column = input('Give the column you want to edit: ')
                            if(column in dataEntry):
                                new_value = input('Give the new value: ')
                                dataEntry[column] = new_value
                                return
                            else:
                                print('That column does not exist!')

    def nodeJoin(self, node):
        # Create node ID for the given Chord
        node.setId(self.m)
        
        # Making sure that we don't have double ids
        while node.id in (chord_node.id for chord_node in self.nodes):
            node.id = (node.id + 1)%2 **self.m

        # Insert ordered in Node's list 
        self.nodes.append(node)
        i = len(self.nodes) - 1
        if i > 0:
            while self.nodes[i-1].getId() > self.nodes[i].getId() and i > 0:
                self.nodes[i-1], self.nodes[i]=self.nodes[i], self.nodes[i-1]
                i-=1    

        # Create Finger Table 
        node.setFingerTable(FingerTable.FingerTable(self, node))
        node.updatePredeccessorFingerTable(self)

        # Find nodes that need Finger Table update
        nodesToUpdate = []
        for chordNode in self.nodes:
            for pow in range(self.m):
                estimSuccID = chordNode.id + (2**pow)
                estimSuccID = estimSuccID % self.chordSize
                if estimSuccID <= node.id + self.chordSize and estimSuccID + self.chordSize > node.predecessor.id:
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
        for current_data in firstSuccessor.data:
            if node.id >= current_data['hash_key'] :
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
            Utils.print_progress_bar(iteration=idx+1, total=len(nodes), prefix="Massive node join: ", suffix="Complete", length=75, printEnd='\r')
            # Create node ID for the given Chord
            node.setId(self.m)
            
            # Making sure that we don't have double ids
            while node.id in (chord_node.id for chord_node in self.nodes):
                node.id = (node.id + 1)%2**self.m

            # Insert ordered in Node's list 
            self.nodes.append(node)
            i = len(self.nodes) - 1
            if i > 0:
                while self.nodes[i-1].getId() > self.nodes[i].getId() and i > 0:
                    self.nodes[i-1], self.nodes[i]=self.nodes[i], self.nodes[i-1]
                    i-=1    

            # Create Finger Table 
            node.setFingerTable(FingerTable.FingerTable(self, node))

        # Find nodes that need Finger Table update
        for idx, chordNode in enumerate(self.nodes):
            Utils.print_progress_bar(iteration=idx+1, total=len(self.nodes), prefix="Updating finger tables: ", suffix="Complete", length=75, printEnd='\r')
            chordNode.updatePredeccessorFingerTable(self)

    def nodeLeave(self, node_to_remove_ID): 
        node_index = self.getIndexFromId(node_to_remove_ID)
        node_to_remove_ID = int(node_to_remove_ID)
        # Move its data to the next node
        firstSuccessor = self.nodes[node_index].fingerTable.successors[0]
        firstSuccessor.data.extend(self.nodes[node_index].data)

        # Begins the update of fingers
        self.nodes.pop(node_index)
            
        # Find nodes that need Finger Table update
        nodesToUpdate = []
        for chordNode in self.nodes:
            if node_to_remove_ID in (node.id for node in chordNode.fingerTable.successors) or chordNode.predecessor.id == node_to_remove_ID :
                nodesToUpdate.append(self.nodes.index(chordNode))
        
        for index in nodesToUpdate:
            self.nodes[index].updatePredeccessorFingerTable(self)
        
    def exactMatch(self, data_key, startingNode=0, add_sleep=False):
        
        # Hash the data key
        hashed_key = Utils.hashing(data_key, self.m)
        #print('The hash of the given key is: ',hashedKey)

        # Select a random node to start search
        # Currently we use the first one
        targetNode = self.nodes[startingNode].findSuccesor(hashed_key, add_sleep)

        # Integrating the failure te
        node_hasFailed = False
        if(targetNode.hasFailed):
            # Taking the next node
            #print('Node has failed I move to the next one')
            node_hasFailed = True
            targetNode = targetNode.fingerTable.successors[0]
        else:
            # Searching the basic storage
            for data_entry in targetNode.data:
                if(data_entry['hash_key']==hashed_key):
                    #print('Found in basic storage')
                    return data_entry, targetNode.id

    
        # Node failure handling mechanism
        if(node_hasFailed):
            for i in range(self.safety_parameter):
                if(targetNode.hasFailed):
                    # Taking the next node
                    #print('Node has failed I move to the next one')
                    targetNode = targetNode.fingerTable.successors[0]
                else:
                    for data_entry in targetNode.backupData[i]:
                        if(data_entry['hash_key']==hashed_key):
                            #print('Found in backup storage')
                            #print('The id of the good node: ',targetNode.id)
                            return data_entry


    def rangeQuery(self, startSearchNode, start, stop):
        nodesOfInterest = []
        # Set the first node
        nodesOfInterest.append(startSearchNode.findSuccesor(start))

        if start > stop:           # Set the rest of nodes if query surpasses max cord size
            while(nodesOfInterest[-1].id <= self.chordSize):
                nodesOfInterest.append(nodesOfInterest[-1].finger(0))
            while(nodesOfInterest[-1].id <= stop):
                nodesOfInterest.append(nodesOfInterest[-1].finger(0))
        else:                    # Set the rest of nodes for normal query
            while(nodesOfInterest[-1].id < stop):
                nodesOfInterest.append(nodesOfInterest[-1].finger(0))

        # Initialize list with data to return
        data_of_interest = []

        # First node
        for record in nodesOfInterest[0].data:
            if record['hash_key'] >= start and record['hash_key']<=stop:
                data_of_interest.append(record)
        # Middle nodes  
        for node in nodesOfInterest[1:-2]:
                data_of_interest.append(node.data)
        
        # Last node
        for record in nodesOfInterest[-1].data:
            if record['hash_key'] >= start and record['hash_key']<=stop:
                data_of_interest.append(record)
        
        return data_of_interest

    # TODO: Can be improved. Find the nearest neighbors of value from all nodes (?)
    # Add all the closest values from the baseNode, its successors and going forward
    # Add all the closest values from the baseNode's predecessor and backwords
    # Until we find the K nearest neighbors of the value
    def kNNQuery(self, startSearchNode, hash_key, n):    
        
        allNeighbors = []
        nearestNeighbors = []

        # First fetching the nodes of the hash_key successor
        # and its predecessor
        baseNode = startSearchNode.findSuccesor(hash_key)
        allNeighbors.extend(baseNode.data)
        allNeighbors.extend(baseNode.predecessor.data)
        
        if(len(allNeighbors) < n):
            return False

        # Then we extract the nearest neighbors
        for _ in range(n):
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
            print("   =>ERROR: Node with such ID does not exist!\n")
            res = -1
        return res

