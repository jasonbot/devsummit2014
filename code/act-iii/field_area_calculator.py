import ctypes
import os

import arcpy

CALLBACK_C_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.c_int)

class Callback(object):
    def __init__(self, feature_layer):
        self._row_count = int(arcpy.management.GetCount(feature_layer)[0])
        arcpy.SetProgressor('step', "Calculating records", 0,
                            self._row_count, 1)
        self.c_function = CALLBACK_C_PROTOTYPE(self.update)
    def update(self, i):
        arcpy.SetProgressorPosition(i)

def execute_tool(featureclass_path, field_name):

    loaded_dll = ctypes.cdll.LoadLibrary(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "pythoncppdll.dll"))
    calculate_area_field = loaded_dll.AddAreaFieldToFeatureClassCPlusPlus

    calculate_area_field.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p,
                                     CALLBACK_C_PROTOTYPE]
    calculate_area_field.restype = ctypes.c_int

    arcpy.AddMessage("Adding field {0}".format(field_name))
    arcpy.management.AddField(featureclass_path, field_name,
                              "DOUBLE", "#", "#", "#", "#", "NULLABLE",
                              "NON_REQUIRED", "#")

    arcpy.AddMessage("Executing C++ function...")
    callback = Callback(featureclass_path)
    returncode = calculate_area_field(featureclass_path, field_name,
                                      callback.c_function)

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
