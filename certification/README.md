# iDesignRES: Certification 

This README provides an overview of the iDesignRES Certification process.

## Step 1

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

## Step 2
Work in progress.