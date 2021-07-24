import bpy
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

# remaking the graph and establishing the point proximity
g = vg.VertexGraph.from_json(json.dumps(data))
g.establish_proximity_xy(1)
data_vert_to_blend_vert_map = {}
verts = g.get_vertices()

for vert in verts:
    x = vert.get_x()
    y = vert.get_y()
    z = vert.get_z()
    
    print(x, y, z)
    
    blend_vert = bpy.ops.mesh.primitive_vert_add()
    bpy.ops.transform.translate(value=(x, y, z), orient_type='GLOBAL')
    
    data_vert_to_blend_vert_map[vert] = blend_vert
    vert.set_created()

# deselecting all onf the verticies
bpy.ops.object.mode_set(mode='EDIT') 
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action='DESELECT')    
bpy.ops.object.mode_set(mode='OBJECT') 
obj = bpy.context.active_object

for vert in verts:
    if not vert.visited:
        adj_verts = vert.get_adjacent()
        vert_indx = obj.data.vertices.index(data_vert_to_blend_vert_map[vert])
        
        for adj_v, adj_e in adj_verts:
            if not adj_e:    # if we don't have an edge
                adj_idx = obj.data.vertices.index(data_vert_to_blend_vert_map[adj_v])
                
                obj.data.vertices[vert_idx].select=True
                obj.data.vertices[adj_idx].select=True
                
                bpy.ops.mesh.edge_face_add()
                
                bpy.ops.object.mode_set(mode='EDIT')
                
                obj.data.vertices[vert_idx].select=False
                obj.data.vertices[adj_idx].select=False
                
                bpy.ops.object.mode_set(mode='OBJECT')
                
                vert.set_connected(adj_v)
                adj_v.set_connected(vert)
        
        vert.set_visited
 
bpy.ops.object.mode_set(mode='EDIT') 
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action='DESELECT')    
bpy.ops.object.mode_set(mode='OBJECT')        

#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.edge_face_add()
#bpy.ops.object.editmode_toggle()
#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
