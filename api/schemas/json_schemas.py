authenticate_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "username": {"type": "string"},
    "password": {"type": "string"}
  },
  "required": [
    "username",
    "password"
  ]
}


pv_power_plants_process_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "nutsid": {"type": "string"},
    "slope_angle": {"type": "integer", "minimum": 0, "maximum": 360}
  },
  "required": [
    "nutsid",
    "slope_angle"
  ]
}

building_energy_simulation_process_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "nutsid": {"type": "string"},
    "year": {"type": "integer", "minimum": 1900, "maximum": 2025},
    "scenario": {
      "type": "object",
      "properties": {
        "increase_residential_built_area": {"type": "number", "minimum": 0, "maximum": 1},
        "increase_service_built_area": {"type": "number", "minimum": 0, "maximum": 1},
        "hdd_reduction": {"type": "number", "minimum": 0, "maximum": 1},
        "cdd_reduction": {"type": "number", "minimum": 0, "maximum": 1},
        "active_measures": {
          "type": "array",
          "minItems": 9,
          "maxItems": 9,
          "items": {
            "type": "object",
            "properties": {
              "building_use": {"type": "string"},
              "user_defined_data": {"type": "boolean"},
              "space_heating": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "solids": {"type": "number", "minimum": 0, "maximum": 1},
                  "lpg": {"type": "number", "minimum": 0, "maximum": 1},
                  "diesel_oil": {"type": "number", "minimum": 0, "maximum": 1},
                  "gas_heat_pumps": {"type": "number", "minimum": 0, "maximum": 1},
                  "natural_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "biomass": {"type": "number", "minimum": 0, "maximum": 1},
                  "geothermal": {"type": "number", "minimum": 0, "maximum": 1},
                  "distributed_heat": {"type": "number", "minimum": 0, "maximum": 1},
                  "advanced_electric_heating": {"type": "number", "minimum": 0, "maximum": 1},
                  "conventional_electric_heating": {"type": "number", "minimum": 0, "maximum": 1},
                  "bio_oil": {"type": "number", "minimum": 0, "maximum": 1},
                  "bio_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "hydrogen": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity_in_circulation": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "solids",
                  "lpg",
                  "diesel_oil",
                  "gas_heat_pumps",
                  "natural_gas",
                  "biomass",
                  "geothermal",
                  "distributed_heat",
                  "advanced_electric_heating",
                  "conventional_electric_heating",
                  "bio_oil",
                  "bio_gas",
                  "hydrogen",
                  "electricity_in_circulation"
                ]
              },
              "space_cooling": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "gas_heat_pumps": {"type": "number", "minimum": 0, "maximum": 1},
                  "electric_space_cooling": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "gas_heat_pumps",
                  "electric_space_cooling"
                ]
              },
              "water_heating": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "solids": {"type": "number", "minimum": 0, "maximum": 1},
                  "lpg": {"type": "number", "minimum": 0, "maximum": 1},
                  "diesel_oil": {"type": "number", "minimum": 0, "maximum": 1},
                  "natural_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "biomass": {"type": "number", "minimum": 0, "maximum": 1},
                  "geothermal": {"type": "number", "minimum": 0, "maximum": 1},
                  "distributed_heat": {"type": "number", "minimum": 0, "maximum": 1},
                  "advanced_electric_heating": {"type": "number", "minimum": 0, "maximum": 1},
                  "bio_oil": {"type": "number", "minimum": 0, "maximum": 1},
                  "bio_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "hydrogen": {"type": "number", "minimum": 0, "maximum": 1},
                  "solar": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "solids",
                  "lpg",
                  "diesel_oil",
                  "natural_gas",
                  "biomass",
                  "geothermal",
                  "distributed_heat",
                  "advanced_electric_heating",
                  "bio_oil",
                  "bio_gas",
                  "hydrogen",
                  "solar",
                  "electricity"
                ]
              },
              "cooking": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "solids": {"type": "number", "minimum": 0, "maximum": 1},
                  "lpg": {"type": "number", "minimum": 0, "maximum": 1},
                  "natural_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "biomass": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "solids",
                  "lpg",
                  "natural_gas",
                  "biomass",
                  "electricity"
                ]
              },
              "lighting": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "electricity"
                ]
              },
              "appliances": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "electricity"
                ]
              }
            },
            "required": [
              "building_use",
              "user_defined_data",
              "space_heating",
              "space_cooling",
              "water_heating",
              "cooking",
              "lighting",
              "appliances"
            ]
          }
        },
        "active_measures_baseline": {
          "type": "array",
          "minItems": 9,
          "maxItems": 9,
          "items": {
            "type": "object",
            "properties": {
              "building_use": {"type": "string"},
              "user_defined_data": {"type": "boolean"},
              "space_heating": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "solids": {"type": "number", "minimum": 0, "maximum": 1},
                  "lpg": {"type": "number", "minimum": 0, "maximum": 1},
                  "diesel_oil": {"type": "number", "minimum": 0, "maximum": 1},
                  "gas_heat_pumps": {"type": "number", "minimum": 0, "maximum": 1},
                  "natural_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "biomass": {"type": "number", "minimum": 0, "maximum": 1},
                  "geothermal": {"type": "number", "minimum": 0, "maximum": 1},
                  "distributed_heat": {"type": "number", "minimum": 0, "maximum": 1},
                  "advanced_electric_heating": {"type": "number", "minimum": 0, "maximum": 1},
                  "conventional_electric_heating": {"type": "number", "minimum": 0, "maximum": 1},
                  "bio_oil": {"type": "number", "minimum": 0, "maximum": 1},
                  "bio_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "hydrogen": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity_in_circulation": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "solids",
                  "lpg",
                  "diesel_oil",
                  "gas_heat_pumps",
                  "natural_gas",
                  "biomass",
                  "geothermal",
                  "distributed_heat",
                  "advanced_electric_heating",
                  "conventional_electric_heating",
                  "bio_oil",
                  "bio_gas",
                  "hydrogen",
                  "electricity_in_circulation"
                ]
              },
              "space_cooling": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "gas_heat_pumps": {"type": "number", "minimum": 0, "maximum": 1},
                  "electric_space_cooling": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "gas_heat_pumps",
                  "electric_space_cooling"
                ]
              },
              "water_heating": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "solids": {"type": "number", "minimum": 0, "maximum": 1},
                  "lpg": {"type": "number", "minimum": 0, "maximum": 1},
                  "diesel_oil": {"type": "number", "minimum": 0, "maximum": 1},
                  "natural_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "biomass": {"type": "number", "minimum": 0, "maximum": 1},
                  "geothermal": {"type": "number", "minimum": 0, "maximum": 1},
                  "distributed_heat": {"type": "number", "minimum": 0, "maximum": 1},
                  "advanced_electric_heating": {"type": "number", "minimum": 0, "maximum": 1},
                  "bio_oil": {"type": "number", "minimum": 0, "maximum": 1},
                  "bio_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "hydrogen": {"type": "number", "minimum": 0, "maximum": 1},
                  "solar": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "solids",
                  "lpg",
                  "diesel_oil",
                  "natural_gas",
                  "biomass",
                  "geothermal",
                  "distributed_heat",
                  "advanced_electric_heating",
                  "bio_oil",
                  "bio_gas",
                  "hydrogen",
                  "solar",
                  "electricity"
                ]
              },
              "cooking": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "solids": {"type": "number", "minimum": 0, "maximum": 1},
                  "lpg": {"type": "number", "minimum": 0, "maximum": 1},
                  "natural_gas": {"type": "number", "minimum": 0, "maximum": 1},
                  "biomass": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "solids",
                  "lpg",
                  "natural_gas",
                  "biomass",
                  "electricity"
                ]
              },
              "lighting": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity": {"type": "number", "minimum": 1, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "electricity"
                ]
              },
              "appliances": {
                "type": "object",
                "properties": {
                  "pct_build_equipped": {"type": "number", "minimum": 0, "maximum": 1},
                  "electricity": {"type": "number", "minimum": 1, "maximum": 1}
                },
                "required": [
                  "pct_build_equipped",
                  "electricity"
                ]
              }
            },
            "required": [
              "building_use",
              "user_defined_data",
              "space_heating",
              "space_cooling",
              "water_heating",
              "cooking",
              "lighting",
              "appliances"
            ]
          }
        },
        "passive_measures": {
          "type": "array",
          "minItems": 9,
          "maxItems": 9,
          "items": {
            "type": "object",
            "properties": {
              "building_use": {"type": "string"},
              "ref_level": {"type": "string"},
              "percentages_by_periods": {
                "type": "object",
                "properties": {
                  "Pre-1945": {"type": "number", "minimum": 0, "maximum": 1},
                  "1945-1969": {"type": "number", "minimum": 0, "maximum": 1},
                  "1970-1979": {"type": "number", "minimum": 0, "maximum": 1},
                  "1980-1989": {"type": "number", "minimum": 0, "maximum": 1},
                  "1990-1999": {"type": "number", "minimum": 0, "maximum": 1},
                  "2000-2010": {"type": "number", "minimum": 0, "maximum": 1},
                  "Post-2010": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": [
                  "Pre-1945",
                  "1945-1969",
                  "1970-1979",
                  "1980-1989",
                  "1990-1999",
                  "2000-2010",
                  "Post-2010"
                ]
              }
            },
            "required": [
              "building_use",
              "ref_level",
              "percentages_by_periods"
            ]
          }
        }
      },
      "required": [
        "increase_residential_built_area",
        "increase_service_built_area",
        "hdd_reduction",
        "cdd_reduction",
        "active_measures",
        "active_measures_baseline",
        "passive_measures"
      ]
    }
  },
  "required": [
    "nutsid",
    "year",
    "scenario"
  ]
}

