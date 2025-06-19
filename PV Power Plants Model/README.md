# iDesignRES: PV Power Plants Model

Assuming the model is installed on the system, proceed with the execution:

```
cd "PV Power Plants Model"
poetry run python pv_power_plants.py <input_payload> <start_time> <end_time>
```

Parameters explained:

- *<input_payload>*: the path to the JSON file containing the scenario definition. It is already included with the name *input.json* in the *"/PV Power Plants Model"* directory. The scenario is defined by modifying the values ​​of its content. The provided file contains the following information:

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

- *<start_time>*: the date and time from which you want to extract results. It must have the following format:
  
  > yyyy-MM-ddTHH:mm:ss

- *<end_time>*: the date and time up to which you want to extract results, with the following format:
  
  > yyyy-MM-ddTHH:mm:ss

It is necessary to clarify that at the current stage of development, only the *ES41* region is available for processing.

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

- Missing command line parameters (preprocess + process).

- Correct command line parameters (preprocess + process).

- Invalid payload (process).

- Payload with incorrect values (process).

- Valid payload (process).

- Correct execution tests (preprocess + process).

With a resulting code coverage of 97%:

| Name                  | Stmts   | Miss   | Cover   |
| --------------------- | ------- | ------ | ------- |
| modules/_ _init __.py | 0       | 0      | 100%    |
| modules/model.py      | 242     | 11     | 95%     |
| modules/preprocess.py | 246     | 0      | 100%    |
| modules/validator.py  | 196     | 11     | 94%     |
| **TOTAL**             | **684** | **22** | **97%** |