import collections
import csv

import numpy as np

from data_structures.vertex_graph import VertexGraph
from data_structures.vertex_point import VertexPoint


def print_order(order: int, network):
    """
    :param order: 0 = in order; 1 = pre order; 2 = post order
    :return:
    """
    print(network.to_string_coordinates(order))
    verts_c = network.get_order_coordinates(order)

    order_adjacent = [(abs(verts_c[x][0] - verts_c[x + 1][0]) == 1 or
                       abs(verts_c[x][1] - verts_c[x + 1][1]) == 1) for
                      x in range(len(verts_c) - 1)]
    print("In order coordinates adjacent\n{}".format(order_adjacent))
    print("Number adjacent: {}".format(order_adjacent.count(True)))
    print("Number non-adjacent: {}".format(order_adjacent.count(False)))
    print("Percent adjacent: {:.5f}%".format(order_adjacent.count(True) / len(order_adjacent) * 100))

def get_from_csv_array(file_name):
    with open(file_name, "r") as f:
        reader = csv.reader(f, delimiter=",")
        l = list(reader)
        cols = [float(x) for x in l[0][1:]]
        rows = []
        l = l[1:]

        for i in range(len(l)):
            rows.append(float(l[i][0]))
            l[i] = l[i][1:]

        array = np.array(l).astype("float")
        
        print(array)
        output = []
        for c in range(len(cols)):
            for r in range(len(rows)):
                x_c = cols[c]
                y_c = rows[r]
                z_c = 100 * array[r][c]
                output.append(VertexPoint(x_c, y_c, z_c))

        return output




width = 10
height = 60
abs_coefficient = 0.005

# Getting the co-ordinates from file
verts = get_from_csv_array("D:\\Work\\Curling Research\\Curling Excel Output\\INFORMS_2021\\hammer_coordinate_array.csv")

node_network = VertexGraph.from_list(verts)

print("Adjacent coordinates:")
for i in range(-width, width+1):
    for j in range(-height, height+1):
        adjs = node_network.range_search(x_range=(i-1, i+1), y_range=(j-1, j+1))
        adjs_co = [g.get_coordinates() for g in adjs]
        print("vertex ({}, {}, z). Within 1 meter x, y: {}".format(i, j, [(a[0], a[1]) for a in adjs_co]))


print("\nEstablishing x_y proximity within 1 meter")
node_network.establish_euclidean_proximity_xy(1)
for vertex in node_network.get_vertices():
    network_adj = node_network.get_adjacent_within(vertex, 1, 1)
    vertex_adj = [v[0] for v in vertex.get_adjacent()]

    print("vertex {} personal and graph adjacents identical: {}".format(vertex.get_coordinates(),
                                                                        collections.Counter(network_adj) == collections.Counter(vertex_adj)))

print("\nVertex to pretty json:")
for vertex in node_network.get_vertices():
    print(vertex.to_pretty_json())

print("\nGraph to pretty json:")
graph_json = node_network.to_pretty_json()
print(graph_json)
new_graph = VertexGraph.from_json(graph_json)
print(new_graph)

with open("D:\\Work\\Curling Research\\Curling Excel Output\\INFORMS_2021\\hammer_coordinates.json", "w+") as f:
    f.write(graph_json)
    f.close()

vertices, edges, faces = node_network.get_blender_data()

print("\nVertices:")
for v in vertices:
    print(v)

print("\nEdges:")
for e in edges:
    print(e)

print("\nFaces:")
for f in faces:
    print(f)
