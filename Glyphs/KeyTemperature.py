import bpy
import os
import sys

# code to help Blender find local python modules
filepath = bpy.data.filepath
dir = os.path.dirname(filepath)
if not dir in sys.path:
   sys.path.append(dir)
      
dir = dir+'\..\Glyphs' # point to glyph code directory
if not dir in sys.path:
   sys.path.append(dir)
#----------------------------------------

from MetOffice import metOfficeLimits
from MetOffice import metOfficeColours

from Glyph import Glyph
from Glyph import createGlyph
from Glyph import initGlyph

from Glyph import Glyph
from Glyph import createGlyph
from Glyph import initGlyph

#
# Code from here
#

def drawKeyTemperature(average, ortho):

    # copy camera collection    
    cam_x = bpy.context.scene.camera.location[0]
    cam_y = bpy.context.scene.camera.location[1]
    
    # init variables
    atX = cam_x -3.05
    atY =  cam_y + 1.4
    atZ =  1.4
    temp = 30
    r = 0.05
    
    maxY = atY
    text_material = bpy.data.materials.get("NewWhiteEmissive");

    # add objects into corect colection
    scene_collection = bpy.context.view_layer.layer_collection.children['TempScale']
    bpy.context.view_layer.active_layer_collection = scene_collection    

    # loop    
    for x in range(1,22) :    
        name = "Temp" + str(temp)
        
        glyph = initGlyph(0.0, 10, atX, atY, 0.1, r, temp, name, True)
        createGlyph( glyph, 0.0, 1.0, ortho,1)    
        
        bpy.ops.object.text_add(location=(atX, atY, atZ));
        txt = bpy.context.object;
        txt.data.body = str(temp);
        txt.data.extrude = 0.02;
        txt.data.size = 0.1;
        txt.data.materials.append(text_material);
        txt.data.align_x = 'RIGHT';
        txt.data.align_y = 'CENTER';
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY');
        txt.location=(atX + 0.17, atY, atZ);
        
        atY =  atY - 0.15
        temp -= 2
        
    minY = atY + 0.2
    
    print("MinY: " + str(minY))
    print("MaxY: " + str(maxY))
    
    minTemp = -10
    maxTemp =  30
    
    avgY = minY + ((average - minTemp) * ((maxY - minY) / (maxTemp - minTemp)))
    
    print ("AvgY: " + str(avgY))
    
    #draw average cone and label    
    text_material = bpy.data.materials.get("NewWhiteEmissive");
    
    atX = cam_x -2.72
    atY = avgY
    
    bpy.ops.mesh.primitive_cone_add(location=(atX,atY,atZ), radius1 = 0.04, radius2 = 0.0, depth = 0.1, rotation=(0.0,-1.5708,0.0))
    cone = bpy.context.object;
    cone.data.materials.append(text_material);
    cone.location=(atX, atY, atZ);
    
    bpy.ops.object.text_add(location=(atX, atY, atZ));
    txt = bpy.context.object;
    txt.data.body = "Average\n("+"{0:.1f}".format(average)+")";
    txt.data.extrude = 0.02;
    txt.data.size = 0.075;
    txt.data.materials.append(text_material);
    txt.data.align_x = 'LEFT';
    txt.data.align_y = 'CENTER';
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY');
    txt.location=(atX + 0.2, atY, atZ);    
        
#for testing
#drawKeyTemperature(11.4, True)