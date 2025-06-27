# Automator: Let the magic work 

## PreRequisites
- Access to Wallapop digital certificate for Spanish Tax Authority web portal
- Apple Automator
- Apple Safari web browser with developer tools and javascript execution enabled

## Spells book

:warning: **All the automator spells need to be customised indicating the local file**

### 01 - Automator for download all references
:warning: **Requires having the list of the presentations exported in the local file (adjusting the destination path is required)**

- Starts Safari web browser and opens Spanish Tax Authority web portal
- Reads from the list of presentation references (adjusting the destination path is required)
- Search for all the reportable sellers in each of the presentations, check if the filters are correct otherwise, adjusts them and execute again.
- Export the presentation XML file in the local system (adjusting the destination path is required).

### 02 - Automator for download presented XML files
- Starts Safari web browser and opens Spanish Tax Authority web portal
- Reads from the list of references to download in the local file (adjusting the destination path is required)
- Search for each of the presentations, check if the filters are correct otherwise, adjusts them and execute again
- Asks for all the presentation
- Export the presentation XML file in the local system. Adjusting the destination path is required.

### 03 - Automator for download presentation proof document
- Starts Safari web browser and opens Spanish Tax Authority web portal
- Reads from the list of references to download in the local file (adjusting the destination path is required)
- Search for each of the presentations, check if the filters are correct otherwise, adjusts them and execute again
- Asks for all the presentation
- Export the presentation proof PDF file in the local system. Adjusting the destination path is required.

### 03 - Automator for download corrections proof document
- Same as for presentation one but getting the data from the corrections local file.