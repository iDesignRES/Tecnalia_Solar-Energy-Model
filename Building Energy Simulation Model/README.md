# iDesignRES: Building Energy Simulation Model

Assuming the model is installed on the system, proceed with the execution:

```
cd "Building Energy Simulation Model"
poetry run python building_energy_process.py <input_payload> <start_time> <end_time> <building_use>
```

Parameters explained:

- *<input_payload>*: the path to the JSON file containing the scenario definition. It is already included with the name *input.json* in the *"/Building Energy Simulation Model"* directory. The scenario is defined by modifying the values ​​of its content. The provided file contains the following information (reduced due to its extension), which is explained in more detail in the *Examples* section.
  
  ```
  {
      "nutsid": "ES21",
      "year": 2019,
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
  }
  ```
  
  To facilitate the adjustment of scenario values, the set of editable properties and their possible values ​​are described below as a data dictionary:
  
  ```
  - nutsid: text -> Region over which the model will be generated.
  - year: integer between 1900 and 2050 -> Year of the modeled scenario.
  - increase_residential_built_area: decimal number as percentage, between 0 and 1 -> % increase in residential built area compared to the base year. It represents the construction of new residential buildings.
  - increase_service_built_area: decimal number as percentage, between 0 and 1 -> % increase in tertiary built area compared to the base year. It represents the construction of new tertiary buildings.
  - hdd_reduction: decimal number as percentage, between -1 and 1 -> Reduction in heating degree days for future scenario.
  - cdd_reduction: decimal number as percentage, between -1 and 1 -> Reduction in cooling degree days for future scenarios. The value represents the reduction. If the value is negative, it will imply an increase.
  - building_use: text -> Input values are defined for each of the building uses.
  - user_defined_data: boolean -> Indicates whether the values used are user defined or those from the database are taken.
  - pct_build_equipped: decimal number as percentage, between 0 and 1 -> Represents the % of buildings equipped with the technology.
  
  % of buildings supplied by each type of fuel:
  
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
  
  - ref_level: text -> Type of renovation implemented: Low, Medium, or High level.
  - Pre-1945: decimal number as percentage, between 0 and 1 -> % of buildings from the construction period that are renovated.
  - 1945-1969: decimal number as percentage, between 0 and 1 -> % of buildings from the construction period that are renovated.
  - 1970-1979: decimal number as percentage, between 0 and 1 -> % of buildings from the construction period that are renovated.
  - 1980-1989: decimal number as percentage, between 0 and 1 -> % of buildings from the construction period that are renovated.
  - 1990-1999: decimal number as percentage, between 0 and 1 -> % of buildings from the construction period that are renovated.
  - 2000-2010: decimal number as percentage, between 0 and 1 -> % of buildings from the construction period that are renovated.
  - Post-2010: decimal number as percentage, between 0 and 1 -> % of buildings from the construction period that are renovated.
  
  Clarifications:
  1) As mentioned before, the fields "building_use" can only have the values:
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
  ```

- *<start_time>*: the date and time from which you want to extract results. It must have the following format:
  
  > yyyy-MM-ddTHH:mm:ss

- *<end_time>*: the date and time up to which you want to extract results, with the following format:
  
  > yyyy-MM-ddTHH:mm:ss

It is necessary to clarify that at the current stage of development, only the *ES21* region is available for processing.

Once the execution has finished, the returned information will be similar to:

```
{
    'time(UTC)': [
        Timestamp('2019-03-0113: 00: 00'),
        Timestamp('2019-03-0114: 00: 00'),
        Timestamp('2019-03-0115: 00: 00'),

        .  .  .  .  .  .  .  .  .  .  .  .

        Timestamp('2019-03-0211: 00: 00'),
        Timestamp('2019-03-0212: 00: 00'),
        Timestamp('2019-03-0213: 00: 00')
    ],
    'Pthermal': [
        10.1687625,
        9.33894,
        16.177590000000002,

        .  .  .  .  .  .  .  .  .  .  .  .

        6.5236275,
        3.989115,
        7.7258025
    ],
    'Ppv': [
        124.5796,
        124.91560000000001,
        118.5708,

        .  .  .  .  .  .  .  .  .  .  .  .

        126.40599999999999,
        119.2748,
        125.5312
    ]
}
```

## Testing

The following tests have been defined for the model:

- Missing command line parameters.

- Correct command line parameters.

- Invalid payload.

- Payload with incorrect values.

- Valid payload.

- Correct execution test.

With a resulting code coverage of 97%:

| Name                  | Stmts    | Miss   | Cover   |
| --------------------- | -------- | ------ | ------- |
| modules/_ _init __.py | 0        | 0      | 100%    |
| modules/model.py      | 805      | 17     | 98%     |
| modules/validator.py  | 517      | 29     | 94%     |
| **TOTAL**             | **1322** | **46** | **97%** |