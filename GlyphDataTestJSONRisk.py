import bpy
import bmesh
from mathutils import Vector
import csv
import os
import glob
import math
import sys
import json

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
from Material import makeEmissive

from Glyph import Glyph
from Glyph import createGlyph
from Glyph import initGlyph

from KeyTemperature import drawKeyTemperature

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

#--------------------------------------------------------------

text_material = bpy.data.materials.get("Text");
bg_colour = bpy.data.materials.get("BG-Material");

axis_colour = text_material
axis_value_colour = text_material
axis_label_colour = text_material
gridlines_colour = text_material

axes_z = -0.5

x_axis_length = 12.5

start_x = -5.5
end_x = start_x + x_axis_length

y_axis_length = 9.5

start_y = -4.25
end_y = start_y + y_axis_length

x_axis_values = []
y_axis_values = []

properties = None

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
        bpy.ops.object.text_add(location=(-6.0, start_y+(index*increment)-0.125, axes_z));
        txt = bpy.context.object;
        txt.data.body = str(round(y,2));
        txt.data.extrude = 0.02;
        txt.data.size = 0.4;
        txt.data.align_x = 'RIGHT';
        txt.data.materials.append(axis_value_colour);
        
        if(index!=0):
            bpy.ops.mesh.primitive_cube_add(location=(0.7, start_y+(index*increment), axes_z));
            cube = bpy.context.object;
            cube.dimensions = (x_axis_length+0.1,0.01,0.01);
            
            cube.data.materials.append(gridlines_colour);
        else:
            bpy.ops.mesh.primitive_cube_add(location=(0.75, start_y+(index*increment), axes_z));
            cube = bpy.context.object;
            cube.dimensions = (x_axis_length+0.25,0.05,0.01);
            cube.data.materials.append(axis_colour);
        
        index = index + 1;
    
    #axis label    
    bpy.ops.object.text_add(location=(-7.45, 0.0, axes_z));
    txt = bpy.context.object;
    txt.data.body = y_axis_label;
    txt.data.extrude = 0.02;
    txt.data.size = 0.5;
    txt.rotation_euler = (0.0, 0.0, 1.5708);        #radians!
    txt.data.materials.append(axis_label_colour);
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
            
        #x_axis_values.append(max)
        x_axis_values.append(max + inc)
    
    num_items = len(x_axis_values);
    index = 0;
    increment = x_axis_length/(num_items-1);
    
    for x in x_axis_values:    
        bpy.ops.object.text_add(location=(start_x+(index*increment), -5.0, axes_z));
        txt = bpy.context.object;
        txt.data.body = str(round(x,2));
        txt.data.extrude = 0.02;
        txt.data.size = 0.4;
        txt.data.align_x = 'CENTER';
        txt.data.materials.append(axis_value_colour);
        
        if(index!=0):
            bpy.ops.mesh.primitive_cube_add(location=(start_x+(index*increment), 0.45, axes_z));
            cube = bpy.context.object;
            cube.dimensions = (0.01,y_axis_length+0.1,0.01);
            cube.data.materials.append(gridlines_colour);
        else:
            bpy.ops.mesh.primitive_cube_add(location=(start_x+(index*increment), 0.5, axes_z));
            cube = bpy.context.object;
            cube.dimensions = (0.05,y_axis_length+0.25,0.01);
            cube.data.materials.append(axis_colour);
        
        index = index + 1;
    
    #axis label    
    bpy.ops.object.text_add(location=(0, -5.5, axes_z));
    txt = bpy.context.object;
    txt.data.body = x_axis_label;
    txt.data.extrude = 0.02;
    txt.data.size = 0.5;
    txt.data.materials.append(axis_label_colour);
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

##----------------------------------------- Code from here

# LOAD JSON DATA
argv = sys.argv             
argv = argv[argv.index("--") + 1:]  # get all args after "--"

j_data = json.loads(argv[0])
values = j_data["data"]

# LOAD PROPERTIES JSON
with open("properties.json", 'r') as props:
    properties = json.load(props)
    
ax_col = properties["properties"]["axis_colour"]
axis_colour = makeEmissive((ax_col[0], ax_col[1], ax_col[2], ax_col[3]), 'AxisMaterial')
axis_colour = bpy.data.materials['AxisMaterial']

tx_col = properties["properties"]["axis_value_colour"]
axis_value_colour = makeEmissive((tx_col[0], tx_col[1], tx_col[2], tx_col[3]), 'AxisValueMaterial')
axis_value_colour = bpy.data.materials['AxisValueMaterial']

ax_col = properties["properties"]["axis_label_colour"]
axis_label_colour = makeEmissive((ax_col[0], ax_col[1], ax_col[2], ax_col[3]), 'AxisLabelMaterial')
axis_label_colour = bpy.data.materials['AxisLabelMaterial']

gx_col = properties["properties"]["gridlines_colour"]
gridlines_colour = makeEmissive((gx_col[0], gx_col[1], gx_col[2], gx_col[3]), 'GridlinesMaterial')
gridlines_colour = bpy.data.materials['GridlinesMaterial']

bg_col = properties["properties"]["background_colour"]      # Background Colour
bg_colour = makeEmissive((bg_col[0], bg_col[1], bg_col[2], bg_col[3]), 'New-BG-Material')
bg_colour = bpy.data.materials['New-BG-Material']

bpy.data.objects["Plane"].data.materials[0] = bg_colour         
bpy.data.objects["Plane.001"].data.materials[0] = bg_colour
bpy.data.objects["Plane.002"].data.materials[0] = bg_colour

bpy.data.objects["Least.U.TXT"].data.materials[0] = axis_label_colour
bpy.data.objects["Most.U.TXT"].data.materials[0] = axis_label_colour
bpy.data.objects["No.Data.TXT"].data.materials[0] = axis_label_colour
bpy.data.objects["Uncertainty.TXT"].data.materials[0] = axis_label_colour
bpy.data.objects["KeyTitle.TXT"].data.materials[0] = axis_label_colour

key_label = j_data["key_name"]
key_low = j_data["key_values"]["low_value"]
key_high = j_data["key_values"]["high_value"]

key_low = key_low.replace(' ', '\n')
key_high = key_high.replace(' ', '\n')

bpy.data.objects["Uncertainty.TXT"].data.body = key_label
bpy.data.objects["Least.U.TXT"].data.body = key_low
bpy.data.objects["Most.U.TXT"].data.body = key_high
bpy.data.objects["KeyTitle.TXT"].data.body = "Temperature"

# ---------------------------------------------------------------
print("Num Glyphs: " + str(len(values)))

min_risk = None
max_risk = None

for idx in range(0, len(values)) :    
    datavalues = values[idx]
    
    d_x = float(datavalues["x"])
    d_y = float(datavalues["y"])
    
    if (min_x == None or d_x < min_x):
        min_x = d_x
    if (max_x == None or d_x > max_x):
        max_x = d_x
    
    if (min_y == None or d_y < min_y):
        min_y = d_y
    if (max_y == None or d_y > max_y):
        max_y = d_y
        
    d_r = float(datavalues["r"])
    if (min_risk == None or min_risk > d_r):
        min_risk = d_r
    if (max_risk == None or max_risk < d_r):
        max_risk = d_r  
    
x_inc = (max_x - min_x)/10.0
y_inc = (max_y - min_y)/8.0

#------------------------------------------------------------------------------------------------------------------- RENDER

drawXAxis(min_x, max_x, x_inc, j_data["x_axis"])
drawYAxis(min_y, max_y, y_inc, j_data["y_axis"])

drawKeyTemperature(0.0 , ortho, axis_value_colour)

for idx in range(0, len(values)) :    
    datavalues = values[idx]
    
    d_x = float(datavalues["x"])
    d_y = float(datavalues["y"])
    d_uncertainty = float(datavalues["u"])
    d_temperature = float(datavalues["v"])
    d_risk = float(datavalues["r"])
    
    risk_range = max_risk - min_risk
    
    if (risk_range <= 0):
        risk_val = d_risk
    else:
        risk_val = (d_risk - min_risk) / risk_range
    
    p_x = start_x + ((d_x - x_axis_values[0]) * (x_axis_length / (x_axis_values[len(x_axis_values)-1] - x_axis_values[0])))
    p_y = start_y + ((d_y - y_axis_values[0]) * (y_axis_length / (y_axis_values[len(y_axis_values)-1] - y_axis_values[0])))
    
    scale = 0.5 + (risk_val * 0.5)
    
    glyph = initGlyph(d_uncertainty, 1, p_x, p_y, 1.0, scale, d_temperature, "data-glyph-"+str(idx), force=True) 
    createGlyph( glyph, minVariance, maxVariance, ortho, numGlyphs )
