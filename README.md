# Supplementing Code for the 'Migrating patient data from Excel to REDCap' Workflow

## Description
This repository contains the code used in the 'Migrating patient data from Excel to REDCap' workflow.
It contains the code for the generation of the dummy data (Create-Dummy-Data-for-TDfRI.ipynb), merging different sheets in an Excel-spreadsheet to a single CSV (Combine-Excel-Sheets-to-CSV.R) and validating the transformed data table (Transform-Data-for-REDCap-Import.ipynb and Transform_Data_for_REDCap_Import_Methods.py).

## Links to publications that cite the data
IsDescribedBy: https://doi.org/10.5281/zenodo.20700861

## Link to ancillary dataset
IsSupplementedBy and IsSupplementTo:  https://doi.org/10.5281/zenodo.20700526

## Description of the Code Files

### Create Dummy Data for 'Transform Data for REDCap Import' workflow
(2025-12-12)<br>

#### Files
Create-Dummy-Data-for-TDfRI.ipynb

#### Description
This script is was used to generate synthetic data for the "Transform Data for REDCap Import" workflow.<br>
It generates three CSV, one for each sheet in the final data XLSX.

#### Supplementing files in ancillary dataset
LLM prompts used for vibe coding: Create-Dummy-Data-for-TDfRI_Perplexity-AI-Prompts.pdf

#### Requirements and installation
It is written in Python 3.12.10 in JupyterLab 4.4.4 and provided as Jupyter Notebook.<br>
Open notebook in JupyterLab.

### Combine Excel Sheets to CSV
V05 (2026-05-25)

#### Files
Combine-Excel-Sheets-to-CSV.R

#### Description
This script merges different sheets of an Excel-Spreadsheet to a single CSV by column.<br>
Merged cells must first be unmerged in the Excel spreadsheet.

#### Supplementing files in ancillary dataset
Demo data file: 01_TransformDataforREDCapImport_Cleaned.xlsx

#### Requirements and installation
It is written in R 4.5.1 in RStudio 2026.01.2.
Open file in R or RStudio and set path to demo data file.

### Transform Data for REDCap Import
V08 (2026-02-19)<br>

#### Files
Transform-Data-for-REDCap-Import.ipynb<br>
Transform_Data_for_REDCap_Import_Methods.py<br>

#### Description
This script is intended to facilitate the preparation of data tables for the REDCap import.<br>
The data in the import file of a project is compared with the parameters stored in the data dictionary and transformed if possible.<br>
The term “errorNaN” is inserted in fields where the transformation failed. This then allows you to search for and manually correct these fields.<br>

#### Supplementing files in ancillary dataset

Demo data file: 05_TransformDataforREDCapImport_Prepared-for-validation-check.csv; 07_TransformDataforREDCapImport_Prepared-for-validation-check.csv (delimiter: ';')
Demo data dictionary: TransformDataforREDCapImportTe_DataDictionary_2026-04-09.csv (delimiter: ',')
Demo REDCap project: TransformDataforREDC_2026-04-09_1425.REDCap.xml
or single REDCap instruments: PatientInformation_2026-04-09_1416.zip; Comorbidities_2026-04-09_1424.zip; Therapy_2026-04-09_1417.zip


#### Requirements and installation
It is written in Python 3.12.10 in JupyterLab 4.4.4 and provided as Jupyter Notebook and supplementing .py file.<br>
Place both files in the same directory and open Transform-Data-for-REDCap-Import.ipynb in JupyterLab. Set paths to the demo files and data dictionary.
Use the demo REDCap project files in REDCap to create the demo instance for uploading the output CSV.

#### Usage

**Input:** Data table with the field names of the project in the header and the data dictionary.<br>
**Output:** Transformed data table with values in text format; a log file with a list of incorrect values.<br>
**Transform_Data_for_REDCap_Import_Methods.py** Contains functions, used by the notebook. adapt them, in case other validations rules are defined in your REDCap project.
**Block “Set variables and Paths; Load packages”<.** The paths to the two files are set manually here. In addition, the existing date format of the data table and the delimiters used for the input and output files are set. The block also checks whether the file paths are correct.<br>
**Block "Import data table and dictionary":** Import the data table and dictionary.<br>
**Block “Execute transformation”:** The data points are checked and transformed here. If a value cannot be transformed, e.g. text in a number field, the value is replaced by “errorVal”. If numerical values are outside the min-max range defined in the dictionary, they are logged with the field name, value and index. However, these values are not replaced by “errorVal” as REDCap accepts these values.<br> 
Dates are formatted in DD/MM/YYYY format (relevant for the import options in REDCap).<br>
If the record ID column is missing in the data table, it is added and filled with values in ascending order from 1.<br>
Errors during the date transformation, the number of “errorVal”, the values outside the min-max ranges and the header of the transformed data table are output in the block.<br>
**Block “Export transformed datatable and log”:** Saves the transformed datatable and a log file with the number of “errorVal” and the values outside the min-max ranges. These are saved as a CSV in the data table directory in the “Export” subfolder. The file names consist of the name of the data table, “_transformed_”, and the current datetime. The log file is also extended by “_log”. This means that exported data tables are not overwritten if the export is carried out several times.<br>
<br>
**Manual rework:** You can search for “errorVal” in the exported table. The position determined in this way can then be used in the original data table to check the incorrect values.<br>
<br>

## Support
The codes are provided “as is.” However, if you have any questions, please feel free to send a message to the email address listed in Michael Rabenstein's ORCID profile.

## Authors and acknowledgment
by Michael Rabenstein [ORCID](https://orcid.org/0000-0001-7712-224X)<br>
Code written with the help of: Perplexity AI. (2025). AI-generated content. [https://www.perplexity.ai](https://www.perplexity.ai)
and<br>
UKB‑GPT (2026-02-17; institutional LLM based on openai/gpt-oss-120b (OpenAI et al. (2025). gpt-oss-120b & gpt-oss-20b Model Card. arXiv. https://doi.org/10.48550/arXiv.2508.10925))<br>

## License
[BSD 3-Clause License](https://gitlab.uni-bonn.de/core-facility-rdm/transform-data-for-redcap-import/-/blob/3b730f0dd1b499532a7fe7d649a7dc1bb5f45d66/LICENSE)

## Project status and contributing
The project is not being actively developed. As a result, new versions will be released only sporadically, if at all. Feel free to fork the project.
