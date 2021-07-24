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

#print(data)

# remaking the graph and establishing the point proximity
g = vg.VertexGraph.from_json(json.dumps(data))
g.establish_proximity_xy(1)
vertices, edges, faces = g.get_blender_data()

new_mesh=bpy.data.meshes.new("new_mesh")
new_mesh.from_pydata(vertices, edges, faces)
new_mesh.update()

#make object from the mesh
new_object = bpy.data.objects.new("new_object", new_mesh)

view_layer=bpy.context.view_layer
view_layer.active_layer_collection.collection.objects.link(new_object)

#data_vert_to_blend_vert_map = {}
#verts = g.get_vertices()

#for vert in verts:
#    x = vert.get_x()
#    y = vert.get_y()
#    z = vert.get_z()
#    
#    print(x, y, z)
#    
#    bpy.ops.mesh.primitive_vert_add()
#    bpy.ops.transform.translate(value=(x, y, z), 
#                                orient_type='GLOBAL', 
#                                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
#                                orient_matrix_type='GLOBAL', 
#                                constraint_axis=(False, True, False), 
#                                mirror=True, 
#                                use_proportional_edit=False, 
#                                proportional_edit_falloff='SMOOTH', 
#                                proportional_size=1, 
#                                use_proportional_connected=False, 
#                                use_proportional_projected=False)
#                                
#    vert.set_created()

# deselecting all onf the verticies
#bpy.ops.object.mode_set(mode='EDIT') 
#bpy.ops.mesh.select_mode(type="VERT")
#bpy.ops.mesh.select_all(action='DESELECT')    
#bpy.ops.object.mode_set(mode='OBJECT') 
#obj = bpy.context.active_object

# overiding the context
#override = None
#for area in bpy.context.screen.areas:
#    print(area.type)
#    if area.type == 'VIEW_3D':
#        override = bpy.context.copy()
#        override['space_data'] = area.spaces.active
#        override['area'] = area
#        override['region'] = area.regions[4]
#        override.update(area=area)
#        
#        print(bpy.context.area, override['area'])
#        print(bpy.context.screen, override['screen'])
#        print(bpy.context.window, override['window'])
#        
#        break

#blend_vert_list = list(bpy.context.active_object.data.vertices)

#for v in range(len(blend_vert_list)):
#    print(blend_vert_list[v].co)
#    print(verts[v].get_coordinates())
#    
#    data_vert_to_blend_vert_map[verts[v]] = blend_vert_list[v]
#    
#for vert in verts:
#    print("vert visited pre: {}".format(vert.visited))
#    if not vert.visited:
#        adj_verts = vert.get_adjacent()
#        vert_indx = obj.data.vertices.values().index(data_vert_to_blend_vert_map[vert])
#        bpy.ops.view3d.select_circle(override,
#                                     x=vert.get_x(), 
#                                     y=vert.get_y(), 
#                                     radius=2, 
#                                     wait_for_input=False, 
#                                     mode='SET')        # selecting the vertex
#        time.sleep(2)
#        
#        for adj_v, adj_e in adj_verts:
#            if not adj_e:    # if we don't have an edge
#                adj_idx = obj.data.vertices.values().index(data_vert_to_blend_vert_map[adj_v])
                
#                obj.data.vertices[vert_idx].select=True
#                obj.data.vertices[adj_idx].select=True

#                bpy.ops.view3d.select_circle(override,
#                                             x=adj_v.get_x(), 
#                                             y=adj_v.get_y(), 
#                                             radius=2, 
#                                             wait_for_input=False, 
#                                             mode='ADD')        # selecting the ADJACENT vertex
#                
#                blend_vert = data_vert_to_blend_vert_map[vert]
#                blend_adj_v = data_vert_to_blend_vert_map[adj_v]
#                
#                blend_vert.select = True
#                blend_adj_v.select = True
#                print("Main vert: {}\nAdj vert: {}".format(blend_vert.co, blend_adj_v.co))
#                
#                bpy.ops.mesh.edge_face_add(override)
#                
#                blend_vert.select = False
#                blend_adj_v.select = False
                
#                bpy.ops.view3d.select_circle(override,
#                                             x=adj_v.get_x(), 
#                                             y=adj_v.get_y(), 
#                                             radius=2, 
#                                             wait_for_input=False, 
#                                             mode='SUB')        # deselecting the ADJACENT vertex
                
#                bpy.ops.object.mode_set(mode='EDIT')
#                
#                obj.data.vertices[vert_idx].select=False
#                obj.data.vertices[adj_idx].select=False
#                
#                bpy.ops.object.mode_set(mode='OBJECT')
                
#                vert.set_connected(adj_v)
#                adj_v.set_connected(vert)
#        
#        vert.set_visited
#        print("vert visited post: {}\n".format(vert.visited))
# 
#bpy.ops.object.mode_set(mode='EDIT') 
#bpy.ops.mesh.select_mode(type="VERT")
#bpy.ops.mesh.select_all(action='DESELECT')    
#bpy.ops.object.mode_set(mode='OBJECT')        

#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.edge_face_add()
#bpy.ops.object.editmode_toggle()
#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
