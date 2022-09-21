class FingerTable:
    def __init__(self, chord, node):
        self.successors = []
        self.chord = chord
        self.node = node
        self.chordSize = chord.chordSize
        
    def updateFingerTable(self):

        self.successors = []
        chordNodesID = self.chord.getIdList()
        newNodeId = self.node.getId()
        num_of_nodes = len(chordNodesID)

        # If only one node, point to itself
        if num_of_nodes == 1:
            for i in range(self.chord.m):
                self.successors.append(self.node)
        else:
            for i in range(self.chord.m):
                wantedSucccesorId = (newNodeId + ( 1 << i )) % self.chordSize
                wantedSucccesorIndex = 0
                while chordNodesID[wantedSucccesorIndex % num_of_nodes] < wantedSucccesorId:
                    if (wantedSucccesorIndex / num_of_nodes) >= 1 and (chordNodesID[wantedSucccesorIndex % num_of_nodes] + self.chordSize) >= wantedSucccesorId:
                        wantedSucccesorIndex = wantedSucccesorIndex % num_of_nodes
                        break
                    wantedSucccesorIndex += 1
                self.successors.append(self.chord.nodes[wantedSucccesorIndex])

    
    def getSuccessors(self):
        return self.successors

