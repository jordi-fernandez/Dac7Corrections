# Dac7Corrections

This project extract data from already presented files and generates the csv files used in the modifications/cancelations 
service page from the Spanish Tax Authority.

## Prerequisites

* Having the original presented files from the Spanish Tax Authority. 
  - <b>It will require digital certificate to access or someone with access can provide them</b>
  - Can be downloaded from Hacienda url
  - Or in batch using Apple automator (more info)[./automator/automator.md]
* Having identified the users to modify and/or delete its presentation
  - In the respective csv files inside the `input` containing the userId and the reportable seller presentation reference
* Having the corrected data of the users to modify
  - In the `users_to_modify_data.csv` with the specific format
  - This information is currently shared by data-engineering (as is the current feeder of the fiscal data into the user-profile service)

## Execution

Execute the main method from the `ExtractDataFromPresentation` file. 

It generates the necessary files in the output folder:

- Ones named as `Modificacion_XX_salida.csv` containing the updated activity data and the original fiscal data
- Ones names as `Borrado_XX_salida.csv` containing the original data

Both files containing the codes as required for the Spanish Tax Authority tax web portal when the csv files generated can 
be imported.