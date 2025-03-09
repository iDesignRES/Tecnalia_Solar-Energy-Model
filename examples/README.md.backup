# iDesignRES Models: Examples

&nbsp;

## Authentication
All the functions that the REST API exposes are JWT secured, so before executing a process, invoke the authentication function to obtain the security token.

Any REST client can be used (Postman, Bruno, Insomnia, cUrl...) with the following data:

```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/authenticate
Verb: POST
Body:
{
  "username": "xxxxxx",
  "password": "xxxxxx"
}
```

Consult the component to obtain valid credentials.

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


## iDesignRES PV Power Plants Model example
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
```


## iDesignRES Building Stock Energy Simulation process example
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



