# import bpy
import json
import importlib.util
import os
import sys
from importlib.machinery import SourceFileLoader

# imports the module from the given path
vg = SourceFileLoader("vertex_graph", "D:\\Bathymetric Mapping\\bathymetric_mapping_scripts\\data_structures\\vertex_graph.py").load_module()

print(os.getcwd())
file_name = "D:\\Bathymetric Mapping\\bathymetric_mapping_scripts\\jsons\\test_data.json"

with open(file_name, "r") as f:
    data = json.load(f)
    f.close()

print(data)

g = vg.VertexGraph.from_json(json.dumps(data))
verts = g.get_vertices()

for vert in verts:
    x = vert.get_x()
    y = vert.get_y()
    z = vert.get_z()
    
    print(x, y, z)