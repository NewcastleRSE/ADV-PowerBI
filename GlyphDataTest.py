import bpy
import bmesh
from mathutils import Vector
import csv
import os
import glob
import math
import sys

from random import *

# code to help Blender find local python modules
filepath = bpy.data.filepath
dir = os.path.dirname(filepath)

if not dir in sys.path:
   sys.path.append(dir)
      
dir = dir+'\Glyphs' # point to glyph code directory
if not dir in sys.path:
   sys.path.append(dir)
#----------------------------------------

from Material import makeFlatColor
from Glyph import Glyph
from Glyph import createGlyph
from Glyph import initGlyph

# Detect current working directory -------
currentDir = os.path.dirname(__file__)
strs = currentDir.split("\\")

if ".blend" in strs[len(strs)-1]:
    currentDir = ""
    x = 0
    for strng in strs:
        currentDir = currentDir + strng
        currentDir = currentDir + "\\"
        x = x + 1
        
        if x == (len(strs) - 1):
            break

os.chdir( currentDir )
print( os.getcwd() )

##-----------------------------------------

#
# Code from here
# This code generates a number of glyphs with a single min uncertainty glyph
#

#
# Make some materials to use.
#

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

#print ("values: " + argv[0])

values = argv[0]
values = values.split(';')

#--------------------------------------------------------------

text_material = bpy.data.materials.get("Text");

axes_z = -0.5

x_axis_length = 12.5

start_x = -5.5
end_x = start_x + x_axis_length

y_axis_length = 9.5

start_y = -4.2
end_y = start_y + y_axis_length

x_axis_values = [];
y_axis_values = [];

def drawYAxis(min, max, inc, y_axis_label):
    idx = min;
       
    if (inc==0.0):
        y_axis_values.append(min-1)
        y_axis_values.append(min)
        y_axis_values.append(min+1)
    else:
        y_axis_values.append(min - inc)
        
        while idx <= max:
            y_axis_values.append(idx);
            idx += inc;
        
        #y_axis_values.append(max)
        y_axis_values.append(max + inc)
    
    num_items = len(y_axis_values);
    index = 0;
    increment = y_axis_length/(num_items-1);
    
    for y in y_axis_values:    
        bpy.ops.object.text_add(location=(-6.0, start_y+(index*increment)-0.175, axes_z));
        txt = bpy.context.object;
        txt.data.body = str(round(y,2));
        txt.data.extrude = 0.02;
        txt.data.size = 0.5;
        txt.data.align_x = 'RIGHT';
        txt.data.materials.append(text_material);
        
        if(index!=0):
            bpy.ops.mesh.primitive_cube_add(location=(0.75, start_y+(index*increment), axes_z));
            cube = bpy.context.object;
            cube.dimensions = (x_axis_length,0.01,0.01);
            cube.data.materials.append(text_material);
        else:
            bpy.ops.mesh.primitive_cube_add(location=(0.75, start_y+(index*increment), axes_z));
            cube = bpy.context.object;
            cube.dimensions = (x_axis_length,0.05,0.01);
            cube.data.materials.append(text_material);
        
        index = index + 1;
    
    #axis label    
    bpy.ops.object.text_add(location=(-7.45, 0.0, axes_z));
    txt = bpy.context.object;
    txt.data.body = y_axis_label;
    txt.data.extrude = 0.02;
    txt.data.size = 0.5;
    txt.rotation_euler = (0.0, 0.0, 1.5708);        #radians!
    txt.data.materials.append(text_material);
    txt.data.align_x = 'CENTER';

def drawXAxis(min, max, inc, x_axis_label):
    idx = min;
    
    if (inc==0.0):
        x_axis_values.append(min-1)
        x_axis_values.append(min)
        x_axis_values.append(min+1)
    else:
        x_axis_values.append(min - inc)
        
        while idx <= max:
            x_axis_values.append(idx);
            idx += inc;
            
        x_axis_values.append(max)
        x_axis_values.append(max + inc)
    
    num_items = len(x_axis_values);
    index = 0;
    increment = x_axis_length/(num_items-1);
    
    for x in x_axis_values:    
        bpy.ops.object.text_add(location=(start_x+(index*increment), -5.0, axes_z));
        txt = bpy.context.object;
        txt.data.body = str(round(x,2));
        txt.data.extrude = 0.02;
        txt.data.size = 0.5;
        txt.data.align_x = 'CENTER';
        txt.data.materials.append(text_material);
        
        if(index!=0):
            bpy.ops.mesh.primitive_cube_add(location=(start_x+(index*increment), 0.5, axes_z));
            cube = bpy.context.object;
            cube.dimensions = (0.01,y_axis_length,0.01);
            cube.data.materials.append(text_material);
        else:
            bpy.ops.mesh.primitive_cube_add(location=(start_x+(index*increment), 0.5, axes_z));
            cube = bpy.context.object;
            cube.dimensions = (0.05,y_axis_length,0.01);
            cube.data.materials.append(text_material);
        
        index = index + 1;
    
    #axis label    
    bpy.ops.object.text_add(location=(0, -5.5, axes_z));
    txt = bpy.context.object;
    txt.data.body = x_axis_label;
    txt.data.extrude = 0.02;
    txt.data.size = 0.5;
    txt.data.materials.append(text_material);
    txt.data.align_x = 'CENTER';
    txt.data.align_y = 'CENTER';

minVariance = 0.0
maxVariance = 1.0

ortho = True

numGlyphs = 7

min_x = None
max_x = None 
min_y = None
max_y = None

print("Do Prep Axes")

print("Num Glyphs: " + str(len(values)-1))

for idx in range(0, len(values)-1) :    
    datavalues = values[idx].split(',')
    
    #print("values[0]: " + datavalues[0])
    #print("values[1]: " + datavalues[1])
    
    d_x = round(float(datavalues[0]), 2)
    d_y = round(float(datavalues[1]), 2)
    
    if (min_x == None or d_x < min_x):
        min_x = d_x
    if (max_x == None or d_x > max_x):
        max_x = d_x
    
    if (min_y == None or d_y < min_y):
        min_y = d_y
    if (max_y == None or d_y > max_y):
        max_y = d_y

print("Do Draw Axes")
    
x_inc = round((max_x - min_x)/10.0, 2)
y_inc = round((max_y - min_y)/10.0, 2)

print("Do Draw X Axis: " + str(min_x) + ", " + str(max_x) + ", " + str(x_inc))   
drawXAxis(min_x, max_x, x_inc, "x_axis")

print("Do Draw Y Axis")
drawYAxis(min_y, max_y, y_inc, "y_axis")

print("Do Draw Glyphs")

for idx in range(0, len(values)-1) :    
    datavalues = values[idx].split(',')
    
    d_x = float(datavalues[0])
    d_y = float(datavalues[1])
    d_uncertainty = float(datavalues[2])
    d_temperature = float(datavalues[3])
    
    p_x = d_x #start_x + ((x_axis_length/(len(values))) * d_x)
    
    #p_y = start_y + ((y_axis_length/(len(values))) * d_y)
    p_x = start_x + ((d_x - x_axis_values[0]) * (x_axis_length / (x_axis_values[len(x_axis_values)-1] - x_axis_values[0])))
    p_y = start_y + ((d_y - y_axis_values[0]) * (y_axis_length / (y_axis_values[len(y_axis_values)-1] - y_axis_values[0])))
    
    glyph = initGlyph(d_uncertainty, 1, p_x, p_y, 1.0, 0.5, d_temperature, "data-glyph-"+str(idx), force=True) 
    createGlyph( glyph, minVariance, maxVariance, ortho, numGlyphs )

