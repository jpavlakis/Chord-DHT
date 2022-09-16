# Class for saving IDs for predecessors/successors
class FingerTable:
    def __init__(self, chord, node):
        self.successors = []
        self.chord = chord
        self.node = node
        self.chordSize = chord.chordSize
        
    def updateFingerTable(self):

        # γινεται χρηση του ID γιατι αν χρησιμοποιηθει direct διευθυνσιοδοτηση και αλλάξουν σειρα τα chord nodes, δειχνει σε αλλον node
        self.successors = []
        chordNodesID = self.chord.getIdList()
        newNodeId = self.node.getId()
        numOfNodes = len(chordNodesID)

        # If only one node, point to itself
        if numOfNodes == 1:
            for i in range(self.chord.m):
                self.successors.append(self.node)
        else:
            for i in range(self.chord.m):
                wantedSucccesorId = (newNodeId + ( 1 << i )) % self.chordSize
                wantedSucccesorIndex = 0
                while chordNodesID[wantedSucccesorIndex % numOfNodes] < wantedSucccesorId:
                    if wantedSucccesorIndex / numOfNodes >= 1 and chordNodesID[wantedSucccesorIndex%numOfNodes] + self.chordSize >= wantedSucccesorId:
                        wantedSucccesorIndex=wantedSucccesorIndex % numOfNodes
                        break
                    wantedSucccesorIndex += 1
                self.successors.append(self.chord.nodes[wantedSucccesorIndex])

    
    def getSuccessors(self):
        return self.successors

