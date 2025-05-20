# Data Quality Assessment for New Site Onboarding (DQA_NSO)

The `DQA_NSO` tool is used to run a set of queries against tables modeled in the PEDSnet Data Model. It queries PEDSnet tables and writes the results to tables in a new schema called `dqa_nso`. It checks the following for input PEDSnet table:

* Row Count
* Foreign Key, Non Null, and Primary Key Constraint Violations
* Column Distributions for Key Descriptive Concepts
* Column Vocabulary Distributions for Mapped Clinial Concepts
* Top 10 Concepts to check plausibility 
* Top 10 Source Values for Unmapped Concepts

# Work Plan

## Requirements
1. `Python3` and `PIP` installed locally.
2. Ability to execute python code within a jupyter notebook.
3. Data Modeled in the PEDSnet (OMOP) CDM within a schema in postgres.
4. OMOP vocabulary tables available on the same database either within the same schema or a separate schema.

## Setup
1. Under the `database.ini` file, enter `username`, `password`, `host`, and `database` information used to connect to your postgres database.

2. Within `main.ipynb`, in Cell 2 (INPUT Variables), populate the strings for `schema`, `vocab_schema`, and `version`. Under tables, comment out or delete any tables from the list that you do not want to be tested. Data Quality testing happens on a table-by-table basis based on the tables in the tables list.

3. Install the python packages required. You can use the commented out command line commands within Cell 1 (IMPORTS) of main.ipynb to install the needed packages:
	* `!python3 -m pip install configparser`
	* `!python3 -m pip install psycopg2-binary`
	* `!python3 -m pip install jinja2`

4. Run cells 2 - 4 of `main.ipynb` to create output tables and calculate metrics to populate the output tables. Execution time will be dependent on how many tables you are testing as well as the size of your local data (number of patients, etc.).

5. Once step 4 is completed, run cell 5 (Export Results) to export the output metric tables as a zip file of csvs. The zip file will be named the same as the `version` you specified. Submit this output file back to the PEDSnet DCC.

## Output Table Definitions

### table_count
 
 > Total row count for each PEDSnet table.
 > * Fields:
 >		* `version` - Tag defined when running tool that is used to differentiate different runs from each other.
 >		* `table_name` - Name of PEDSnet table being sampled.
 >		* `record_count` - Total number of records in PEDSnet table.
 >

### ddl_constraint_violations

> Checks all Primary Key (pk), Foreign Key (fk), and Non Null (nn) constraints defined in the DDL for each table. 
> * Fields:
> 	* `version` - Tag defined when running tool that is used to differentiate different runs from each other.
> 	* `table_name` - Name of PEDSnet table being sampled.
> 	* `column_name` - The name of the column within the PEDSnet table which has the DDL constraint applied.
> 	* `constraint_type` - The type of DDL constraint being checked. Either `pk` (primary key), `fk` (foreign key), or `nn` (non null).
> 	* `violation_count` - Total number of records that violate the column_name's constraint. violation_count == 0 is good. violation_count > 0 is bad.
> 	* `violation_percentage` - Percent of records in the table that violate the column_name's constraint. Calculated as ddl_constraint_violations.violation_count divided by table_count.record_count.
>

### column_distributions

> Stratifies a PEDSnet table by a key descriptive column to get the count and percent of table for each value.
> * Not all tables will have a field tested for column distribution.
> * Fields:
> 	* `version` - Tag defined when running tool that is used to differentiate different runs from each other.
> 	* `table_name` - Name of PEDSnet table being sampled.
>  	* `column_name` - The name of the column within the PEDSnet table which is being stratified by.
> 	* `column_value_concept_id` - The distinct concept_id value for the column_name field being stratified (if field is a concept_id).
> 	* `column_value_text` - The distinct text value for the column_name field being stratified. If field is a concept_id, it is populated with the corresponding concept_name from the concept table.
> 	* `record_count` - Total number of records in the table that have this column_value_concept_id and column_value_text for the column_name.
> 	* `percent_of_table` - Percent of records in the table that have this column_value_concept_id and column_value_text for the column_name. Calculated as column_distributions.record_count divided by table_count.record_count.
>

### column_vocabulary_distributions

> For a PEDSnet table, stratifies a concept_id field by each vocabulary_id the concept_ids may belong to in the concept table.
> * Primarily used to test correctly used Vocabularies for clinical fact tables.
> * Not all tables will have a field tested for column vocabulary distribution.
> * Fields:
> 	* `version` - Tag defined when running tool that is used to differentiate different runs from each other.
> 	* `table_name` - Name of PEDSnet table being sampled.
> 	* `column_name` - The name of the column within the PEDSnet table whose concept_id value's vocabulary is being stratified.
> 	* `vocabulary_id` - The distinct vocabulary_id value from the column_name field whose concept_id value's vocabulary is being stratified.
> 	* `record_count` - Total number of records in the table that have this vocabulary_id for the column_name.
> 	* `percent_of_table` - Percent of records in the table that have this vocabulary_id for the column_name. Calculated as column_vocabulary_distributions.record_count divided by table_count.record_count.
>

### top_10_concept_ids

> For a PEDSnet table, checks the top 10 concept_id values for a defined *_concept_id field. Also can include a different column to filter by BEFORE checking the the top 10 concept_id values.
> * Primarily used to check plausibility of top codes used within for clinical fact tables.
> * Not all tables will have a field tested for top 10 concept_ids.
> * Fields:
> 	* `version` - Tag defined when running tool that is used to differentiate different runs from each other.
> 	* `table_name` - Name of PEDSnet table being sampled.
> 	* `column_name` - The name of the column within the PEDSnet table whose concept_id value's vocabulary is being stratified.
> 	* `column_value_concept_id` - The distinct concept_id value for the column_name field being stratified (if field is a concept_id).
> 	* `column_value_text` - The distinct text value for the column_name field being stratified. If field is a concept_id, it is populated with the corresponding concept_name from the concept table.
> 	* `filter_column_name` - The name of the column used to filter by before checking the top 10 concept_ids. If field is NULL, then no filter is applied.
> 	* `filter_column_value` - The value of the column used to filter by before checking the top 10 concept_ids. If field is NULL, then no filter is applied.
> 	* `rank` - Ranking (1 to 10 if applicable) of the top returned concept_id values.
> 	* `record_count` - Total number of records filtered by filter_column_name = filter_column_value that have this column_value_concept_id for the column_name.
> 	* `percent_of_table` - Percent of records filtered by filter_column_name = filter_column_value that have this column_value_concept_id for the column_name. Calculated as top_10_concept_ids.record_count divided by total number of records where filter_column_name = filter_column_value.

### top_10_unmapped_concepts

> For a PEDSnet table, checks the top 10 source values for a defined *_source_value field where its corresponding *_concept_id field equals 0 or some flavor of NULL.
> * Primarily used to check the top source values for unmapped concepts in order to see if a manual mapping is possible.
> * Not all tables will have a field tested for top 10 unmapped concepts.
> * Fields:
> 	* `version` - Tag defined when running tool that is used to differentiate different runs from each other.
> 	* `table_name` - Name of PEDSnet table being sampled.
> 	* `column_name` - The name of the source value column within the PEDSnet table whose value is being stratified.
> 	* `column_value_text` - The distinct text value for the column_name field being stratified.
> 	* `filter_column_name` - The name of the column used to filter by (checking if 0 or some flavor of NULL before checking the top 10 source values.
> 	* `rank` - Ranking (1 to 10 if applicable) of the top returned source values.
> 	* `record_count` - Total number of records filtered by filter_column_name = 0 or some flavor of NULL that have this column_value_text for the column_name.
> 	* `percent_of_table` - Percent of records filtered by filter_column_name = 0 or some flavor of NULL that have this column_value_text for the column_name. Calculated as top_10_concept_ids.record_count  divided by table_count.record_count.
> 
