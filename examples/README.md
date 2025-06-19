# iDesignRES: PV Power Plants Model example

Assuming that the model is already installed with Poetry, the first thing to do is open a terminal and access its directory:

```
cd "PV Power Plants Model"
```

As mentioned in the *Getting Started* guide, the command to execute the model is:

```
poetry run python pv_power_plants.py <input_payload> <start_time> <end_time>
```

Let's suppose that the information to be obtained corresponds to the period between 1:00 p.m. on March 1, 2019, and 1:00 p.m. on March 2, 2019.. The *<start_time>* and *<end_time>* parameters will have the values:

> 2019-03-01T13:00:00    :    start_time
> 
> 2019-03-02T13:00:00    :    end_time

The next step consists of configuring the scenario. To do this, open the *input.json* file and edit its values. The provided file includes this content:

```
{
    "nutsid": "ES41",
    "slope_angle": 10,
    "area_total_thermal":  null,
    "area_total_pv": null,
    "power_thermal": 10,
    "power_pv": 200,
    "capex_thermal": null,
    "capex_pv": null,
    "tilt": 30,
    "azimuth": 180,
    "loss": 14,
    "tracking_percentage": 60,
    "efficiency_thermal": 45,
    "efficiency_optical": 65,
    "aperture":50,
    "system_cost_thermal": 5,
    "system_cost_pv": 0.5,
    "opex_thermal": 20000,
    "opex_pv": 15000,
    "min_ghi_thermal": 1700,
    "min_ghi_pv": 1000,
    "land_use_thermal": 50,
    "land_use_pv": 100,
    "convert_coord": 1,
    "pvgis_year": 2019
}
```

To facilitate the adjustment of scenario values, the set of editable properties and their possible values ​​are described below as a data dictionary:

```
- nutsid: text -> Identifier of NUTS2 region for which the analysis will be carried out.
- slope_angle: integer between 0 and 360 -> Maximum slope angle in º with which a land area can be considered suitable for PV.
- area_total_thermal: null, or integer between 0 and 10000000000 -> Area in m2 to deploy CSP technology. 
- area_total_pv: null, or integer between 0 and 10000000000 -> Area in m2 to deploy PV technology.
- power_thermal: null, or integer between 0 and 1000000000000 -> CSP power capacity in MW to be deployed.
- power_pv: null, or integer between 0 and 1000000000000 -> PV power capacity in MW to be deployed.
- capex_thermal: null, or integer between 0 and 500000000000 -> Investment in € to deploy CSP technology.
- capex_pv: null, or integer between 0 and 500000000000 -> Investment in € to deploy PV technology.
- tilt: integer between 0 and 90 -> Tilt angle in º from horizontal plane.
- azimuth: integer between 0 and 360 -> Orientation (azimuth angle) of the (fixed) plane of array. Clockwise from north.
- tracking_percentage: integer between 0 and 100 -> Percentage in % of single-axis tracking systems from the total PV capacity. The rest is considered fixed mounted systems.
- loss: integer between 8 and 20 -> Percentage in % of power losses of PV systems. Please read the documentation to understand which other losses are already included in the model.
- efficiency_thermal: integer between 25 and 65 -> Thermal efficiency in % of collectors of CSP systems.
- efficiency_optical: integer between 45 and 85 -> Amount of incoming solar radiation in % captured in the collectors of CSP systems.
- aperture: integer between 25 and 75 -> Aperture area in % of solar field of CSP systems.
- system_cost_thermal: decimal number between 1 and 10 -> CAPEX in €/W of CSP technology to compute CSP power capacity to be installed from a given investment.
- system_cost_pv: decimal number between 0.2 and 1 -> CAPEX in €/W of PV technology to compute PV power capacity to be installed from a given investment.
- opex_thermal: decimal number between 0 and 40000 -> Annual Operational Expenditures in €/MW for CSP technology.
- opex_pv: decimal number between 0 and 30000 -> Annual Operational Expenditures in €/MW for PV technology.
- min_ghi_thermal: integer between 1500 and 2500 -> Minimum annual Global Horizontal Irradiance in kWh/m2 in a land area to install CSP systems.
- min_ghi_pv: integer between 500 and 2000 -> Minimum annual Global Horizontal Irradiance in kWh/m2 in a land area to install PV systems.
- land_use_thermal: integer between 25 and 100 -> Land use ratio of CSP technology in W/m2 to compute required area for a given CSP power capacity.
- land_use_pv: integer between 50 and 200 -> Land use ratio of PV technology in W/m2 to compute required area for a given PV power capacity.
- convert_coord: integer with the value 0 (False) or 1 (True) -> Convert coordinates expressed into EPSG:3035 to EPSG:4326.
- pvgis_year: integer between 1900 and 2020 -> Year for calculate time-series hourly production.
```

The final execution command will be as follows:

```
poetry run python pv_power_plants.py input.json 2019-03-01T13:00:00 2019-03-02T13:00:00
```

All input values ​​will be validated, and the user will be notified of those that do not comply with the scheme.

When the execution finishes, a result similar to the following is obtained:

```
{
    'time(UTC)': [
        Timestamp('2019-03-0113: 00: 00'),
        Timestamp('2019-03-0114: 00: 00'),
        Timestamp('2019-03-0115: 00: 00'),
        Timestamp('2019-03-0116: 00: 00'),
        Timestamp('2019-03-0117: 00: 00'),
        Timestamp('2019-03-0118: 00: 00'),
        Timestamp('2019-03-0119: 00: 00'),
        Timestamp('2019-03-0120: 00: 00'),
        Timestamp('2019-03-0121: 00: 00'),
        Timestamp('2019-03-0122: 00: 00'),
        Timestamp('2019-03-0123: 00: 00'),
        Timestamp('2019-03-0200: 00: 00'),
        Timestamp('2019-03-0201: 00: 00'),
        Timestamp('2019-03-0202: 00: 00'),
        Timestamp('2019-03-0203: 00: 00'),
        Timestamp('2019-03-0204: 00: 00'),
        Timestamp('2019-03-0205: 00: 00'),
        Timestamp('2019-03-0206: 00: 00'),
        Timestamp('2019-03-0207: 00: 00'),
        Timestamp('2019-03-0208: 00: 00'),
        Timestamp('2019-03-0209: 00: 00'),
        Timestamp('2019-03-0210: 00: 00'),
        Timestamp('2019-03-0211: 00: 00'),
        Timestamp('2019-03-0212: 00: 00'),
        Timestamp('2019-03-0213: 00: 00')
    ],
    'Pthermal': [
        10.1687625,
        9.33894,
        16.177590000000002,
        12.6936225,
        9.50508,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.1325025,
        0.3782025,
        9.373747500000002,
        6.5236275,
        3.989115,
        7.7258025
    ],
    'Ppv': [
        124.5796,
        124.91560000000001,
        118.5708,
        106.6472,
        71.9428,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.004,
        79.44319999999999,
        103.268,
        123.5084,
        126.40599999999999,
        119.2748,
        125.5312
    ]
}
```

---

---

# iDesignRES: Building Energy Simulation Model example

As with the first model, and assuming that this model is already installed with Poetry,  open a terminal and access its directory:

```
cd "Building Energy Simulation Model"
```

And as mentioned in the *Getting Started* guide, the command to execute the model is:

```
poetry run python building_energy_process.py <input_payload> <start_time> <end_time> <building_use>
```

As with the first model, let's suppose that the information to be obtained corresponds to the period between 1:00 p.m. on March 1, 2019, and 1:00 p.m. on March 2, 2019. The *<start_time>* and *<end_time>* parameters will have the values:

> 2019-03-01T13:00:00    :    start_time
> 
> 2019-03-02T13:00:00    :    end_time

This model has *<building_use>* as an additional parameter, and it can take one of the following values:

> - Apartment Block.
> - Single family- Terraced houses.
> - Hotels and Restaurants.
> - Health.
> - Education.
> - Offices.
> - Trade.
> - Other non-residential buildings.
> - Sport.

For this example, *Apartment Block* will be used, so the final execution command will be as follows:

```
poetry run python building_energy_process.py input.json 2019-03-01T13:00:00 2019-03-02T13:00:00 "Apartment Block"
```

But before launching the execution, it is necessary to configure the scenario. To do this, open the *input.json* file and edit its values. The provided file includes this content:

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

When execution is launched, a full input validation is performed. And when the execution finishes, a result similar to the following is obtained:

```
{
    'Datetime': [
        Timestamp('2019-03-0113: 00: 00'),
        Timestamp('2019-03-0114: 00: 00'),
        Timestamp('2019-03-0115: 00: 00'),
        Timestamp('2019-03-0116: 00: 00'),
        Timestamp('2019-03-0117: 00: 00'),
        Timestamp('2019-03-0118: 00: 00'),
        Timestamp('2019-03-0119: 00: 00'),
        Timestamp('2019-03-0120: 00: 00'),
        Timestamp('2019-03-0121: 00: 00'),
        Timestamp('2019-03-0122: 00: 00'),
        Timestamp('2019-03-0123: 00: 00'),
        Timestamp('2019-03-0200: 00: 00'),
        Timestamp('2019-03-0201: 00: 00'),
        Timestamp('2019-03-0202: 00: 00'),
        Timestamp('2019-03-0203: 00: 00'),
        Timestamp('2019-03-0204: 00: 00'),
        Timestamp('2019-03-0205: 00: 00'),
        Timestamp('2019-03-0206: 00: 00'),
        Timestamp('2019-03-0207: 00: 00'),
        Timestamp('2019-03-0208: 00: 00'),
        Timestamp('2019-03-0209: 00: 00'),
        Timestamp('2019-03-0210: 00: 00'),
        Timestamp('2019-03-0211: 00: 00'),
        Timestamp('2019-03-0212: 00: 00'),
        Timestamp('2019-03-0213: 00: 00')
    ],
    'Solids|Coal': [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    'Liquids|Gas': [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    'Liquids|Oil': [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    'Gases|Gas': [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    'Solids|Biomass': [
        32122.691348017957,
        32122.691348017957,
        64245.382696035915,
        64245.382696035915,
        64245.382696035915,
        64245.382696035915,
        163660.41232639138,
        220565.83375773567,
        201560.15533916256,
        173119.4612462985,
        209993.0875329488,
        32122.691348017957,
        22698.978585984067,
        22830.887057335134,
        18527.014292553293,
        23606.21740838426,
        21067.383975638644,
        211216.26136272465,
        172116.72040547177,
        75185.93245862774,
        32122.691348017957,
        32122.691348017957,
        32122.691348017957,
        32122.691348017957,
        32122.691348017957
    ],
    'Electricity': [
        161173.11861968559,
        160213.8566797556,
        165801.12498076717,
        166724.35317887345,
        211430.6124219727,
        281552.06573231873,
        314936.5879770741,
        324306.6577357886,
        305390.9134292254,
        288023.3151820475,
        253053.63874331006,
        74470.98677417252,
        61016.137472871174,
        55468.66688247181,
        61409.44427627222,
        114906.60409195494,
        184004.56049890912,
        302144.70157534163,
        293791.3494591355,
        207919.85831409346,
        200691.2466995108,
        207607.2383517306,
        154847.83165558134,
        171245.36898895042,
        161173.11861968559
    ],
    'Heat': [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    'Liquids|Biomass': [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    'Gases|Biomass': [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    'Hydrogen': [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    'Heat|Solar': [
        6139.853042048224,
        6139.853042048224,
        12279.706084096448,
        12279.706084096448,
        12279.706084096448,
        12279.706084096448,
        12279.706084096448,
        12279.706084096448,
        12279.706084096448,
        12279.706084096448,
        24559.412168192895,
        6139.853042048224,
        2455.9412168192894,
        2455.9412168192894,
        2455.9412168192894,
        2455.9412168192894,
        2455.9412168192894,
        24559.412168192895,
        12279.706084096448,
        6139.853042048224,
        6139.853042048224,
        6139.853042048224,
        6139.853042048224,
        6139.853042048224,
        6139.853042048224
    ],
    'Variablecost[
        €/KWh
    ]': [
        38900.810689364705,
        38680.180443180805,
        41796.24555925048,
        42008.58804481494,
        52291.027670727766,
        68418.96193210736,
        81764.05873733135,
        87162.7838034223,
        81728.83894305413,
        76113.17178290997,
        70171.94290033943,
        18959.320364896696,
        15327.553398161457,
        14059.153945236612,
        15180.211998218147,
        27774.073333427543,
        43521.8898013605,
        81532.6082600039,
        77382.66343871303,
        52107.16556238328,
        47989.98014772452,
        49580.658227735046,
        37445.99468762075,
        41217.4282742956,
        38900.810689364705
    ],
    'Emissions[
        KgCO2/KWh
    ]': [
        64886.282773518884,
        64503.53725948683,
        67311.06575585475,
        67679.43380689916,
        85517.23124489575,
        113495.69111572382,
        128605.58602472759,
        133368.54144421886,
        125479.05725436588,
        118037.45306007033,
        104748.27743417378,
        30292.132167159154,
        24754.020466223305,
        22542.95405313828,
        24835.854523498576,
        46272.646946040935,
        73797.03255062629,
        124357.62863309032,
        120320.84940149356,
        84313.37025157864,
        80654.01587736912,
        83413.49654660482,
        62362.49327484131,
        68905.11067085555,
        64886.282773518884
    ]
}
```