# ADV-PowerBI
Visualising Uncertainty in Power BI using Blender

Project: Automating Data Visualisation (Turing)  
PI: [Nick Holliman](https://www.ncl.ac.uk/computing/people/profile/nickholliman.html)  
RSE(s): [Mike Simpson](https://www.ncl.ac.uk/digitalinstitute/staff/profile/mikesimpson.html)    

## Instructions
Script.py contains code that can be copy-pasted into the Python window in PowerBI when you add a Python Visualisation to your Power BI Page. 
* The top section of the file includes a coded "filepath" variable, which currently points at "D:\Projects\ADV-PowerBI". This needs to be changed to point at the directory into which the files have been downloaded. 
* This section also includes all variable information, which will have to be updated to refer to the columns/fields of the specific dataset that you are working with.
* This section also contains the 'format' of the visualisation, which allows you to select betweeen "graph", which is a simple scatter plot, and "map" which uses the 3D Model as a backdrop (if using latitute and longitude data).

## Notes
There is a Power BI file in the repository, which contains some examples of how the code has been adapted to work with several different datasets.

## Installation
The scripts will only work if the following are installed on your PC:

(Python and PIP are required)

Run the following commands:<br />
`py -m pip install pandas` <br />
`py -m pip install matplotlib` <br />

Blender will need to be installed and added to the path.

## Testing & Debugging
If you comment out the code on line 50 of the file (#raise Exception(callStr)), this will throw a Power BI exception with the string that you can then use from the command line to see the printouts from Blender and the other Python scripts. (It will be in the same format as the command below.)

Alternatively, the following can be copy-pasted to the command line to generate an image from the blend file using some sample JSON data, if the PowerBI interface is not working. This could also be used to test whether the blender scripts are working correcntly.

`blender "D:\Projects\ADV-PowerBI//CityModel.blend" --background -noaudio --use-extension 1 --python "D:\Projects\ADV-PowerBI//GlyphDataTest.py" -E BLENDER_EEVEE --render-output //glyph_json_latlon_# -F PNG --render-frame 1 -- "{\"key_name\":\"Uncertainty\",\"key_values\":{\"high_value\":\"Most Uncertain\",\"low_value\":\"Least Uncertain\"},\"x_axis\":\"lat\",\"y_axis\":\"lon\",\"background\":\"map\",\"data\":[{\"x\":-1.625430832,\"y\":54.97204714,\"u\":-1.0,\"v\":28.0,\"r\":1.0},{\"x\":-1.627724051,\"y\":54.97238667,\"u\":0.0,\"v\":-28.0,\"r\":0.0},{\"x\":-1.6246465140000002,\"y\":54.97239519,\"u\":0.42,\"v\":-4.0,\"r\":0.4},{\"x\":-1.6236904330000002,\"y\":54.97273372,\"u\":0.7,\"v\":12.0,\"r\":0.6},{\"x\":-1.6247964480000001,\"y\":54.97306962,\"u\":0.56,\"v\":4.0,\"r\":0.5},{\"x\":-1.6260928590000001,\"y\":54.97309159,\"u\":0.28,\"v\":-12.0,\"r\":0.2},{\"x\":-1.624197719,\"y\":54.97361594,\"u\":0.84,\"v\":20.0,\"r\":0.8},{\"x\":-1.626982,\"y\":54.973636,\"u\":0.14,\"v\":-20.0,\"r\":0.1}]}"`
