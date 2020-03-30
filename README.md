# mapservicedoc
GISTMaps doc public repository

Geometry and related data for countries in CODs hosted for the humanitarian community as coordinated through [UN OCHA](https://www.unocha.org/) are documented in these pages. Now under development for this funding cycle are COD Version 2. Spreadsheets of sources, fomats and metadata and portals for CODs are to be consolidated and managed through an api with expanded sources for CODs including vector tile data and versions. An example for vector tiles include the leaflet example: ![alt text](https://github.com/UGA-ITOSHumanitarianGIS/mapservicedoc/blob/master/Doc/Images/VectorTile.png "Ecuador Administrative level 2 vector tile format boundaries in leaflet client")  A sample preview dataset is available here: https://itos-humanitarian.s3.amazonaws.com/v1/VectorTile/COD_ECU/Admin2/{z}/{x}/{y}.pbf

Deployment status of map services (https://gistmaps.itos.uga.edu/arcgis/rest/services/COD_External) based on [UN OCHA processing protocols](https://data.humdata.org/organization/inform) are available in the [DOC folder](https://github.com/UGA-ITOSHumanitarianGIS/mapservicedoc/blob/master/Data/CODServiceDeploymentStatus.xlsx).

ITOS is planning an API for this tracking document. This way, organizations may include the status in their own spreadsheets or website documentation for these important source data automatically! 

![alt text](https://github.com/UGA-ITOSHumanitarianGIS/mapservicedoc/blob/master/Doc/Images/TrackingAPI.png "Process for tracking api with Excel consumer as example")
 
Under investigation for low bandwidth uses are the Amazon S3 services. Mozambique is published. For urls of Mozambique administrative boundaries at different levels in simplified geometry geojson, topojson, KML and csv format please refer to the [spreadsheet](https://github.com/UGA-ITOSHumanitarianGIS/mapservicedoc/blob/master/Data/AWSDeploymentURLlist.xlsx). For more information on how to use these, please see the [Wiki](https://github.com/UGA-ITOSHumanitarianGIS/mapservicedoc/wiki).
