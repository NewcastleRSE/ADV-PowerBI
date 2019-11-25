# ADV-PowerBI
Visualising Uncertainty in Power BI using Blender

Project: Automating Data Visualisation (Turing)
PI: [Nick Holliman](https://www.ncl.ac.uk/computing/people/profile/nickholliman.html)
RSE(s): [Mike Simpson](https://www.ncl.ac.uk/digitalinstitute/staff/profile/mikesimpson.html)  

## Instructions
Currently, there are some hard-coded links in the files, these will need to be updated for the scripts to work. Most currently point at "D:\Projects\ADV-PowerBI\"

## Installation
The scripts will only work if the following are installed on your PC:

(Python and PIP are required)

Run the following commands:<br />
`py -m pip install pandas` <br />
`py -m pip install matplotlib` <br />
`py -m pip install seaborn` <br />

This should install all the required dependencies. 

Blender will need to be installed and added to the path.

## Testing
The following can be copy-pasted to the command line to generate an image from the blend file using some sample JSON data, if the PowerBI interface is not working. This could alsop be used to test whether the blender scripts are working correcntly.

`blender "D:\Projects\ADV-PowerBI\GlyphsTest.blend" --background -noaudio --use-extension 1 --python "D:\Projects\ADV-PowerBI\GlyphDataTestJSONRisk.py" --engine BLENDER_EEVEE --render-output //glyph_json_risk_# -F PNG --render-frame 1 -- "{\"key_name\":\"Uncertainty\",\"key_values\":{\"high_value\":\"Most Uncertain\",\"low_value\":\"Least Uncertain\"},\"x_axis\":\"x\",\"y_axis\":\"y\",\"data\":[{\"x\":-6.0,\"y\":2.2,\"u\":0.0,\"v\":-28.0,\"r\":0.0},{\"x\":-4.0,\"y\":1.8,\"u\":0.14,\"v\":-20.0,\"r\":0.1},{\"x\":-2.0,\"y\":1.4,\"u\":0.28,\"v\":-12.0,\"r\":0.2},{\"x\":-0.1,\"y\":-1.0,\"u\":-1.0,\"v\":28.0,\"r\":1.0},{\"x\":0.1,\"y\":1.0,\"u\":0.42,\"v\":-4.0,\"r\":0.4},{\"x\":2.0,\"y\":0.6,\"u\":0.56,\"v\":4.0,\"r\":0.5},{\"x\":4.0,\"y\":0.2,\"u\":0.7,\"v\":12.0,\"r\":0.6},{\"x\":6.0,\"y\":-0.2,\"u\":0.84,\"v\":20.0,\"r\":0.8}]}"`
