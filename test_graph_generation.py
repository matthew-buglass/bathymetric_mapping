import random
import collections
import os

from data_structures.vertex_graph import VertexGraph
from data_structures.vertex_point import VertexPoint

"""
Generates a graph for testing purposes
"""

def print_order(order: int, network):
    """
    Prints out the graph in the order provided
    
    :param order: 0 = in order; 1 = pre order; 2 = post order
    :param network: the node network in a 3D-tree
    
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


# Generating the graph
width = 10
height = 60
abs_coefficient = 0.005

verts = []

# making a hyperbolic paraboloid Vertex's
for x in range(-width, width+1):
    for y in range(-height, height+1):
        z = abs_coefficient * (x**2) + -abs_coefficient * (y**2)
        vert = VertexPoint()
        vert.set_coordinates(x, y, z)
        verts.append(vert)

# Generating the network from the list of vericies    
node_network = VertexGraph.from_list(verts)

# Output the verticies that are within 1 meter of eachother
print("Adjacent coordinates:")
for i in range(-width, width+1):
    for j in range(-height, height+1):
        adjs = node_network.range_search(x_range=(i-1, i+1), y_range=(j-1, j+1))
        adjs_co = [g.get_coordinates() for g in adjs]
        print("vertex ({}, {}, z). Within 1 meter x, y: {}".format(i, j, [(a[0], a[1]) for a in adjs_co]))

# create edges between verticies that are withing 1 meter of eachother across the x and y co-ordinates
print("\nEstablishing x_y proximity within 1 meter")
node_network.establish_euclidean_proximity_xy(1)
for vertex in node_network.get_vertices():
    network_adj = node_network.get_adjacent_within(vertex, 1, 1)
    vertex_adj = [v[0] for v in vertex.get_adjacent()]

    print("vertex {} personal and graph adjacents identical: {}".format(vertex.get_coordinates(),
                                                                        collections.Counter(network_adj) == collections.Counter(vertex_adj)))

# pretty print the verticies
print("\nVertex to pretty json:")
for vertex in node_network.get_vertices():
    print(vertex.to_pretty_json())

# Pretty print graph
print("\nGraph to pretty json:")
graph_json = node_network.to_pretty_json()
print(graph_json)
new_graph = VertexGraph.from_json(graph_json)
print(new_graph)

# write the graph to file
try:
    os.mkdir("jsons")
except FileExistsError:
    pass
with open("jsons/test_data.json", "w+") as f:
    f.write(graph_json)
    f.close()

# get and print the data required to build the graph as a mesh in Blender (https://www.blender.org/)
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
