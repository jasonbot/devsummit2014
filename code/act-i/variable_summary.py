import arcpy 
import os
import re
import sys
import subprocess
import tempfile

class TempShapefile(object):
    def __init__(self, featureclass):
        self._fcname = featureclass
        self._shapefilename = None
        self._spatial_reference_string = arcpy.SpatialReference("WGS 1984").exportToString()
    def __enter__(self):
        if self._shapefilename:
            raise RuntimeError("Already have a temporary shapefile!")
        self._shapefilename = tempfile.mktemp('.shp')
        arcpy.AddMessage("Creating temporary shapefile as {0}".format(self._shapefilename))
        arcpy.management.Project(self._fcname, self._shapefilename, self._spatial_reference_string)
        return self._shapefilename
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._shapefilename and arcpy.Exists(self._shapefilename):
            arcpy.AddMessage("Deleting temporary shapefile...".format(self._shapefilename))
            arcpy.management.Delete(self._shapefilename)
        self._shapefilename = None

def variable_summary(feature_class_path):
    # Use a context manager to make sure we have a shapefile to work with
    with TempShapefile(feature_class_path) as shapefile_path:
        # Assemble command line
        commandlineargs = ['R', '--slave', '--vanilla', '--args',
                           shapefile_path,
                           str(arcpy.GetParameterAsText(1))]

        # Locate and read R input script
        rscriptname = os.path.join(os.path.abspath(
                                        os.path.dirname(__file__)),
                                    "VarSummary.r")
        scriptsource = open(rscriptname, 'rb')

        # Open R and feed it the script
        rprocess = subprocess.Popen(commandlineargs,
                                    stdin=scriptsource,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)

        # Grab the printed output
        stdoutstring, stderrstring = rprocess.communicate()

        # Push output to messages window
        if stderrstring and "Calculations Complete..." not in stdoutstring:
            arcpy.AddError(stderrstring)
        else:
            # Just grab the tables
            tables = re.findall('\[1\] "Begin Calculations[.]{4}"\n(.*)\n\[1\] "Calculations Complete[.]{3}"',
                                stdoutstring.replace('\r', ''),
                                re.DOTALL)
            # Push to output window
            arcpy.AddMessage(" ")
            arcpy.AddMessage("\n".join(tables))
            arcpy.AddMessage(" ")

if __name__ == '__main__':
    test = variable_summary(arcpy.GetParameterAsText(0)) 
