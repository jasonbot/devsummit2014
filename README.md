Accessing C Type Libraries with Python Script Tools
==========

Synopsis (from the [Dev Summit 2014 Agenda](http://www.esri.com/events/devsummit/agenda))
----

This session will provide an overview of integrating external executable tools and high-performance in-process C/C++ native code from Python using the Python standard library and the Python APIs.

Agenda
----

This presentation will cover using Python's built-in libraries to integrate code, both as command-line utilities written in any language as well as high performance, in-process native code written in C or C++.

* Starting point with Script Tools
* Wrapping a command line utility as a script tool
  * Using subprocess
  * Using the script to do setup/teardown for the external tool
* Writing C++ ArcObjects code
  * Introduction to CTypes
  * Putting what we learned from wrapping into practice on in-process code

Demos Etc.
----
The recorded video demos and the compiled DLL (along with all the code as it was presented) [is available as a binary release on this project](https://github.com/jasonbot/devsummit2014/releases).

Useful Links
----
[Extending Geoprocessing through Python Modules](http://blogs.esri.com/esri/arcgis/2013/08/13/extending-geoprocessing-through-python-modules/)

[Getting started with ArcObjects and `comtypes`](http://www.pierssen.com/arcgis/upload/misc/python_arcobjects.pdf)

[Programming Against ArcObjects in C++](http://resources.arcgis.com/en/help/arcobjects-cpp/conceptualhelp/index.html#/Programming_against_ArcObjects_with_C/000100000058000000/)
