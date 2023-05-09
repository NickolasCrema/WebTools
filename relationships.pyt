# -*- coding: utf-8 -*-

import arcpy
import arcgis
import arcgis.gis
import arcgis.gis.server

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
        param_output = arcpy.Parameter(
            name="output", 
            displayName="Output Features", 
            direction="Output", 
            parameterType="Derived", 
            datatype="DEFile"
        )        
        params = [param_output]
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
       
        gis = arcgis.gis.GIS('home', verify_cert=False)
        item = gis.content.get('e26d0297e11443fe95706f4ed6253b1d')
        
        # Lista todas as keys
        # featureSet = item.layers[0].query()
        # arcpy.AddMessage('\n'.join(i.attributes['local_soltura'] for i in featureSet.features))

        # Pega os registros desejados da tabela principal 
        # (nesse caso o registro cujo local de soltura é igual a 
        # "porto_ceramica_altonia" e "canal_da_piracema_lago_principal")
        featureSet = item.layers[0].query(where="local_soltura = 'porto_ceramica_altonia'")
        featureSet2 = item.layers[0].query(where="local_soltura = 'canal_da_piracema_lago_principal'")
        
        #Concatena os campos dos registros buscados 
        features = featureSet.features + featureSet2.features       
        
        # Lista as keys para procurar na tabela relacionada 
        # (necessário em caso de mais de uma query)
        lista = [i.attributes['local_soltura'] for i in features]
        
        # Busca os registros da tabela relacionada cuja key está na lista de keys
        another_set = [item.layers[1].query(where=f"local_soltura = '{i}'") for i in lista]

        #Transforma o resultado em string para visualização
        featureSet_str = '\n\n'.join(f'{i}' for i in features)
        another_set_str = '\n\n'.join(f'{j}' for i in another_set for j in i.features)

        str = f"Campo principal (referente ao local de soltura: 'porto_ceramica_altonia' e 'canal_da_piracema_lago_principal') :\n{featureSet_str}\n\nCampos relacionados: \n{another_set_str}"
        
        arcpy.AddMessage(str)
        
        
        portalAddMessage(0, 'output', str)
        return

# def GetServerManager(): 
#     gis = arcgis.GIS("home", verify_cert=False) 
#     url = arcpy.GetActivePortalURL() 
#     ARCGIS_SERVER_URL = url.replace(r'/portal/', r'/server/admin') 
#     server = arcgis.gis.server.Server(url=ARCGIS_SERVER_URL, gis=gis) 
#     return server
# def ExtractServiceFolderAndName(url):
#     parts = os.path.normpath(url) 
#     parts = parts.split(os.sep)
#     folder = parts[-4] 
#     name = parts[-3] 
#     if folder == 'services': 
#         folder = '\\' 
#     return folder, name
# def GetService(url): 
#     folder, name = ExtractServiceFolderAndName(url) 
#     services = GetServerManager().services 
#     for service in services.list(folder=folder): 
#         if service.properties["serviceName"] == name: 
#             return service

def portalAddMessage(paramOutputIndex, outputFileName, output):
    f = open(arcpy.env.scratchFolder + '\\{0}.txt'.format(outputFileName), 'w')
    f.write(str(output))
    f.close()
    arcpy.SetParameter(paramOutputIndex, f.name)