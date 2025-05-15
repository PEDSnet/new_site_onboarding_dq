# ===================================================================================================
# Functions to read in .sql file checks, pass in variables, write to database, and output csv files.
# ===================================================================================================

import time
import datetime
import os
import csv
import zipfile
from jinja2 import Template
from config.config import *
from src.variables import *


#Read in .sql file and use JINJA templating to pass in table name and variables from varaibles.py
def read_and_render_sql_file(file_path, version = '', schema = '', vocab_schema = '', 
                             table_name = '', column_name = '',  fk_table_name = '', 
                             fk_column_name = '', filter_column_name = '', filter_column_value = ''):
    try:
        with open(file_path, 'r') as sql_file:
            sql_query = sql_file.read()
        template = Template(sql_query)
        context = {
            "version" : version,
            "schema" : schema,
            "vocab_schema" : vocab_schema,
            "table_name" : table_name,
            "column_name" : column_name,
            "fk_table_name" : fk_table_name,
            "fk_column_name" : fk_column_name,
            "filter_column_name" : filter_column_name,
            "filter_column_value" : filter_column_value
        }
        rendered_sql = template.render(context)
        return rendered_sql
    except Exception as e:
        print(f"Error rendering templated variables in SQL Query: {e}")

# Execute .sql file against postgres database
def execute_sql_file(sql_query):
    try:
        with get_db_connection('config/database.ini') as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query)
                print("Successfully executed SQL file")
    except Exception as e:
        print(f"Error executing SQL query: {e}")

# For a spefied table, read, render, and execute all .sql checks.
def render_and_execute_checks_on_table(version, schema, vocab_schema, table):

    # Table Count
    print('\n')
    print("-" * 50)
    print('Getting Table Count')
    print("-" * 50)
    site_query  = read_and_render_sql_file('src/sql/table_count.sql', version, schema,  table_name = table)
    execute_sql_file(site_query)

    # Primary Key (pk) Violations
    pk = pks.get(table)
    print('\n')
    print("-" * 50)
    print(f'Checking for Primary Key violations ({pk})')
    print("-" * 50)
    site_query  = read_and_render_sql_file('src/sql/ddl_violation_pk.sql', version, schema,  table_name = table, column_name = pk)
    execute_sql_file(site_query)

    # Non Null (nn) Violations
    print('\n')
    print("-" * 50)
    print('Checking for Non Null violations')
    print("-" * 50)
    nns = non_nulls.get(table)
    if nns:
        for nn in nns:
            print(nn)
            site_query  = read_and_render_sql_file('src/sql/ddl_violation_nn.sql', version, schema,  table_name = table, column_name = nn)
            execute_sql_file(site_query)

    # Foreign Key (fk) Violations in DDL (Non Vocabulary)
    print('\n')
    print("-" * 50)
    print('Checking for Foreign Key violations')
    print("-" * 50)
    fks = fk_other.get(table)
    if fks:
        for fk, (ref_table, ref_column) in fks.items():
            print(fk)
            site_query  = read_and_render_sql_file('src/sql/ddl_violation_fk.sql', version, schema,  table_name = table, column_name = fk, fk_table_name = ref_table, fk_column_name = ref_column)
            execute_sql_file(site_query)

    # Foreign Key (fk) Violations against Vocabulary
    print('\n')
    print("-" * 50)
    print('Checking for concept_id Foreign Key violations')
    print("-" * 50)
    fks_c = fk_concept.get(table)
    if fks_c:
        for fk_c in fks_c:
            print(fk_c)
            site_query  = read_and_render_sql_file('src/sql/ddl_violation_fk_concept.sql', version, schema, vocab_schema, table_name = table, column_name = fk_c)
            execute_sql_file(site_query)

    # Get distribution of column values in table
    print('\n')
    print("-" * 50)
    print('Calculating Column Distributions')
    print("-" * 50)
    columns = column_distribution.get(table)
    if columns:
        for col in columns:
            print(col)
            site_query  = read_and_render_sql_file('src/sql/column_distribution.sql', version, schema, vocab_schema, table_name = table, column_name = col)
            execute_sql_file(site_query)

    # Get distribution of vocabularies used for column in table
    print('\n')
    print("-" * 50)
    print('Calculating Column Vocabulary Distributions')
    print("-" * 50)
    columns_v = column_vocabulary_distribution.get(table)
    if columns_v:
        for col_v in columns_v:
            print(col_v)
            site_query  = read_and_render_sql_file('src/sql/column_vocabulary_distribution.sql', version, schema, vocab_schema, table_name = table, column_name = col_v)
            execute_sql_file(site_query)

    # Getting top 10 concept_ids for field in table
    print('\n')
    print("-" * 50)
    print('Identifying Top 10 concept_ids')
    print("-" * 50)
    top_concs = top_concepts.get(table)
    if top_concs:
        for col, filters in top_concs.items():
            if col:
                print(col)
                for filter in filters:
                    if filter:
                        if(filter[0] == -1):
                            print('Top concepts with no filter')
                        else:
                            print(f'Top concepts with filter {filter[1]} = {filter[0]}')
                        ref_column = filter[1]
                        ref_value = filter[0]
                        # filter against visit_concept_id
                        if(ref_column == 'visit_concept_id'):
                            site_query  = read_and_render_sql_file('src/sql/top_10_concept_id_filter_visit.sql', version, schema, vocab_schema, table_name = table, column_name = col, filter_column_name = ref_column, filter_column_value = ref_value)
                            execute_sql_file(site_query) 
                        # no filter column
                        elif(ref_value == -1):
                            site_query  = read_and_render_sql_file('src/sql/top_10_concept_id_no_filter.sql', version, schema, vocab_schema, table_name = table, column_name = col)
                            execute_sql_file(site_query)  
                        # filter column exist but is not visit_concept_id
                        else:
                            site_query  = read_and_render_sql_file('src/sql/top_10_concept_id_filter.sql', version, schema, vocab_schema, table_name = table, column_name = col, filter_column_name = ref_column, filter_column_value = ref_value)
                            execute_sql_file(site_query)     

    # Getting top 10 source values for unmapped concepts
    print('\n')
    print("-" * 50)
    print('Identifying Top 10 Unmapped Concepts')
    print("-" * 50)
    top_src_vals = top_unmapped_concepts.get(table)
    if top_src_vals:
        for src_val, filter_cols in top_src_vals.items():
            print(src_val)
            if filter_cols:
                for filter_col in filter_cols:
                    print(filter_col)
                    site_query  = read_and_render_sql_file('src/sql/top_10_unmapped_concepts.sql', version, schema,  table_name = table, column_name = src_val, filter_column_name = filter_col)
            execute_sql_file(site_query)  

# Exports metrics as a zip file containing a .csv for each table
def export_results(version):

    #tables to extract
    queries = {
        'column_distributions' : f"select * from dqa_nso.column_distributions where version = '{version}';",
        'column_vocabulary_distributions' : f"select * from dqa_nso.column_vocabulary_distributions where version = '{version}';",
        'ddl_constraint_violations' : f"select * from dqa_nso.ddl_constraint_violations where version = '{version}';",
        'table_count' : f"select * from dqa_nso.table_count where version = '{version}';",
        'top_10_concept_ids' : f"select * from dqa_nso.top_10_concept_ids where version = '{version}';",
        'top_10_unmapped_concepts' : f"select * from dqa_nso.top_10_unmapped_concepts where version = '{version}';"
    }

    try:
        # extract each table and write as csv in subdirectory
        with get_db_connection('config/database.ini') as conn:
            os.makedirs(f'results/{version}', exist_ok=True)
            with conn.cursor() as cur:
                for query in queries:
                    print(f'Extracting data from {query} table and writing to csv.')
                    cur.execute(queries[query])
                    rows = cur.fetchall()
                    cols = [desc[0] for desc in cur.description]
                    csv_path = os.path.join(f'results/{version}/', f'{query}.csv')
                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(cols)  # header
                        writer.writerows(rows) 
                
        #zip csv contents
        print("Zipping contents")
        with zipfile.ZipFile(f'results/{version}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(f'results/{version}/'):
                if filename.endswith('.csv'):
                    filepath = os.path.join(f'results/{version}/', filename)
                    zipf.write(filepath, arcname=filename)

        # delete csvs
        for filename in os.listdir(f'results/{version}/'):
            os.remove(os.path.join(f'results/{version}/', filename))
        os.rmdir(f'results/{version}/')
        print("Export Complete!")

    except Exception as e:
        print(f"Error executing SQL query: {e}")
