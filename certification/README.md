# iDesignRES: Certification 

This README provides an overview of the iDesignRES Certification process.

## Step 1: Identification

(1) **Stress testing**: 

The *Solar Energy Model* has been tested numerous times, changing the input data and parameters. No performance issues have been observed, with results obtained in less than 15 seconds, although this value depends on the size of the region. The tests have been very useful in finding and correcting some minor bugs.

The *Building Stock Energy Model* has also been tested numerous times, changing the input data and parameters. This process requires more memory, so it has had to be expanded from 16GB to 32GB to have a minimum viable case. The execution time is about 8 and 10 minutes, a variation that depends on different factors (network traffic, other running processes...), but not because of changes in input parameters, so the input does not significantly affect execution. Finally, and as in the previous model, the stress tests have allowed to identify and solve some minor bugs.

<br>

(2) **Check for deviating model results**:

As a preliminary clarification, and for the *Solar Energy Model*, results are not included for the Euskadi Use Case because it does not have regions with the minimum radiation considered. The results included correspond to Castilla y León (Spain).

Two examples of inputs and results are included for each of the models, following the nomenclature:
```
Step1__<model_name>__InputXX.<extension>
Step1__<model_name>__ResultXX.<extension>
```

<br>

(3) **Integration**:

Both models are executed by calling a function of a REST API, which is why it is very easy to integrate with other components.

All the results can be consulted through the UI available in the component. This graphical interface can also be integrated with other components, and it is deployed at:

https://idesignres.digital.tecnalia.dev

<br>

## Step 2: Quality
(1) **Publication platform**:

The code has been published on the GitHub of the IDesignRES project, and all data input examples are included in JSON format.

<br>

(2) **Documentation**:
The README.md file located in the root directory contains installation instructions under the heading *Getting started*.

The README.md file in the *examples* directory also explains in detail the format of the input data for each of the models. In addition, these inputs can be downloaded from this directory.

<br>

(3) **Coding standards**:
The component is mostly composed of Python and Java code. Every function in Python includes a Docstring that describes its functionality. In the case of Java, Javadoc has been used for the same purpose.

All code is extensively commented, and uses Camel Case styling as the coding standard.

<br>

(4) **Robustness of code**:
The code does not include circular references or any other expressions that would result in catastrophic failure. In addition, all the code corresponding to the execution of the models is surrounded by *try-catch* statements for error handling.

It also includes exhaustive validations of input data. For the following input example:
```
{
	"nutsid": "ES21",
	"slope_angle": 10
}
```
The component is validating that both *nutsid* and *slope_angle* have a value, and *slope_angle* is also an integer between 0 and 360.

It is also being validated that all percentage values ​​are decimal numbers between 0 and 1. And also that some text values ​​are included in a fixed list, For example:
```
{
	"building_use": "Apartment Block",
	"user_defined_data": true,
	"space_heating": {
		"pct_build_equipped": 1,
		"solids": 0,
		"lpg": 0,
		"diesel_oil": 0,
		"gas_heat_pumps": 0,
		"natural_gas": 0,
		"biomass": 0.5363,
		"geothermal": 0.1016,
		"distributed_heat": 0,
		"advanced_electric_heating": 0.3621,
		"conventional_electric_heating": 0,
		"bio_oil": 0,
		"bio_gas": 0,
		"hydrogen": 0,
		"electricity_in_circulation": 0
	}
}
```
The property *building_use* must have one of these values:

- Apartment Block
- Single family- Terraced houses
- Hotels and Restaurants
- Health
- Education
- Offices
- Trade
- Other non-residential buildings
- Sport

Properties like *solids*, *lpg*, *diesel_oil*, *gas_heat_pumps*... belong to percentages and their values ​​must be between 0 and 1. In this example, the additional circumstance is that it is validated that the sum of the values ​​between *solids* and *electricity_in_circulation* (all the energy systems) must be 1.

Finally, it should be noted that most of the validations have been carried out using the *jsonschema* library, leaving the more complex validations for manual control.

<br>

(5) **Automated testing**:
Work in progress.

<br>

(6) **Versioning and compatibility**:
The component includes Semantic Versioning:
```
MAJOR_version.MINOR_version.PATCH_version
```
And the current version is specified in three different places:

- *VERSION* file: the root directory of the repository contains a *VERSION* file with the component current version information, and key dependencies that meet compatibility requirements:
```
-----------------------------------
Component version: 0.4.160
-----------------------------------


-----------------------------------
Python key dependencies:
-----------------------------------
fiona:1.9.6
Flask:2.0.0
Flask-JWT-Extended:4.4.1
Flask-Testing.0.8.1 
geopandas:0.10.2
jsonschema:4.17.3
openpyxl:3.1.3
paramiko:3.5.0
pvlib:0.10.4
pygeos:0.14
PyMySQL:1.1.1
pyproj:3.2.1
pytest:7.4.4
rasterio:1.2.10
requests:2.31.0
scikit-learn:1.0.2
Werkzeug:2.2.3
zipfile37:0.1.3


-----------------------------------
Java key dependencies:
-----------------------------------
com.jcraft.jsch:0.1.55
mariadb-java-client
org.json:20200518
spring-boot-starter-data-jpa
spring-boot-starter-data-rest
spring-boot-starter-security
io.jsonwebtoken.jjwt:0.9.0
```

- *API configuration* file: the *config.ini* file contains information about the current version, which will be shown in the logs of each function, as well as part of the response from the *hello* function. The following file attaches some examples:

>Step2__Versioning and compatibility.rar

- Git tags: every time code is uploaded to the repository it is tagged with the new version to which it belongs.

<br>

(7) **Input data processing**:
The file *examples/README.md* describes in detail the input data for each model. That section can be consulted for any clarification.