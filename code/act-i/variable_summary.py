import os
import re
import sys
import subprocess
import tempfile
import _winreg

import arcpy

class TempShapefile(object):
    def __init__(self, featureclass):
        self._fcname = featureclass
        self._shapefilename = None
        self._spatial_reference_string = (arcpy.SpatialReference("WGS 1984")
                                               .exportToString())
    def __enter__(self):
        if self._shapefilename:
            raise RuntimeError("Already have a temporary shapefile!")
        self._shapefilename = tempfile.mktemp('.shp')
        arcpy.AddMessage(
                "Creating temporary shapefile as {0}".format(
                    self._shapefilename))
        arcpy.management.Project(self._fcname,
                                 self._shapefilename,
                                 self._spatial_reference_string)
        return self._shapefilename
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._shapefilename and arcpy.Exists(self._shapefilename):
            arcpy.AddMessage(
                    "Deleting temporary shapefile".format(self._shapefilename))
            arcpy.management.Delete(self._shapefilename)
        self._shapefilename = None

def find_r_executable():
    handle = None
    try:
        handle =_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\R-Core\R")
        i = 0
        while True:
            key, value, _ = _winreg.EnumValue(handle, i)
            if key.lower() == "installpath":
                r_executable_path = os.path.join(value, "bin", "R.exe")
                return r_executable_path
            i + = 1
    finally:
        if handle is not None:
            _winreg.CloseKey(handle)

def variable_summary(feature_class_path, variable_name):
    # Use a context manager to make sure we have a shapefile to work with
    with TempShapefile(feature_class_path) as shapefile_path:
        # Assemble command line
        r_exe = find_r_executable()
        arcpy.AddMessage("Found R.exe at {}".format(r_exe))
        commandlineargs = [r_exe,
                           '--slave',
                           '--vanilla',
                           '--args',
                           shapefile_path,
                           variable_name]

        # Locate and read R input script
        rscriptname = os.path.join(os.path.abspath(
                                        os.path.dirname(__file__)),
                                   "variable_summary.r")
        scriptsource = open(rscriptname, 'rb')

        # Open R and feed it the script
        rprocess = subprocess.Popen(commandlineargs,
                                    stdin=scriptsource,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)

        # Grab the output written to stdout/stderr
        stdoutstring, stderrstring = rprocess.communicate()

        # Push output to messages window
        if stderrstring and "Calculations Complete..." not in stdoutstring:
            arcpy.AddError(stderrstring)
        else:
            # Just grab the tables
            table_string = ('\[1\] "Begin Calculations[.]{4}"\n(.*)\n'
                            '\[1\] "Calculations Complete[.]{3}"')
            tables = re.findall(table_string,
                                stdoutstring.replace('\r', ''),
                                re.DOTALL)
            # Push to output window
            arcpy.AddMessage(" ")
            arcpy.AddMessage("\n".join(tables))
            arcpy.AddMessage(" ")

if __name__ == '__main__':
    test = variable_summary(arcpy.GetParameterAsText(0),
                            arcpy.GetParameterAsText(1))
