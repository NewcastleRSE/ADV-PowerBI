# In Power BI, create a Python Visualisation ('Py' Symbol) then
# copy and pase the following where it says "Paste or type your script code here:"
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
import subprocess
import json

# ----------------------------- Variables Here

filepath = "D:\Projects\ADV-PowerBI"

format = "graph" 			 # "graph" or "map"

x_data = dataset.x
y_data = dataset.y
value_data = dataset.temperature
uncertainty_data = dataset.uncertainty
risk_data = dataset.risk

x_axis_label = dataset.columns[0]
y_axis_label = dataset.columns[1]

# ----------------------------- Code from Here

json_data = {
    'key_name' : "Uncertainty",
    'key_values' : { 
        'high_value' : "Most Uncertain", 
        'low_value' : "Least Uncertain" 
        },
    'x_axis_label' : x_axis_label,
    'y_axis_label' : y_axis_label,
    'background' : format,
    'data' : []
}

idx = 0

for x in value_data:    
    j_data = { 'x': float(x_data[idx]), 'y': float(y_data[idx]), 'u': float(uncertainty_data[idx]), 'v': float(value_data[idx]), 'r': float(risk_data[idx]) }
    json_data['data'].append(j_data)
    
    idx = idx + 1

json_str = json.dumps(json_data, separators=(',', ':'))
json_str = json_str.replace('\"', '\\"')

callStr = "blender \"" + filepath + "//CityModel.blend\" --background -noaudio --use-extension 1 --python \"" + filepath + "//GlyphDataTest.py\" --engine BLENDER_EEVEE --render-output //glyph_json_risk_# -F PNG --render-frame 1 -- " + "\"" + json_str + "\""

#raise Exception(callStr)

return_code = subprocess.call(callStr, shell=True)

img = mpimg.imread(filepath + '//glyph_json_risk_1.png') 
plt.imshow(img)
plt.axis('off')
plt.show()
