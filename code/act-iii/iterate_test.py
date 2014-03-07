"""Example of a very simple test script you can use to debug your C++ code in
   Visual Studio. Run this script from the command line (assuming you have
   copied a shapefile named tet.shp in this folder) and attach to the process
   from Visual Studio.
"""

import os

import arcpy

import field_area_calculator

if __name__ == "__main__":
    raw_input("Attach to python.exe (PID {}) and press enter>".format(os.getpid()))

    shape_path = os.path.join(os.path.dirname(__file__), "test.shp")

    try:
        arcpy.management.DeleteField(shape_path, "pyfld")
        print "Deleted field."
    except:
        pass

    field_area_calculator.execute_tool(shape_path, "pyfld", True)
