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
