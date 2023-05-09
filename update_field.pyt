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
        
        paraminput = arcpy.Parameter(
            name="input", 
            displayName="Input Features", 
            direction="Input", 
            parameterType="Required", 
            datatype="GPFeatureRecordSetLayer"
        )

        field_to_update = arcpy.Parameter(
            name="field_to_update", 
            displayName="Campo de atualização", 
            direction="Input", 
            parameterType="Required", 
            datatype="GPString"
        )

        value_to_update = arcpy.Parameter(
            name="value_to_update",
            displayName='Novo valor',
            direction='Input',
            parameterType='Required',
            datatype='GPString'
        )

        params =  [paraminput, field_to_update, value_to_update]
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
        field_to_update = parameters[1].valueAsText
        value = parameters[2].valueAsText

        # Edita o registro utilizando UpdateCursor
        # (nesse caso para registro com OID = 2)
        with arcpy.da.UpdateCursor(layer, ['OID@', field_to_update]) as cursor:
            for row in cursor:
                # Compara OID com 2
                if row[0] == 2:
                    # Edita o valor do campo field_to_update
                    row[1] = value
                    # Aplica a edição
                    cursor.updateRow(row)
        
    # Criação da expressão para utilizar CalculateField
    #     exp = "returnStr('{0}')".format(value)
    #     codeblock = """def returnStr(data):
    #  return data"""
        #  CalculateField para edição dos registros
        #  arcpy.management.CalculateField(layer, field_to_update, exp, 'PYTHON3', codeblock)
        
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return