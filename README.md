# Supplementing Code for the 'Migrating patient data from Excel to REDCap' Workflow

## Description
This repository contains the code used in the 'Migrating patient data from Excel to REDCap' workflow.
It contains the code for the generation of the dummy data (Create-Dummy-Data-for-TDfRI.ipynb), merging different sheets in an Excel-spreadsheet to a single CSV (Combine-Excel-Sheets-to-CSV.R) and validating the transformed data table (Transform-Data-for-REDCap-Import.ipynb and Transform_Data_for_REDCap_Import_Methods.py).

## DOI of the Dataset
[https://doi.org/10.5281/zenodo.20748230](https://doi.org/10.5281/zenodo.20748230)

## Links to publications that cite the data
IsDescribedBy: [https://doi.org/10.5281/zenodo.20700861](https://doi.org/10.5281/zenodo.20700861)

## Link to ancillary dataset
IsSupplementedBy and IsSupplementTo: [https://doi.org/10.5281/zenodo.20700526](https://doi.org/10.5281/zenodo.20700526)

## Description of the Code Files

### Create Dummy Data for 'Transform Data for REDCap Import' workflow
(2025-12-12)

#### Files
Create-Dummy-Data-for-TDfRI.ipynb

#### Description
This script is was used to generate synthetic data for the "Transform Data for REDCap Import" workflow.
It generates three CSV, one for each sheet in the final data XLSX.

#### Supplementing files in ancillary dataset
LLM prompts used for vibe coding: Create-Dummy-Data-for-TDfRI_Perplexity-AI-Prompts.pdf

#### Requirements and installation
It is written in Python 3.12.10 in JupyterLab 4.4.4 and provided as Jupyter Notebook.
Open notebook in JupyterLab.

### Combine Excel Sheets to CSV
V01.0 (2026-05-25)

#### Files
Combine-Excel-Sheets-to-CSV.R

#### Description
This script merges different sheets of an Excel-Spreadsheet to a single CSV by column.
Merged cells must first be unmerged in the Excel spreadsheet.

#### Supplementing files in ancillary dataset
Demo data file: 01_TransformDataforREDCapImport_Cleaned.xlsx

#### Requirements and installation
It is written in R 4.5.1 in RStudio 2026.01.2.
Open file in R or RStudio and set path to demo data file.

### Transform Data for REDCap Import
V01.1 (2026-10-14)

#### Files
Transform-Data-for-REDCap-Import.ipynb
Transform_Data_for_REDCap_Import_Methods.py

#### Description
This script is intended to facilitate the preparation of data tables for the REDCap import.
The data in the import file of a project is compared with the parameters stored in the data dictionary and transformed if possible.
The term “errorNaN” is inserted in fields where the transformation failed. This then allows you to search for and manually correct these fields.

#### Supplementing files in ancillary dataset

Demo data file: 05_TransformDataforREDCapImport_Prepared-for-validation-check.csv; 07_TransformDataforREDCapImport_Prepared-for-validation-check.csv (delimiter: ';')
Demo data dictionary: TransformDataforREDCapImportTe_DataDictionary_2026-04-09.csv (delimiter: ',')
Demo REDCap project: TransformDataforREDC_2026-04-09_1425.REDCap.xml
or single REDCap instruments: PatientInformation_2026-04-09_1416.zip; Comorbidities_2026-04-09_1424.zip; Therapy_2026-04-09_1417.zip


#### Requirements and installation
It is written in Python 3.12.10 in JupyterLab 4.4.4 and provided as Jupyter Notebook and supplementing .py file.
Place both files in the same directory and open Transform-Data-for-REDCap-Import.ipynb in JupyterLab. Set paths to the demo files and data dictionary.
Use the demo REDCap project files in REDCap to create the demo instance for uploading the output CSV.

#### Usage

**Input:** Data table with the field names of the project in the header and the data dictionary.<br>
**Output:** Transformed data table with values in text format; a log file with a list of incorrect values.<br>
**Transform_Data_for_REDCap_Import_Methods.py** Contains functions, used by the notebook. adapt them, in case other validations rules are defined in your REDCap project.<br>
**Block “Set variables and Paths; Load packages”<.** The paths to the two files are set manually here. In addition, the existing date format of the data table and the delimiters used for the input and output files are set. The block also checks whether the file paths are correct.<br>
**Block "Import data table and dictionary":** Import the data table and dictionary.<br>
**Block “Execute transformation”:** The data points are checked and transformed here. If a value cannot be transformed, e.g. text in a number field, the value is replaced by “errorVal”. If numerical values are outside the min-max range defined in the dictionary, they are logged with the field name, value and index. However, these values are not replaced by “errorVal” as REDCap accepts these values.<br> 
Dates are formatted in DD/MM/YYYY format (relevant for the import options in REDCap).<br>
If the record ID column is missing in the data table, it is added and filled with values in ascending order from 1.<br>
Errors during the date transformation, the number of “errorVal”, the values outside the min-max ranges and the header of the transformed data table are output in the block.<br>
**Block “Export transformed datatable and log”:** Saves the transformed datatable and a log file with the number of “errorVal” and the values outside the min-max ranges. These are saved as a CSV in the data table directory in the “Export” subfolder. The file names consist of the name of the data table, “_transformed_”, and the current datetime. The log file is also extended by “_log”. This means that exported data tables are not overwritten if the export is carried out several times.<br>

**Manual rework:** You can search for “errorVal” in the exported table. The position determined in this way can then be used in the original data table to check the incorrect values.<br>

#### Patch notes
V01.1 (2026-10-14): A bug has been fixed in the 'Export transformed data table, log and error report' cell, which caused an error if no out-of-range values were detected (empty out_of_range_log variable).<br>

## Support
The codes are provided “as is.” However, if you have any questions, please feel free to send a message to the email address listed in Michael Rabenstein's ORCID profile.

## Authors and acknowledgment
by Michael Rabenstein [ORCID](https://orcid.org/0000-0001-7712-224X)<br>
Code written with the help of:<br>
Perplexity AI (2025)<sup>1</sup><br>
UKB‑GPT (2026-02-17; institutional LLM based on openai/gpt-oss-120b<sup>2</sup><br>
UKB-GPT (2026-10-14; institutional LLM based on Qwen/Qwen3.8-27B-FP8)<sup>3</sup><br>

<sup>1</sup>**Perplexity AI: AI-powered search engine**. https://www.perplexity.ai<br>
<sup>2</sup>**gpt-oss-120b & gpt-oss-20b Model Card**<br>
OpenAI: Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Altman, Andy Applebaum, Edwin Arbus, Rahul K. Arora, Yu Bai, Bowen Baker, Haiming Bao, Boaz Barak, Ally Bennett, Tyler Bertao, Nivedita Brett, Eugene Brevdo, Greg Brockman, Sebastien Bubeck, Che Chang, Kai Chen, Mark Chen, Enoch Cheung, Aidan Clark, Dan Cook, Marat Dukhan, Casey Dvorak, Kevin Fives, Vlad Fomenko, Timur Garipov, Kristian Georgiev, Mia Glaese, Tarun Gogineni, Adam Goucher, Lukas Gross, Katia Gil Guzman, John Hallman, Jackie Hehir, Johannes Heidecke, Alec Helyar, Haitang Hu, Romain Huet, Jacob Huh, Saachi Jain, Zach Johnson, Chris Koch, Irina Kofman, Dominik Kundel, Jason Kwon, Volodymyr Kyrylov, Elaine Ya Le, Guillaume Leclerc, James Park Lennon, Scott Lessans, Mario Lezcano-Casado, Yuanzhi Li, Zhuohan Li, Ji Lin, Jordan Liss, Lily (Xiaoxuan)Liu, Jiancheng Liu, Kevin Lu, Chris Lu, Zoran Martinovic, Lindsay McCallum, Josh McGrath, Scott McKinney, Aidan McLaughlin, Song Mei, Steve Mostovoy, Tong Mu, Gideon Myles, Alexander Neitz, Alex Nichol, Jakub Pachocki, Alex Paino, Dana Palmie, Ashley Pantuliano, Giambattista Parascandolo, Jongsoo Park, Leher Pathak, Carolina Paz, Ludovic Peran, Dmitry Pimenov, Michelle Pokrass, Elizabeth Proehl, Huida Qiu, Gaby Raila, Filippo Raso, Hongyu Ren, Kimmy Richardson, David Robinson, Bob Rotsted, Hadi Salman, Suvansh Sanjeev, Max Schwarzer, D. Sculley, Harshit Sikchi, Kendal Simon, Karan Singhal, Yang Song , Dane Stuckey, Zhiqing Sun, Philippe Tillet, Sam Toizer, Foivos Tsimpourlas, Nikhil Vyas, Eric Wallace, Xin Wang, Miles Wang, Olivia Watkins, Kevin Weil, Amy Wendling, Kevin Whinnery, Cedric Whitney, Hannah Wong, Lin Yang, Yu Yang, Michihiro Yasunaga, Kristen Ying, Wojciech Zaremba, Wenting Zhan, Cyril Zhang, Brian Zhang, Eddie Zhang, Shengjia Zhao. arXiv, 2025.arXiv:2508.10925 (https://doi.org/10.48550/arXiv.2508.10925)<br>
<sup>3</sup>**Secure On-Premise Deployment of Open-Weights Large Language Models in Radiology: An Isolation-First Architecture with Prospective Pilot Evaluation**<br>
Sebastian Nowak*, Jann-Frederick Laß*, Narine Mesropyan, Babak Salam, Nico Piel, Wolfgang Block, Alois Martin Sprinkart, Julian Alexander Luetkens, Benjamin Wulff*, Alexander Isaak* (_*contributed equally_). arXiv preprint, 2026. arXiv:2604.22768 (https://doi.org/10.48550/arXiv.2604.22768)
<br>
## License
[BSD 3-Clause License](https://github.com/Core-Facility-Research-Data-Management/Supplementing-Code-for-the-Migrating-patient-data-from-Excel-to-REDCap-Workflow/blob/main/LICENSE)

## Project status and contributing
The project is not being actively developed. As a result, new versions will be released only sporadically, if at all. Feel free to fork the project.
