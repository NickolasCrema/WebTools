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
            datatype="DEFile"
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
        input_layer = parameters[0].value
        output_file = arcpy.env.scratchFolder + '\\output.csv'
        fields = [i.name for i in arcpy.ListFields(input_layer)]
        arcpy.AddMessage(fields)
        with open(output_file, 'w') as f:
            f.write(';'.join(fields) + '\n')
            with arcpy.da.SearchCursor(input_layer, fields) as cursor:
                for row in cursor:
                    f.write(';'.join(str(col) for col in row) + '\n')
        arcpy.SetParameter(1, output_file)
        return
