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

print ("values: " + argv[0])

values = argv[0]
values = values.split(',')

minVariance = 0.0
maxVariance = 1.0

ortho = True

numGlyphs = 7

atX = -7.5
atY = 1.5

vrnce = 0.0

for idx in range(0,numGlyphs) :
    #mat = Morange
    #createGlyph( fname, atX, atY, mat)
    
    glyph = initGlyph(vrnce, 1, atX, atY, 1.0, 1.0, float(values[idx]), "data-glyph-"+str(idx), force=True) 
    createGlyph( glyph, minVariance, maxVariance, ortho, numGlyphs )
    
    atX =  atX + 2.5
    vrnce = vrnce + ((maxVariance / numGlyphs) - 0.01)

#
# NoVar Glyph (should be last alphabetically)
#
atX = -0.0
atY = -1.5
vrnce = -1

glyph = initGlyph(vrnce, 1, atX, atY, 1.0, 1.0, float(values[idx]), "data-glyph-x", force=True) 
createGlyph( glyph, minVariance, maxVariance, ortho, numGlyphs )