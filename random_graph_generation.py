import random
import collections

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


width = 2
height = 3
max_depth = -30

verts = []

for x in range(width):
    for y in range(height):
        z = random.random() * max_depth
        vert = VertexPoint()
        vert.set_coordinates(x, y, z)
        verts.append(vert)

node_network = VertexGraph.from_list(verts)

print("Adjacent coordinates:")
for i in range(width):
    for j in range(height):
        adjs = node_network.range_search(x_range=(i-1, i+1), y_range=(j-1, j+1))
        adjs_co = [g.get_coordinates() for g in adjs]
        print("vertex ({}, {}, z). Within 1 meter x, y: {}".format(i, j, [(a[0], a[1]) for a in adjs_co]))


print("\nEstablishing x_y proximity within 1 meter")
node_network.establish_proximity_xy(1)
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
