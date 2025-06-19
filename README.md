# iDesignRES Solar Energy Model

This README provides an overview of the iDesignRES Solar Energy Model within iDesignRES.

It is handled by Tecnalia and part of WP1, Task number Task 1.3. 

## Purpose of the model

The solar power model provides time-series of annual thermal energy generation in Concentrating Solar Power (CSP) plants and electrical energy generation in large Photovoltaic (PV) plants on hourly basis, for a given NUTS2 region and a specific amount of investment in €, in MWp or in m2 for each of these technologies: CSP and PV. These profiles are provided aggregated at NUTS2 level and disaggregated at NUTS3 level, as well as the annual operational expenditures of both technologies

## Model design philosophy

The model firstly establishes the required area to deploy the given investment in each technology. Then, the most suitable available areas in the given region NUTS2 are selected. Once potential areas for each technology in each NUTS3 region are categorized by intervals of 100W/m2 of Global Horizontal Irradiance (GHI), those with higher GHI are selected until reaching the area, power capacity or investment required by the user at the input.

Since CSP technology requires higher solar radiation, CSP technology is prioritized when selecting the locations. Considering the solar resource on hourly basis of selected areas for each technology, simplified models are used to estimate annual thermal and electrical energy generation. These profiles are obtained at NUTS3 level and they are finally aggregated to provide them at NUTS2 level.

## Input to and output from the model

Input: 

- NUTS2 region identifier.
- Investment in €, power capacity in MW or area in m2 to deploy CSP technology in the given NUTS2 region. 
- Investment in €, power capacity in MWp or area in m2 to deploy PV plants in the given NUTS2 region.
- Optional: Financial and technical parameters of CSP and PV technologies in the market.
- Optional: Configuration parameters of areas selection criteria.

Output: 

- Time-series of annual thermal energy generation and electrical energy generation on hourly basis aggregated at NUTS2 level.
- Time-series of annual thermal energy generation and electrical energy generation on hourly basis disaggregated at NUTS3 level.

## Implemented features

- Estimation of required area to deploy given investment or power capacity of CSP and PV technologies 
- Categorization of available areas in intervals of 100W/m2 of annual radiation for each NUTS3 region complying with selection criteria (maximum slope and land use restriction) for each technology.  
- Selection of previously characterized areas with the highest solar radiation until reaching all the required area, prioritizing CSP and relegating PV in case of conflicts. 
- For each selected areas estimation of annual thermal or electrical energy generation on hurly basis making use of simplified model of CSP and Solar PV models. 
  - Aggregation of estimated generation profiles at NUTS3 and NUTS2 level.  

## Core assumption

The main factor impacting on generation profile of CSP and solar PV plants is the available solar radiation. For this purpose, a selection of potential locations with the highest solar resource in the region for CSP and PV deployment is carried out, considering maximum slope and land use restrictions.

For thermal energy generation two different CSP technologies are considered: Parabolic Trough and Power Tower. For both of them specific different optical and thermal efficiencies are considered to estimate the thermal energy available in the solar field. Please notice that the thermal energy storage (TES) and power block are not modelled, since these depend on the energy dispatch at the output taking into account existing energy demand and other energy sources availability.

For electrical energy demand two different PV technologies are considered: single-axis tracking and fixed mounted systems. For both of them specific system losses are considered, in addition to shallow angle reflection, effects of changes in solar spectrum, and PV power dependence on irradiance and module temperature.

&nbsp;

---

---

&nbsp;

# iDesignRES Building Stock Energy Model

This README provides an overview of the Model iDesignRES Building Stock Energy Model within iDesignRES.  

It is handled by Tecnalia and part of WP1, Task number Task 1.4. 

## Purpose of the model

The objective of the model is to simulate the energy performance of the building stock of any region in Europe (NUTS Level2) both for an initial diagnosis and to evaluate different years of the transition period considered in the scenarios proposed. The aim is to cover the building stock for different uses including the residential and tertiary sector with a high degree of disaggregation in both cases. 
Besides, the model aims to generate information that provides greater granularity to the building sector models generated in the project for higher scales such as the national scale and exploitation.

## Model design philosophy

In the case of the building sector, when developing new models and functionalities that allow ESM type models (traditionally focused on covering the European and country scales) to reach a regional resolution, it is necessary to find the balance between the agility of calculation and this greater detail of analysis. In this process, it is worth highlighting the potential associated with the use of georeferenced information to capture the specificities of each region in terms of building typologies. This allows a more detailed disaggregation of the building energy model at the country level, capturing aspects such as the number of buildings, surface area, age, or the most specific use for each building typology in the region, as well as their geographic distribution. Traditional methods used for obtaining and processing detailed georeferenced data are applied at smaller scales such as the district or urban scales since they are based on cadastral data. Moreover, they are not easily replicable and automatable for other cities and regions due to their high heterogeneity. This aspect related to the specificity to the case study and the complexity of data preprocessing is an important barrier that makes it unusual to disaggregate national models at the regional level with a high degree of disaggregation of building typologies based on bottom-up data collected. 
The developed model aims to help break this barrier by treating and preprocessing geometric and semantic information of each of the buildings (level of detail at the building portal level) in the region. It follows this bottom-up georeferenced information processing approach but starting from georeferenced data available for the whole Europe and developed ad-hoc to cover larger scales such as the regional scale. This information is then used to adapt the energy calculation of the building sector through the use of building archetypes that provide greater detail for each building use. The model performs hourly simulations for given years so that they can be used for initial diagnosis and analysis of potential future scenarios.

## Input to and output from the model

Input data:

(a) For initial diagnosis: energy demand (base year assessment):

- Data to be filled in by the user: NUTS Level 2 Code or NUTS Level 3 Code.
- Main data used by the model as input (provided by the model with the option to be modified by the user in case more accurate data are available): Meteorological data (Outdoor dry bulb temperature (hourly), Radiation, Solar gains, heating, and cooling periods); geometry, surface area, age, use of each building. Other building parameters (U-values, H/C base temperature, Window-to-wall ratio, adjacent buildings).

(b) For initial diagnosis: energy consumption calculation (base year assessment):

- Main data used by the model as input (provided by the model with the option to be modified by the user in case more accurate data are available): Shares of fuels/technologies by building type (From statistical data or model results of a higher scale, used for the adjustment), Hourly profiles (for Heating, Cooling, DHW, Occupancy, Lighting, Equipment, kitchen), Installed power (Lighting, Equipment), Equipment performance, Fuel cost, Environmental impact factors.

(c) For the scenarios:

- Main data used by the model as input (provided by the model with the option to be modified by the user in case more accurate data are available): Shares of fuels/technologies of the scenario to be simulated (if available from model results of a higher scale, used for the adjustment). Investments/measurement of amount of technology deployed in each sector/type of buildings. For example (for refurbishment total m2 refurbished or associated investment, for solar PV total MW installed or associated investment, etc.).

Output data:

- Energy results: Energy demand and energy consumption by building typology: use of buildings/age/archetype/end use of energy/fuel (On an annual basis and on an hourly basis). 
- Energy generation results for building integrated solar technology. 
- Costs and CO2 emissions associated.

## Implemented features

- The model allows building stock simulations for any region in Europe avoiding most of the building data collection, treatment, and preprocessing.
- The model allows simulations of a given year on an hourly basis (based on the heating degree hours method) for both NUTS Level 2 and NUTS level 3 contained in the region.
- The model generates in a first instance the most relevant information required as input to the energy model in an automated way for the selected NUTS Level 2 region of Europe. Avoiding the user having to contact the different local, provincial, and regional entities in question for the request of cadaster shape files. The characterization obtained is at the portal level of each building in the region collecting the main characteristics in terms of use, sub-use, age, geometry, area and height, as well as their geographical distribution that can be used for finer analysis than NUTS Level 2. 
- In a second simulation phase, the model treats the information obtained and simplifies it to the level of archetypes of representative building typologies (according to the form factor) to be simulated for the region.
- The model offers a high degree of disaggregation for both the calculation and the presentation of results based on the following structure: Use - age - archetype - final use – fuel
- The model has an internal database that provides the most relevant data to perform the simulations for any region in Europe. It also offers the possibility of substituting these values for others proposed by the modeler in case more specific information is available. 
- Through new simulations of future years, the model allows to evaluate the behavior of the building stock for different scenarios that consider different degrees of deployment of certain technologies.
- Regarding the coordination with the rest of the models of higher scales that contemplate the behavior of the building sector, the developed model maintains a coherence with them using a structure of disaggregation of building typologies, final uses and fuels used, as well as allowing the use of the outputs of the simulation models at higher scales to adjust some of the parameters of the regional model.

## Core assumption

- Following the Energy Performance of Buildings Directive[1], static equations are used to determine the heating, cooling and domestic hot water (DHW) energy demand. The methodology is based on the Degree-Days method. However, to obtain a more detailed analysis, the calculation is done on an hourly basis and considers internal gains, solar gains, ventilation losses[2].
- The model does not allow optimization. It is a simulation model that allows the evaluation of prospective exploratory scenarios based on the narratives set for each proposed scenario.
- Once the information is collected for each building, the model groups areas/geometries of buildings based on a clustering of buildings according to their form factor. Three archetypes are considered for each age range of residential buildings and a single representative archetype for each sub-use of the tertiary sector (7 subcategories of tertiary buildings are considered). 
- Buildings of industrial use do not fall within the scope of the model. However, their geometric characteristics and geographic distribution across the region are considered to rule out areas available for large-scale solar technology use in the solar module. 
- Limitations in terms of technologies or measures considered in the generation of future scenarios: Rehabilitation measures are contemplated differentiating, facades, roofs, and windows (differentiating 3 levels; high, medium, low), replacement of heating and cooling systems, improvement of performances, installation of solar photovoltaic and thermal systems. To include measures related to district heating and cooling systems, they must be introduced as a new technology defining their share of fuel mix, performance, as well as other key parameters representative for the case study. 

&nbsp;

---

---

&nbsp;

# Getting started

## System requirements

The recommended system requirements are as follows:

- Broadband Internet connection.

- *RAM memory*: it is recommended to have 32GB.

- *Operating system*: the models run on any operating system that supports Python and Poetry.

- *Python*: version 3.10.

- *Poetry*: version 2.1.1.

To make sure *Python 3.10* is installed.:

```
python --version
```

And to make make sure that *Poetry 2.1.1* is installed:

```
poetry --version
```

## Installation

Clone the repository in the desired directory:

```
cd directory
git clone https://github.com/iDesignRES/Tecnalia.git
```

To install the PV Power Plants Model, enter the following commands:

```
cd "PV Power Plants Model"
poetry install
```

And to install the Building Energy Simulation Model, enter the following commands:

```
cd "Building Energy Simulation Model"
poetry install
```

## Execution

Once installed, execute the *PV Power Plants Model* entering the command:

```
poetry run python pv_power_plants.py <input_payload> <start_time> <end_time>
```

There is preloaded data for the *ES41* region. To generate data for another region, it is necessary to run the preprocessing module. To do so, enter the command:

```
poetry run python pv_power_plants_preprocess.py <nuts_id> <slope_angle>
```

Finally, to execute the *Building Energy Simulation Model*, enter the command:

```
poetry run python building_energy_process.py <input_payload> <start_time> <end_time> <building_use>
```

More details about the execution of both models and their parameters can be found in the *"PV Power Plants Model"* and *"Building Energy Simulation Model"* directories.