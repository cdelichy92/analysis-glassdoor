import csv

#files
file_node = "jobs-ids3.csv"
file_edge = "job-edges3.csv"

dict_id = {}
header_node = ['nodedef>name','label','salary low DOUBLE','salary median DOUBLE','salary high DOUBLE']
header_edge = ['edgedef>node1','node2','count DOUBLE','percentage DOUBLE','national_count DOUBLE']

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
                    filewriter.writerow([dict_id[row[0]],dict_id[row[1]],row[2],row[3],row[4]])
            except:
                continue
