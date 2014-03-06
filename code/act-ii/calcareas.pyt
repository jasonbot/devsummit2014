import re

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Calculate Polygon Areas Toolbox"
        self.alias = "calcareas"

        # List of tool classes associated with this toolbox
        self.tools = [CalcAreaTool]


class CalcAreaTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calculate Polygon Area"
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
        if self.parameters[1].valueAsText:
            if not re.match("[a-z][a-z0-9_]{0,10}$",
                            parameters[1].valueAsText,
                            re.IGNORECASE):
                err_msg = "Invalid field name {}".format(
                            self.parameters[1].valueAsText)
                parameters[1].setErrorMessage(err_msg)

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Make feature layer chainable in model builder
        parameters[2].value = parameters[0].valueAsText
        add_area_field(parameters[0].valueAsText, parameters[1].valueAsText)

def add_area_field(feature_layer, new_field):
    arcpy.AddMessage("Adding field {0}".format(field_name))
    arcpy.management.AddField(feature_layer, new_field,
                              "DOUBLE", "#", "#", "#", "#", "NULLABLE",
                              "NON_REQUIRED", "#")

    arcpy.AddMessage("Calculating value field")
    feature_count = int(arcpy.management.GetCount("Income")[0])    
    arcpy.SetProgressor('step', "Calculating records", 0, feature_count, 1)
    with arcpy.da.UpdateLayer(feature_layer, ["SHAPE@", new_field]) as cur:
        for index, row in enumerate(cur):
            if index % 100 == 0:
                arcpy.SetProgressorPosition(index)
            row[1] = row[0].area
            cur.updateRow(row)
