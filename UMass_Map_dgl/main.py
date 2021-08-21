# Back-up code

import sys
from os import PRIO_USER
import torch
import dgl
import random as rand

source_node = int(sys.argv[1])
destination_node = int(sys.argv[2])

src = torch.LongTensor([0, 0, 0, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 7, 8, 9, 10,
     1, 2, 3, 3, 3, 4, 5, 5, 6, 5, 8, 6, 8, 9, 8, 11, 11, 10, 11])

dst = torch.LongTensor([1, 2, 3, 3, 3, 4, 5, 5, 6, 5, 8, 6, 8, 9, 8, 11, 11, 10, 11,
     0, 0, 0, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 7, 8, 9, 10])

g = dgl.graph((src, dst))

# frontier = dgl.in_subgraph(g, [8])
# first_hop = dgl.in_subgraph(g, frontier.all_edges()[0])

# print(frontier.all_edges(), first_hop.all_edges())
# combined = torch.cat((first_hop.all_edges()[0].unique(), frontier.all_edges()[0], frontier.all_edges()[1].unique()))
# uniques, counts = combined.unique(return_counts=True)
# difference = uniques[counts == 1]


# print('All second hop nodes: ', difference)
# print('All first hop nodes: ', frontier.all_edges()[0])
# print('Src nodes: ', frontier.srcnodes())
# print('Dst nodes: ', frontier.dstnodes())

# To find the k_hop neighbors
def k_hop(graph, srcNode, k):
    difference = [0]
    if (k == 1): return dgl.in_subgraph(graph, srcNode).all_edges()[0]
    for x in range(k - 1):
        fr = dgl.in_subgraph(graph, srcNode)
        srcNode = fr.all_edges()[0]
        f_hop = dgl.in_subgraph(graph, fr.all_edges()[0])
        combined = torch.cat((f_hop.all_edges()[0].unique(), srcNode, fr.all_edges()[1].unique()))
        uniques, counts = combined.unique(return_counts=True)
        difference = uniques[counts == 1]
    return difference if torch.numel(difference) > 0 else 'empty'

def path(graph, srcNodes, pathLength):
    uniRandWalk = dgl.sampling.random_walk(graph, srcNodes, length=pathLength)
    paths = uniRandWalk[0]
    for x in range(len(srcNodes)):
        print('Random path starting from ', srcNodes[x], ': ', paths[x])
    return 'Success'

def pathWithFrontier(graph, srcNode, length):
    tenList = srcNode
    for x in range(length):
        tenr = k_hop(graph, srcNode, 1)
        srcNode = tenr[rand.randint(0, torch.numel(tenr) - 1)].tolist()
        tenList.append(srcNode)
    return tenList