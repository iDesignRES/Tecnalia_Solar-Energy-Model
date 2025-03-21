# iDesignRES Models: Examples

&nbsp;

This directory contains a client program to execute the *PV Power Plants process* and *Building Stock Energy Model process* in *standalone* mode. This is, the code can be downloaded, installed and executed in any local terminal.

The steps to follow are:

- Make sure that *Python* is installed on the local machine. The client program has been developed under version 3.10, although any other version should not cause problems.
- Make sure that *Poetry* is installed. The version used was 2.1.1, so it is recommended to use the same version. It can be checked with the command:
```
poetry --version
```

- Download the client programs, located at */examples/pv_power_plants/* and */examples/building_energy_process/* directories.
- The *README.md* files in the */examples/pv_power_plants/* and */examples/building_energy_process/* directories details how to install and run the client programs.

It is necessary to clarify that the client programs calls the global REST API of the component from the local location, since, due to the design of its architecture oriented towards integration and scalability and reusability, it is deployed on a server as a single instance.

For any questions, please consult the component owner.