# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 13:49:36 2015

@author: Cyprien
"""

from snap import *
import json

file_edge = "snap-job-edges.csv"
file_node = "ids-jobs.json"

with open(file_node, 'r') as idjobfile:
    for line in idjobfile:
        id_jobH = json.loads(line.strip())

counter = 0
      
G = TNGraph.New()
weightH = {}

with open(file_edge, 'r') as f:
  for line in f:
      line = line.strip()
      elems = line.split(',')
      
      n1, n2, weight = int(elems[0]), int(elems[1]), int(elems[2])

      if not G.IsNode(n1):
          G.AddNode(n1)
      if not G.IsNode(n2):
          G.AddNode(n2)
      
      G.AddEdge(n1,n2)
      weightH[(n1,n2)]=weight

G = GetMxWcc(G)

G.GetNodes()
G.GetEdges()

InDegV = TIntPrV()
GetNodeInDegV(G, InDegV)

DegSorted = sorted(InDegV, key=lambda x: x.GetVal2(), reverse = True)

print "Top 20 jobs with highest in-degree :"
for job in DegSorted[:20]:
    print "%s : \t %d" % (id_jobH[str(job.GetVal1())], job.GetVal2())
 

NIdBtwH = TIntFltH()
EdgeBtwH = TIntPrFltH()
GetBetweennessCentr(G, NIdBtwH, EdgeBtwH, 1)

BtwSorted = sorted(NIdBtwH, key=lambda key: NIdBtwH[key], reverse = True)

print "Top 20 jobs with highest betweenness :"
for job in BtwSorted[:20]:
    print "%s : \t %.1f, main genre : %s" % (id_jobH[str(job)][0], NIdBtwH[job])


#NIdClsH = TIntFltH()
#
#for NI in G.Nodes():
#    NIdClsH[NI.GetId()] = GetClosenessCentr(G, NI.GetId())
#    
#ClsSorted = sorted(NIdClsH, key=lambda key: NIdClsH[key], reverse = True)
#
#print "Top 20 jobs with highest closeness :"
#for job in ClsSorted[:20]:
#    print "%s : \t %.5f" % (id_jobH[str(job)], NIdClsH[job])