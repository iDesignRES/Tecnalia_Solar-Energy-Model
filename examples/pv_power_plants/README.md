# iDesignRES Models: PV Power Plants example

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
poetry run python pv_power_plants.py auth.json process.json <start_time> <end_time> <thermal_investment> <pv_investment>
```

The client program has the following input parameters:

- *auth.json*, which contains the payload to be authenticated against the centralized REST API.
- *process.json*, which contains the payload to be sent to the centralized REST API.
- *<start_time>*, which represents the date **from** which the results are to be obtained, with the format *yyyy-MM-ddTHH:mm:ss*.
- *<end_time>*, which represents the date **until** which the results are to be obtained, with the format *yyyy-MM-ddTHH:mm:ss*.
- *<thermal_investment>*, which represents the thermal investment.
- *<pv_investment>*, which represents the photovoltaic investment.

A practical example of an execution command could be:
```
poetry run python pv_power_plants.py auth.json process.json 2019-01-01T13:00:00 2019-01-02T13:00:00 5 0.5
```

When the execution ends, the process returns as output a filtered time series similar to the following (for example, between *2019-01-01 01:00:00* and *2019-01-31 23:00:00*):
```
[
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 01:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 02:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 03:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 04:00:00" },
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-31 23:00:00" }
]
```

For any questions, please consult the component owner.