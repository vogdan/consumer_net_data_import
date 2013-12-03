'''
creez o matrice care are leg[turile dintre site-uri ca informatie

for line in file
    put line in dict
    got_1 = 0
    for key in dict
        if dict[key] == 1: 
            if got_1:
               matrice[site1, key] += 1 ;# tine cont ca matrice[site1, key] == matrice[key, site1]
            else:
                got_1 = 1
                site1 = key
            
'''
from csv import reader, writer


class Node:

    def __init__(self, name):
        self.name = str(name)

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

 
class Link:

    def __init__(self, src, dest, weight=0):
        self.src = src
        self.dest = dest
        self.weight = weight

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dest

    def getWeight(self):
        return self.weight

    def __str__(self):
        return str(self.src) + '->' + str(self.dest)


class SimpleGraph:

    def __init__(self):
        self.nodes = set([])
        self.links = {}

    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.links[node] = {}

    def addLink(self, link, weight=1):
        src = link.getSource()
        dest = link.getDestination()
        weight = link.getWeight()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.links[src][dest]=weight

    def childrenOf(self, node):
        return self.links[node]

    def hasNode(self, node):
        return node in self.nodes

    def __str__(self):
        res = ''
        for k in self.links:
            for d in self.links[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]

    def linkWeight(self,node1,node2):
        if not self.hasNode(node1) or not self.hasNode(node2)or node2 not in self.links[node1]:
            raise ValueError('Node not in graph')
        return self.links[node1][node2]

    

input_file = "../ExperianBrands.csv"
graph = SimpleGraph()

with open(input_file, 'rb') as csv_file:
    rdr = reader(csv_file)
    header = rdr.next()
    for entry in header[1:]:
        graph.addNode(entry)
    
    for row in rdr:
        for source in row:
            if source:
                src_idx = row.index(source)
                for destination in row[src_idx:]:
                    if destination:
                        dest_idx = row.index(destination)
                        srcNode = Node(header(src_idx)
                        destNode = Node(dest_idx)
                        graph.addLink(Link(srcNode, destNode))


