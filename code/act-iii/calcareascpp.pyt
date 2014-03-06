import imp
import os
import re

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Calculate Polygon Areas Toolbox (C++)"
        self.alias = "calcareascpp"

        # List of tool classes associated with this toolbox
        self.tools = [CalcAreaToolCPP]


class CalcAreaToolCPP(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calculate Polygon Area with C++"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        input_layer = arcpy.Parameter(name="in_layer",
                                      displayName="Input Feature Layer",
                                      direction="Input",
                                      datatype="GPFeatureLayer")
        input_layer.filterlist = ["Polygon"]

        new_field = arcpy.Parameter(name="new_field", 
                                    displayName="New Area Field",
                                    direction="Input",
                                    datatype="GPString")

        modified_layer = arcpy.Parameter(name="modified_layer",
                                         displayName="Feature Layer",
                                         direction="Output",
                                         parameterType="Derived",
                                         datatype="GPFeatureLayer")

        params = [input_layer,
                  new_field,
                  modified_layer]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].valueAsText and parameters[1].valueAsText:
            field = arcpy.Field()
            field.name = parameters[1].valueAsText
            field.type = "Double"
            parameters[2].value = parameters[0].valueAsText
            parameters[2].schema.additionalFields = [field]

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        if parameters[0].valueAsText and parameters[1].valueAsText:
            if not re.match("[a-z][a-z0-9_]{0,10}$",
                            parameters[1].valueAsText,
                            re.IGNORECASE):
                err_msg = "Invalid field name {}".format(
                            parameters[1].valueAsText)
                parameters[1].setErrorMessage(err_msg)
            else:
                if (parameters[1].valueAsText.lower() in
                        [f.name.lower()
                         for f in
                            arcpy.ListFields(parameters[0].valueAsText)]):
                    parameters[1].setErrorMessage("Field already exists")

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Make feature layer chainable in model builder
        parameters[2].value = parameters[0].valueAsText
        add_area_field(arcpy.Describe(parameters[0].valueAsText).catalogPath,
                       parameters[1].valueAsText)

def add_area_field(feature_layer, new_field):
    module_info = imp.find_module('field_area_calculator',
                                  [os.path.dirname(__file__)])
    field_area_calculator = imp.load_module('field_area_calculator',
                                            *module_info)
    field_area_calculator.execute_tool(feature_layer, new_field)
