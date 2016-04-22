import csv

#files
file_node = "jobs-ids3.csv"
file_edge = "job-edges3.csv"

dict_id = {}
dict_job_count = {}
header_node = ['nodedef>name','label','salary low DOUBLE','salary median DOUBLE','salary high DOUBLE']
header_edge = ['edgedef>node1','node2','count DOUBLE','percentage DOUBLE','national_count DOUBLE']

starting_queue = ['software engineer',
                      'engineer', 
                      'surgeon', 
                      'dentist',
                      'doctor', 
                      'physician', 
                      'lawyer', 
                      'architect', 
                      'assistant professor', 
                      'artist', 
                      'geologist', 
                      'recruiter',
                      'legal intern',
                      'public relations intern']

#create gdf file
with open('big_graph2.gdf', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(header_node)
    with open(file_node, 'rb') as csvfile:
        nodes = csv.reader(csvfile, delimiter=',')
        for row in nodes:
            dict_id[row[0]] = row[1]
            filewriter.writerow([row[1],row[0],row[2],row[3],row[4]])

    filewriter.writerow(header_edge)
    with open(file_edge, 'rb') as csvfile:
        edges = csv.reader(csvfile, delimiter=',')
        for row in edges:
            try:
                if (int(row[2]) < 5): #remove edges with low count
                    continue
                else:
                    dict_job_count[int(dict_id[row[1]])] = int(row[4])
                    filewriter.writerow([dict_id[row[0]],dict_id[row[1]],row[2],row[3]])
            except:
                continue

infile = open("big_graph2.gdf", 'r') # open file for appending
outfile = open("big_graph3.gdf",'w') # open file for appending
node_part_bool = True

for line in infile.readlines():
    line = line.strip()
    if line == 'nodedef>name,label,salary low DOUBLE,salary median DOUBLE,salary high DOUBLE':
        outfile.write(line + ',national_count DOUBLE\n')
    elif line == 'edgedef>node1,node2,count DOUBLE,percentage DOUBLE,national_count DOUBLE':
        node_part_bool = False
        outfile.write('edgedef>node1,node2,count DOUBLE,percentage DOUBLE\n')
    else:
        elems = line.split(',')
        if node_part_bool:
            id_job = int(elems[0])
            if id_job in dict_job_count:
                outfile.write(line + ',' + str(dict_job_count[id_job]) + '\n')
            else:
                if elems[1] in starting_queue:
                    outfile.write(line + ',' + '9999999999999' + '\n')
                else:
                    outfile.write(line + ',' + '-1' + '\n')
        else:
            outfile.write(line + '\n')

infile.close()
outfile.close()
