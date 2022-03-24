import bpy
import json
import importlib.util
import os
import sys
from importlib.machinery import SourceFileLoader
import time

"""
Script to build a mesh from a vertex graph.

CAN ONLY BE RUN FROM THE SCRIPTING TERMINAL IN THE BLENDER APPLICATON
"""

# Changing the working directory to load modules
script_root = os.path.dirname(bpy.data.filepath)
script_root = script_root.split("\\")
script_root = script_root[0:len(script_root)-1]
script_root.append("bathymetric_mapping_scripts")
script_root = "\\".join(script_root)
os.chdir(script_root)
print(os.getcwd())

# imports the module containing the VertexGraph data structure from the given absolute path
vg = SourceFileLoader("vertex_graph", script_root+"\\data_structures\\vertex_graph.py").load_module()

# load the graph from the given absolute path
data_filename = "test_data.json"
file_name = script_root+"\\jsons\\" + data_filename

with open(file_name, "r") as f:
    data = json.load(f)
    f.close()

#print(data)

# deserializing the graph and building the edges between adjacent verticies
g = vg.VertexGraph.from_json(json.dumps(data))
g.establish_euclidean_proximity_xy(1)
vertices, edges, faces = g.get_blender_data()

# instantiate a new mesh and define it's verticies, edges, and faces
new_mesh=bpy.data.meshes.new("new_mesh")
new_mesh.from_pydata(vertices, edges, faces)
new_mesh.update()

# make object from the mesh data
new_object = bpy.data.objects.new("hyperbolic_paraboloid", new_mesh)

view_layer=bpy.context.view_layer
view_layer.active_layer_collection.collection.objects.link(new_object)

#bpy.ops.object.mode_set(mode='EDIT') 
#bpy.ops.mesh.select_mode(type="VERT")
#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.edge_face_add()   
#bpy.ops.mesh.select_all(action='DESELECT') 
#bpy.ops.object.mode_set(mode='OBJECT') 
#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
