# -*- coding: utf-8 -*-

import arcpy
import arcgis.gis
from arcgis.features import FeatureLayer
import pandas as pd


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
        input_layer = arcpy.Parameter(
            name='input_layer',
            displayName='Camada',
            direction='Input',
            parameterType='Optional',
            datatype='GPFeatureRecordSetLayer',
        )

        output_type = arcpy.Parameter(
            name='output_type',
            displayName='Tipo de Arquivo do Output',
            direction='Input',
            parameterType='Required',
            datatype='GPString',
        )
        output_type.filter.list = ['EXCEL', 'KML']
        
        param_output = arcpy.Parameter(
            name="output", 
            displayName="Output Features", 
            direction="Output", 
            parameterType="Derived", 
            datatype="DEFile",
        )

        params = [input_layer, output_type, param_output]
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
        output_type = parameters[1].value
        input_txt = parameters[0].valueAsText
        
        if input_layer != '' and input_layer is not None:
            coded_values = get_dict_domain_from_feature(input_txt)

            ##Geração do csv
            if output_type == 'EXCEL':
                    
                    fields = [field.name for field in arcpy.ListFields(input_layer)]
                    fields_label = [field.aliasName for field in arcpy.ListFields(input_layer)]
                    fields_to_rename = dict(zip(fields, fields_label))
                    oid_field_name = arcpy.Describe(input_layer).OIDFieldName
                    rows = []

                    with arcpy.da.SearchCursor(input_layer, fields) as cursor:
                        for row in cursor:
                            lin = []
                            for col in row:
                                lin.append(col)
                            rows.append(lin)

                    df = pd.DataFrame(data=rows, columns=fields)
                    new_df = transform_dataframe(df, coded_values)\
                                .rename(columns=fields_to_rename)\
                                .set_index(fields_to_rename[oid_field_name])
    
                    new_df.to_csv(arcpy.env.scratchFolder + '\\feature.csv', 
                                  sep=';', 
                                  encoding='utf-8-sig'
                                  )
                    
                    arcpy.SetParameter(2, arcpy.env.scratchFolder + '\\feature.csv')

            ##Geração do kml
            elif output_type == 'KML':
                    new_layer = arcpy.MakeFeatureLayer_management(input_layer, 'inputs_layer')
                    arcpy.conversion.LayerToKML(new_layer, 'feature.kmz')
                    arcpy.SetParameter(2, arcpy.env.scratchFolder + '\\feature.kmz')

        return

def transform_dataframe(df, domains):
    """Transforma os dados do dataframe com os dados coletados do domain
    @Retorna o dataframe transformado"""
    for key, value in domains.items():
        if df.get(key) is not None:
            df[key] = df[key].map(domains[key])
        else:
            pass
    return df

def get_dict_domain_from_feature(feature_url):
    """Coleta os dados de 'name' do domain dos campos
    @Retorna um dictionary com os dados coletados indexados pelo seu campo e pelo seu code"""
    gis = arcgis.gis.GIS('home')
    feature = FeatureLayer(feature_url)
    dict_domain_desc = {}
    inside_dict = {}
    for field in feature.properties.fields:
        if(field.get('domain') is not None):
            dict_domain_desc[field.get('name')] = []
            if field.get('domain').get('type') == 'codedValue':
                for domain in field.get('domain').get('codedValues'):
                    inside_dict[domain.get('code')] = domain.get('name')
                dict_domain_desc[field.get('name')] = inside_dict
    return dict_domain_desc
