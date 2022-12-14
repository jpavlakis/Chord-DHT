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
        self.id = Utils.generateHash(self.ipAddress, m)

    def setFingerTable(self, fingerTable):
        self.fingerTable = fingerTable

    def finger(self, i):
        return self.fingerTable.getSuccessors()[i]

    def findSuccessor(self, looking_id, add_sleep=False):

        offset = 2**self.m

        if looking_id == self.id:
            return self

        looking_id_offseted = looking_id + 0
        # The looking ID is after the chord zero needs an offset.
        if looking_id < self.id:
            looking_id_offseted = looking_id + offset

        # If current Finger Table Node is after the chord zero, offset is needed.
        current_fingerTable_nodeId = self.fingerTable.successors[0].id
        if current_fingerTable_nodeId < self.id:
            current_fingerTable_nodeId += offset

        if current_fingerTable_nodeId >= looking_id_offseted:
            #print('First Element Bigger, goes to the next node.')
            return self.fingerTable.successors[0]

        for index, fingerTable_node in enumerate(self.fingerTable.successors):    
            current_fingerTable_nodeId = fingerTable_node.id
            if(add_sleep):
                sleep(0.001)
            # If current Finger Table Node is after the chord zero, offset is needed.
            if(fingerTable_node.id < self.id):
                current_fingerTable_nodeId += offset

            if looking_id_offseted <= current_fingerTable_nodeId:
                return self.fingerTable.successors[index-1].findSuccessor(looking_id)
        else:
            return self.fingerTable.successors[-1].findSuccessor(looking_id)


    def updatePredeccessorFingerTable(self, chord):
        # Update Predecessor
        self_idx = chord.nodes.index(self) 
        self.predecessor = chord.nodes[(len(chord.nodes) + self_idx-1 ) % len(chord.nodes)]
        
        # Update Successors
        self.fingerTable.updateFingerTable()

    def getSuccessorsId(self):
        return [node.id for node in self.fingerTable.successors]
    
    def getIpAddress(self):
        return self.ipAddress

    def getId(self):
        return self.id

    def getPredecessor(self):
        return self.predecessor

    def getData(self):
        return self.data

    def getBackupData(self):
        return self.backupData

