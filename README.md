# Data Quality Assesment for New Site Onboarding (DQA_NSO)

The `DQA_NSO` tool is used to run a set of queries against tables modeled in the PEDSnet Data Model. It queries PEDSnet tables and writes the results to tables in a new schema called dqa_nso. It checks the following for input PEDSnet table:

* Row Count
* Foreign Key, Non Null, and Primary Key Constraint Violations
* Column Distributions for Key Descriptive Concepts
* Column Vocabulary Distributions for Mapped Clinial Concepts
* Top 10 Concepts to check plausibility 
* Top 10 Source Values for Unmapped Concepts

# Work Plan

## Requirements
1. Python3 and PIP installed locally.
2. Ability to execute python code within a jupyter notebook.
3. Data Modeled in the PEDSnet (OMOP) CDM within a schema in postgres.
4. OMOP vocabulary tables available on the same database either within the same schema or a separate schema.

## Setup
1. Under the database.ini file, enter username, password, host, and database information used to connect to your postgres database.

2. Within main.ipynb, in Cell 2 (INPUT Variables), populate the strings for schema, vocab_schema, and version. Under tables, comment out or delete any tables from the list that you do not want to be tested. Data Quality testing happens on a table-by-table basis based on the tables in the tables list.

3. Install the python packages required. You can use the commented out command line commands within Cell 1 (IMPORTS) of main.ipynb to install the needed packages:
	* !python3 -m pip install configparser
	* !python3 -m pip install psycopg2-binary
	* !python3 -m pip install jinja2

4. Run cells 2 - 5 of main.ipynb to calculate results. Execution time will be dependent on how many tables you are testing as well as the size of your local data (number of patients, etc.)
