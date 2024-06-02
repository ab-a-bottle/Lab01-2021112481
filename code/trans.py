import re
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# input:string
# Output:Adjacency Matrix,word to nodenumber dic,nodenumber to word dic
def text2matrix(text):
    # turn input to lower case to avoid recongizing A and a as different word
    text = text.lower()
    # delete non-litter item
    text = re.sub('[^a-zA-Z]', ' ', text)
    splited = text.split()
    # init dics
    node2word = dict()
    word2node = dict()
    # set dic values
    for i,elem in enumerate(set(splited)):
        node2word[i]=elem
        word2node[elem]=i
    # init Adjacency Matrix
    matri = np.zeros((len(set(splited)),len(set(splited))),dtype=int)
    # set Adj Matrix values
    for i in range(len(splited)-1):
        out = word2node[splited[i]]
        in_num = word2node[splited[i+1]]
        matri[out,in_num] += 1
    return matri,word2node,node2word


# input:nodenumber to word dic,Adj Matrix
# output:graph
def matrix2graph(node2word,matrix):
    # init Graph
    G = nx.DiGraph()

    # add egdes and nodes
    for i in range(len(matrix)):
        G.add_node(i, name=node2word[i])
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                G.add_edge(i, j,weight= matrix[i][j])
    return G


# input:graph
# output:none
def showDirectedGraph(G):
    # set nodes` position
    pos = nx.spring_layout(G) 
    # draw nodes and edges
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'name'))
    # add edges` weight
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.savefig("Graph.png")
    # show img
    plt.show()
