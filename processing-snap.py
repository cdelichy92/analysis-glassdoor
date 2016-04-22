# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 12:36:47 2015

@author: Cyprien
"""

import csv
import json

#files
file_node = "jobs-ids.csv"
file_edge = "job-edges.csv"

job_idH = {}
id_jobH = {}

with open(file_node, 'r') as jobidfile:
    for line in jobidfile:
        line = line.strip()
        elems = line.split(',')        
        job = elems[0]
        idjob = int(elems[1])
        
        job_idH[job] = idjob
        id_jobH[idjob] = job
        
with open('jobs-ids.json', 'w') as outfile:
    json.dump(job_idH, outfile)
    
with open('ids-jobs.json', 'w') as outfile2:
    json.dump(id_jobH, outfile2)

fedges = open('snap-job-edges.csv', 'w')

with open(file_edge, 'r') as f:
    for line in f:
        line = line.strip()
        elems = line.split(',')
        
        if int(elems[2]) >= 5:
            try:
                fedges.write("%d,%d,%d\n" %(job_idH[elems[0]], job_idH[elems[1]], int(elems[2])))
            except:
                continue