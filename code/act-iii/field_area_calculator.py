import ctypes
import os

import arcpy

def execute_tool(featureclass_path, field_name):
    loaded_dll = ctypes.cdll.LoadLibrary(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "pythoncppdll.dll"))
    calculate_area_field = loaded_dll.AddAreaFieldToFeatureClassCPlusPlus

    calculate_area_field.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
    calculate_area_field.restype = ctypes.c_int

    arcpy.AddMessage("Adding field {0}".format(field_name))
    arcpy.management.AddField(featureclass_path, field_name,
                              "DOUBLE", "#", "#", "#", "#", "NULLABLE",
                              "NON_REQUIRED", "#")

    arcpy.AddMessage("Executing C++ function...")
    returncode = calculate_area_field(featureclass_path, field_name)

    if returncode == -1:
        arcpy.AddError("Error opening Feature Class")
    elif returncode == -2:
        arcpy.AddError("Field does not exist on Feature Class")
    elif returncode == -3:
        arcpy.AddError("Shape field is not Polygon")
    elif returncode == -4:
        arcpy.AddError("Function Error")
    elif returncode == 0:
        arcpy.AddMessage("Computed value")
    else:
        arcpy.AddError("Unknown failure")
