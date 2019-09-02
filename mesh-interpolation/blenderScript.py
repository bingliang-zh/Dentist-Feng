# blender v2.8.0
import csv
import os
import bpy, bmesh

filename = '2.csv'
# directory = '/home/zeffii/Desktop'  # <-- if you have linux or osx
directory = r'C:\Projects\Dentist-Feng\mesh-interpolation'  # <-- if windows, the r is important
# directory = 'c:/Users/bl/Desktop'  # <-- if windows (alternative)

fullpath = os.path.join(directory, filename)

with open(fullpath, 'r', newline='') as csvfile:
    ofile = csv.reader(csvfile, delimiter=',')
    # next(ofile) # <-- skip the x,y,z header

    # this makes a generator of the remaining non-empty lines
    rows = (r for r in ofile if r)

    # this converts the string representation of each line
    # to an x,y,z list, and stores it in the verts list.
    verts = [[float(i) for i in r] for r in rows]

if verts:
    name = "name"
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.show_name = True
    # Link object to scene
    bpy.context.collection.objects.link(ob)
    # me.from_pydata(verts, [], [])
    # Update mesh with new data
    # me.update()

    bm = bmesh.new()
    bm.from_mesh(me)

    new_column_count = 13
    vertex_list = []

    for vert in verts:
        new_vertex = bm.verts.new((vert[0], vert[1], vert[2]))
        vertex_list.append(new_vertex)

    vertex_list_length = len(vertex_list)

    for i in range(vertex_list_length):
        if (i + 1 + new_column_count < vertex_list_length and (i + 1) % new_column_count != 0):
            bm.faces.new([vertex_list[i], vertex_list[i + 1], vertex_list[i + 1 + new_column_count], vertex_list[i + new_column_count]])

    bm.to_mesh(me)
    bm.free()