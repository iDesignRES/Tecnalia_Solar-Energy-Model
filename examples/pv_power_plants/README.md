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
poetry run python pv_power_plants.py process.json
```

The client program has a single input parameter: *process.json*, which contains the payload to be sent to the centralized REST API.

When the execution ends, the process returns as output a time series similar to the following:
```
[
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 00:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 01:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 02:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 03:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 04:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 05:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 06:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 07:00:00" },
    { "Ppv": "10802,436960619998", "Pthermal": "16770,4875", "time(UTC)": "2019-01-01 08:00:00" },
    { "Ppv": "52280,47640937", "Pthermal": "145662,075", "time(UTC)": "2019-01-01 09:00:00" },
    { "Ppv": "49919,20137375", "Pthermal": "164349,9", "time(UTC)": "2019-01-01 10:00:00" },
    { "Ppv": "43312,7553725", "Pthermal": "139829,625", "time(UTC)": "2019-01-01 11:00:00" },
    { "Ppv": "38147,73946937", "Pthermal": "159838,0875", "time(UTC)": "2019-01-01 12:00:00" },
    { "Ppv": "39763,918840620005", "Pthermal": "115772,9625", "time(UTC)": "2019-01-01 13:00:00" },
    { "Ppv": "46548,423876880006", "Pthermal": "123481,8", "time(UTC)": "2019-01-01 14:00:00" },
    { "Ppv": "50649,60551562", "Pthermal": "86754,0375", "time(UTC)": "2019-01-01 15:00:00" },
    { "Ppv": "22610,06340437", "Pthermal": "40335,75", "time(UTC)": "2019-01-01 16:00:00" },
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-01-01 17:00:00" },
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    { "Ppv": "0,0", "Pthermal": "0,0", "time(UTC)": "2019-12-31 23:00:00" }
]
```

For any questions, please consult the component owner.