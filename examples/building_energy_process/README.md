# iDesignRES Models: Building Stock Energy Model example

&nbsp;

Assuming the code has been downloaded to a directory, enter that directory to proceed with the installation of the client program:
```
cd selected_directory
```

Type the following command to install the client program:
```
poetry install
```

Once installed, proceed with the execution:
```
poetry run python building_energy_process.py auth.json process.json <start_time> <end_time> <building_use>
```

The client program has the following input parameters:

- *auth.json*, which contains the payload to be authenticated against the centralized REST API.
- *process.json*, which contains the payload to be sent to the centralized REST API.
- *<start_time>*, which represents the date **from** which the results are to be obtained, with the format *yyyy-MM-ddTHH:mm:ss*.
- *<end_time>*, which represents the date **until** which the results are to be obtained, with the format *yyyy-MM-ddTHH:mm:ss*.
- *<building_use>*, which represents the type of building, and it can be one of the following:
	+ Apartment Block
	+ Single family- Terraced houses
	+ Hotels and Restaurants
	+ Health
	+ Education
	+ Offices
	+ Trade
	+ Other non-residential buildings
	+ Sport

A practical example of an execution command could be:
```
poetry run python building_energy_process.py auth.json process.json 2019-01-01T13:00:00 2019-01-02T13:00:00 "Apartment Block"
```

When the execution ends, the process returns as output a filtered time series similar to the following (for example, between *2019-01-01 01:00:00* and *2019-01-31 23:00:00*):
```
[
    { "Datetime": "2019-01-01 01:00:00", "Solids|Coal": 0.0, ...., "Solids|Biomass": 32122.691348, ..., "Variable cost [€/KWh]": 38900.810689 },
    { "Datetime": "2019-01-01 02:00:00", "Solids|Coal": 0.0, ...., "Solids|Biomass": 32122.691348, ..., "Variable cost [€/KWh]": 38900.810689 },
    { "Datetime": "2019-01-01 03:00:00", "Solids|Coal": 0.0, ...., "Solids|Biomass": 98555.078645, ..., "Variable cost [€/KWh]": 57131.613673 },
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    { "Datetime": "2019-12-31 23:00:00", "Solids|Coal": 0.0, ...., "Solids|Biomass": 23625.356813, ..., "Variable cost [€/KWh]": 15458.251539 },
]
```

For any questions, please consult the component owner.