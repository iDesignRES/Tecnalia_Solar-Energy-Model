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
Various tests have been carried out on the functions defined in the REST API. They are located in the */api/tests/* directory, and they are described as:

- Test 01: the only test that checks whether the application is correctly started and running.
- Test 02: performs three authentication checks:
	+ (a): authentication attempt with missing parameters.
	+ (b): authentication with incorrect credentials.
	+ (c): authentication with correct credentials.
- Test 03: performs checks on the execution of the PV Power Plants process:
	+ (a): attempt to launch process with missing input parameters.
	+ (b): attempt to launch process with wrong input parameters.
	+ (c): attempt to launch process with correct input parameters.
- Test 04: performs checks on the execution of the Building Energy Simulation process:
	+ (a): attempt to launch process with missing input parameters. Due to the long input length of the function, checking each parameter can be considered a stress test for practical purposes.
	+ (b): attempt to launch process with wrong input parameters. Due to the long input length of the function, checking each parameter can be considered a stress test for practical purposes.
	+ (c): attempt to launch process with correct input parameters.
	
All defined tests has been executed successfully, using the "PyTest" Python library. The command used inside the Docker container is the following:

```
export PYTHONPATH=/home/qgis/api:$PYTHONPATH && cd /home/qgis && pytest -s --cov=api --cov-report=term-missing /home/qgis/api/tests/
```

And the command used outside the Docker container is the following:

```
sudo docker exec -it ideignres.qgis.dck bash -c "export PYTHONPATH=/home/qgis/api:$PYTHONPATH && cd /home/qgis && pytest -s --cov=api --cov-report=term-missing /home/qgis/api/tests/"
```

Code coverage was also analyzed, with an overall result of **87%**. The result can be consulted in this directory (file *Step2__Automated testing__Result.png*). Most of the uncovered code relates to handling unthrown exceptions. Throwing them would require changes to the API configuration file, which greatly complicates test definition.

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

All the functions that the REST API exposes are JWT secured, so before executing a process, invoke the authentication function to obtain the security token.

**Authentication**:

Any REST client can be used (Postman, Bruno, Insomnia, cUrl...) with the following data:

```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/authenticate
Verb: POST
Body:
{
  "username": "xxxxxx",
  "password": "xxxxxx"
}

Data dictionary:
- username: text
- password: text.
```

Consult the component owner to obtain valid credentials.

The function returns the following response (if login is successful):
```
{
  "code": "200",
  "error": null,
  "message": "Success!",
  "value": "The security token"
}
```

The "value" field contains the security token required to invoke any process-related function.


**PV Power Plants Model**:

To execute the process, follow the procedure described for the previous process with the following data:
```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/pv-power-plants-process
Verb: POST
Body:
{
  "nutsid": "XXXX"
  "slope_angle": YY
}
Authentication:
Use the JWT token as a "Bearer" token.

Data dictionary:
- nutsid: text
- slope_angle: integer between 0 and 360.
```


**Building Stock Energy Simulation**:

To execute the process, follow the procedure described for the previous process with the following sample data:
```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/building-energy-simulation-process
Verb: POST
Body:
{
	"nutsid": "XXXX",
	"year": YYYY,
	"scenario": {
		"increase_residential_built_area": 0.13,
		"increase_service_built_area": 0,
		"hdd_reduction": 0.16,
		"cdd_reduction": 0,
		"active_measures": [
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
			},
			"space_cooling": {
				"pct_build_equipped": 0.02,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"natural_gas": 0,
				"biomass": 0,
				"electricity": 1
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Single family- Terraced houses",
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
			},
			"space_cooling": {
				"pct_build_equipped": 0.005,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"natural_gas": 0,
				"biomass": 0,
				"electricity": 1
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Offices",
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
			},
			"space_cooling": {
				"pct_build_equipped": 1,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Education",
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
			},
			"space_cooling": {
				"pct_build_equipped": 0,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Health",
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
			},
			"space_cooling": {
				"pct_build_equipped": 0.6,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Trade",
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
			},
			"space_cooling": {
				"pct_build_equipped": 1,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Hotels and Restaurants",
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
			},
			"space_cooling": {
				"pct_build_equipped": 1,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Other non-residential buildings",
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
			},
			"space_cooling": {
				"pct_build_equipped": 0.75,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Sport",
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
			},
			"space_cooling": {
				"pct_build_equipped": 0.5,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"diesel_oil": 0,
				"natural_gas": 0,
				"biomass": 0.4914,
				"geothermal": 0.0885,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.3096,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.1105,
				"electricity": 0
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		}
	],
	"active_measures_baseline": [
		{
			"building_use": "Apartment Block",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 0.783,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 0.02,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"natural_gas":0,
				"biomass":0,
				"electricity": 1
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Single family- Terraced houses",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 0.786,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 0.005,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0,
				"natural_gas":0,
				"biomass":0,
				"electricity": 1
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Offices",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 1,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Education",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 0,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Health",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 0.6,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Trade",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 1,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Hotels and Restaurants",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 1,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Other non-residential buildings",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 0.75,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		},
		{
			"building_use": "Sport",
			"user_defined_data": true,
			"space_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0645,
				"diesel_oil": 0.1342,
				"gas_heat_pumps": 0,
				"natural_gas": 0.6342,
				"biomass": 0.1059,
				"geothermal": 0.001,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.0036,
				"conventional_electric_heating": 0.0566,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"electricity_in_circulation": 0
			},
			"space_cooling": {
				"pct_build_equipped": 0.5,
				"gas_heat_pumps": 0,
				"electric_space_cooling": 1
			},
			"water_heating": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.124,
				"diesel_oil": 0.1093,
				"natural_gas": 0.5399,
				"biomass": 0.0614,
				"geothermal": 0.0014,
				"distributed_heat": 0,
				"advanced_electric_heating": 0.004,
				"bio_oil": 0,
				"bio_gas": 0,
				"hydrogen": 0,
				"solar": 0.0308,
				"electricity": 0.1292
			},
			"cooking": {
				"pct_build_equipped": 1,
				"solids": 0,
				"lpg": 0.0563,
				"natural_gas": 0.5222,
				"biomass": 0,
				"electricity": 0.4215
			},
			"lighting": {
				"pct_build_equipped": 1,
				"electricity": 1
			},
			"appliances": {
				"pct_build_equipped": 1,
				"electricity": 1
			}
		}
	],
	"passive_measures": [
		{
			"building_use": "Apartment Block",
			"ref_level": "High",
			"percentages_by_periods":  {
				"Pre-1945": 1,
				"1945-1969": 1,
				"1970-1979": 1,
				"1980-1989": 1,
				"1990-1999": 0.13,
				"2000-2010": 0,
				"Post-2010": 0
			}
		},
		{
			"building_use": "Single family- Terraced houses",
			"ref_level": "High",
			"percentages_by_periods":  {
				"Pre-1945": 1,
				"1945-1969": 1,
				"1970-1979": 1,
				"1980-1989": 1,
				"1990-1999": 0.13,
				"2000-2010": 0,
				"Post-2010": 0
			}
		},
		{
			"building_use": "Offices",
			"ref_level": "Medium",
			"percentages_by_periods":  {
				"Pre-1945": 0,
				"1945-1969": 0,
				"1970-1979": 0,
				"1980-1989": 0,
				"1990-1999": 0,
				"2000-2010": 0,
				"Post-2010": 0
			}
		},
		{
			"building_use": "Education",
			"ref_level": "Medium",
			"percentages_by_periods":  {
				"Pre-1945": 0,
				"1945-1969": 0,
				"1970-1979": 0,
				"1980-1989": 0,
				"1990-1999": 0,
				"2000-2010": 0,
				"Post-2010": 0
			}
		},
		{
			"building_use": "Health",
			"ref_level": "Low",
			"percentages_by_periods":  {
				"Pre-1945": 0,
				"1945-1969": 0,
				"1970-1979": 0,
				"1980-1989": 0,
				"1990-1999": 0,
				"2000-2010": 0,
				"Post-2010": 0
			}
		},
		{
			"building_use": "Trade",
			"ref_level": "Low",
			"percentages_by_periods":  {
				"Pre-1945": 0,
				"1945-1969": 0,
				"1970-1979": 0,
				"1980-1989": 0,
				"1990-1999": 0,
				"2000-2010": 0,
				"Post-2010": 0
			}
		},
		{
			"building_use": "Hotels and Restaurants",
			"ref_level": "Medium",
			"percentages_by_periods":  {
				"Pre-1945": 0,
				"1945-1969": 0,
				"1970-1979": 0,
				"1980-1989": 0,
				"1990-1999": 0,
				"2000-2010": 0,
				"Post-2010": 0
			}
		},
		{
			"building_use": "Other non-residential buildings",
			"ref_level": "Medium",
			"percentages_by_periods":  {
				"Pre-1945": 0,
				"1945-1969": 0,
				"1970-1979": 0,
				"1980-1989": 0,
				"1990-1999": 0,
				"2000-2010": 0,
				"Post-2010": 0
			}
		},
		{
			"building_use": "Sport",
			"ref_level": "Medium",
			"percentages_by_periods":  {
				"Pre-1945": 0,
				"1945-1969": 0,
				"1970-1979": 0,
				"1980-1989": 0,
				"1990-1999": 0,
				"2000-2010": 0,
				"Post-2010": 0
			}
		}
	]
}
Authentication:
Use the JWT token as a "Bearer" token.

Data dictionary:
- nutsid: text
- year: integer between 1900 and 2025.
- increase_residential_built_area: decimal number as percentage, between 0 and 1.
- increase_service_built_area: decimal number as percentage, between 0 and 1.
- hdd_reduction: decimal number as percentage, between 0 and 1.
- cdd_reduction: decimal number as percentage, between 0 and 1.
- building_use: text.
- user_defined_data: boolean.
- pct_build_equipped: decimal number as percentage, between 0 and 1.
- solids: decimal number as percentage, between 0 and 1.
- lpg: decimal number as percentage, between 0 and 1.
- diesel_oil: decimal number as percentage, between 0 and 1.
- gas_heat_pumps: decimal number as percentage, between 0 and 1.
- natural_gas: decimal number as percentage, between 0 and 1.
- biomass: decimal number as percentage, between 0 and 1.
- geothermal: decimal number as percentage, between 0 and 1.
- distributed_heat: decimal number as percentage, between 0 and 1.
- advanced_electric_heating: decimal number as percentage, between 0 and 1.
- conventional_electric_heating: decimal number as percentage, between 0 and 1.
- bio_oil: decimal number as percentage, between 0 and 1.
- bio_gas: decimal number as percentage, between 0 and 1.
- hydrogen: decimal number as percentage, between 0 and 1.
- electricity_in_circulation: decimal number as percentage, between 0 and 1.
- electric_space_cooling: decimal number as percentage, between 0 and 1.
- solar: decimal number as percentage, between 0 and 1.
- electricity: decimal number as percentage, between 0 and 1.
- ref_level: text.
- Pre-1945: decimal number as percentage, between 0 and 1.
- 1945-1969: decimal number as percentage, between 0 and 1.
- 1970-1979: decimal number as percentage, between 0 and 1.
- 1980-1989: decimal number as percentage, between 0 and 1.
- 1990-1999: decimal number as percentage, between 0 and 1.
- 2000-2010: decimal number as percentage, between 0 and 1.
- Post-2010: decimal number as percentage, between 0 and 1.

Clarifications:
1) The fields "building_use" can only have the values:
   - Apartment Block
   - Single family- Terraced houses
   - Offices
   - Education
   - Health
   - Trade
   - Hotels and Restaurants
   - Other non-residential buildings
   - Sport
2) The fields "ref_level" can only have the values:
   - "Low"
   - "Medium"
   - "High"
3) The sum of all the Energy Systems in each section must add up to 1.
4) For any further clarification, please consult the component owner.
```