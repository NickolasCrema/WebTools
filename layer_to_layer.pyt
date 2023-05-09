# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        pinput = arcpy.Parameter(
            name='input',
            displayName='Input Feature',
            direction='Input',
            parameterType='Required',
            datatype='GPFeatureRecordSetLayer'
        )
        output = arcpy.Parameter(
            name="output", 
            displayName="Output File", 
            direction="Output", 
            parameterType="Derived", 
            datatype="DEFeatureClass"
        )
        params = [pinput, output]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        layer = parameters[0].value

        new = arcpy.management.CreateFeatureclass(arcpy.env.scratchGDB, 'output', 'POLYLINE', spatial_reference=arcpy.Describe(layer).spatialReference)
        
        new_cursor = arcpy.da.InsertCursor(new, ['SHAPE@'])

        layer_cursor = arcpy.da.SearchCursor(layer, ['SHAPE@'])

        for row in layer_cursor:
            new_cursor.insertRow(row)
        
        del new_cursor
        del layer_cursor
        
        arcpy.SetParameter(1, arcpy.env.scratchGDB + '\\output')

        return
