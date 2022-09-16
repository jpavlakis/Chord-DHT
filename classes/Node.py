from time import sleep
from classes import Utils

class Node:
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        self.id = None
        self.fingerTable = None
        self.predecessor= None
        self.m = None
        self.hasFailed = False
        self.data = []
        self.backupData = []


    def setId(self, m):
        """
        Hashing the IP Address using sha1 algorithm and from the 160 bit
        output we only take the m last bits.
        """
        self.m = m
        self.id = Utils.hashing(self.ipAddress, m)

    def setFingerTable(self, fingerTable):
        self.fingerTable = fingerTable

    def finger(self, i):
        allSucc = self.fingerTable.getSuccessors()
        return allSucc[i]

    def findSuccesor(self, looking_id, add_sleep=False):

        offset = 2**self.m

        if looking_id==self.id:
            return self

        # The looking ID is after the chord zero needs an offset.
        lookingIdOffseted = looking_id
        if looking_id < self.id:
            #print('Offset to looking ID added: ',lookingId,' -> ',lookingId+offset)
            lookingIdOffseted+=offset

        # If current Finger Table Node is after the chord zero, offset is needed.
        current_finger_table_node_id = self.fingerTable.successors[0].id 
        if current_finger_table_node_id < self.id:
            current_finger_table_node_id+=offset

        if current_finger_table_node_id >= lookingIdOffseted:
            #print('First Element Bigger, goes to the next node.')
            #print(self.fingerTable.successors[0].id)
            return self.fingerTable.successors[0]

        for index,finger_table_node in enumerate(self.fingerTable.successors):    
            current_finger_table_node_id = finger_table_node.id
            if(add_sleep):
                sleep(0.001)
            # If current Finger Table Node is after the chord zero, offset is needed.
            if(finger_table_node.id<self.id):
                #print('Offset to the finger table node id, added: ',current_finger_table_node_id,' -> ',current_finger_table_node_id+offset)
                current_finger_table_node_id+=offset

            if lookingIdOffseted <= current_finger_table_node_id:
                return self.fingerTable.successors[index-1].findSuccesor(looking_id)
                # break
        else:
            return self.fingerTable.successors[-1].findSuccesor(looking_id)


    def getSuccessorsId(self):
        return [node.id for node in self.fingerTable.successors]

    def updatePredeccessorFingerTable(self, chord):
        # Update Predecessor
        self_idx = chord.nodes.index(self) 
        self.predecessor = chord.nodes[(len(chord.nodes) + self_idx-1 ) % len(chord.nodes)]
        
        # Update Successors
        self.fingerTable.updateFingerTable()

    def getId(self):
        return self.id

    # Returns a string with all the values of a specific 
    # key from all the data stored in that node
    # Usefull for debugging and demo purposes
    def getDataAttributeString(self, key):
        data_values = [str(data_entry[key] for data_entry in self.data)]
        return ', '.join(data_values)
