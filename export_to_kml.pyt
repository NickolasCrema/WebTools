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
        param_input = arcpy.Parameter(
            name="input", 
            displayName="Input Features", 
            direction="Input", 
            parameterType="Required", 
            datatype="GPFeatureRecordSetLayer"
        )
        param_output = arcpy.Parameter(
            name="output", 
            displayName="Output Features", 
            direction="Output", 
            parameterType="Derived", 
            datatype="DEFile"
        )
        params = [param_input, param_output]
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
        arcpy.env.overwriteOutput = True
        layer = parameters[0].value
      
        new_feat = arcpy.CreateFeatureclass_management(arcpy.env.scratchGDB, 'feat', geometry_type='POINT', template=layer, spatial_reference=arcpy.Describe(layer).spatialReference)
        layer_fields_object = arcpy.ListFields(layer)
        
        layer_fields = [field.name for field in layer_fields_object]

        edit = arcpy.da.Editor(arcpy.env.scratchGDB)
        edit.startEditing(with_undo=False, multiuser_mode=False)
        edit.startOperation()
        new_feat_cursor = arcpy.da.InsertCursor(new_feat, layer_fields)
        cursor = arcpy.da.SearchCursor(layer, layer_fields)
        for row in cursor:
            new_feat_cursor.insertRow(row)
        edit.stopOperation() 
        edit.stopEditing(save_changes=True)

        new_layer = arcpy.MakeFeatureLayer_management(new_feat, 'layer')
        arcpy.conversion.LayerToKML(new_layer, arcpy.env.scratchFolder + '\\features.kmz')
        arcpy.SetParameter(1, arcpy.env.scratchFolder + '\\features.kmz')
        
        return
