import bpy
import json
import importlib.util
import os
import sys
from importlib.machinery import SourceFileLoader
import time

# imports the module from the given path
vg = SourceFileLoader("vertex_graph", "D:\\Bathymetric Mapping\\bathymetric_mapping_scripts\\data_structures\\vertex_graph.py").load_module()

print(os.getcwd())
file_name = "D:\\Bathymetric Mapping\\bathymetric_mapping_scripts\\jsons\\test_data.json"

with open(file_name, "r") as f:
    data = json.load(f)
    f.close()

# remaking the graph and establishing the point proximity
g = vg.VertexGraph.from_json(json.dumps(data))
g.establish_euclidean_proximity_xy(1)
vertices, edges, faces = g.get_blender_data()

new_mesh=bpy.data.meshes.new("new_mesh")
new_mesh.from_pydata(vertices, edges, faces)
new_mesh.update()

#make object from the mesh
new_object = bpy.data.objects.new("hyperbolic_paraboloid", new_mesh)

view_layer=bpy.context.view_layer
view_layer.active_layer_collection.collection.objects.link(new_object)