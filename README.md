# ADV-PowerBI
Visualising Uncertainty in Power BI using Blender

Project: Automating Data Visualisation (Turing)  
PI: [Nick Holliman](https://www.ncl.ac.uk/computing/people/profile/nickholliman.html)  
RSE(s): [Mike Simpson](https://www.ncl.ac.uk/digitalinstitute/staff/profile/mikesimpson.html)    

## Blend Files 
The projects that use the city model will require the .blend file to be downloaded from AWS (as they are too big to store on GitHub).

https://turing-vis-blender.s3.eu-west-2.amazonaws.com/blend+files/CityModel.blend

## Notes
There are two Power BI files in the repository, one contains some test python code (examples of how to use matplotlib/seaborn to draw Power BI graphs) and the second contains the Blender code.

## Instructions
Currently, there are some hard-coded links in the files, these will need to be updated for the scripts to work. The "blender_test.pbix" visualisations include a coded "filepath" variable, which currently points at "D:\Projects\ADV-PowerBI". This needs to be changed to point at the directory into which the files have been downloaded.

## Installation
The scripts will only work if the following are installed on your PC:

(Python and PIP are required)

Run the following commands:<br />
`py -m pip install pandas` <br />
`py -m pip install matplotlib` <br />

Seaborn is required for some of the test python IMD visualisations:  

`py -m pip install seaborn` <br />

This should install all the required dependencies. 

Blender will need to be installed and added to the path.

## Testing
The following can be copy-pasted to the command line to generate an image from the blend file using some sample JSON data, if the PowerBI interface is not working. This could alsop be used to test whether the blender scripts are working correcntly.

`blender "D:\Projects\ADV-PowerBI\GlyphsTest.blend" --background -noaudio --use-extension 1 --python "D:\Projects\ADV-PowerBI\GlyphDataTestJSONRisk.py" --engine BLENDER_EEVEE --render-output //glyph_json_risk_# -F PNG --render-frame 1 -- "{\"key_name\":\"Uncertainty\",\"key_values\":{\"high_value\":\"Most Uncertain\",\"low_value\":\"Least Uncertain\"},\"x_axis\":\"x\",\"y_axis\":\"y\",\"data\":[{\"x\":-6.0,\"y\":2.2,\"u\":0.0,\"v\":-28.0,\"r\":0.0},{\"x\":-4.0,\"y\":1.8,\"u\":0.14,\"v\":-20.0,\"r\":0.1},{\"x\":-2.0,\"y\":1.4,\"u\":0.28,\"v\":-12.0,\"r\":0.2},{\"x\":-0.1,\"y\":-1.0,\"u\":-1.0,\"v\":28.0,\"r\":1.0},{\"x\":0.1,\"y\":1.0,\"u\":0.42,\"v\":-4.0,\"r\":0.4},{\"x\":2.0,\"y\":0.6,\"u\":0.56,\"v\":4.0,\"r\":0.5},{\"x\":4.0,\"y\":0.2,\"u\":0.7,\"v\":12.0,\"r\":0.6},{\"x\":6.0,\"y\":-0.2,\"u\":0.84,\"v\":20.0,\"r\":0.8}]}"`
