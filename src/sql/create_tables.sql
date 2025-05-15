BEGIN;
create schema if not exists dqa_nso;
COMMIT;

BEGIN;
create table dqa_nso.table_count (
    version varchar(256),
    table_name varchar(256),
    record_count integer
);

-- constraint_types: pk, nn, fk ddl, fk concept
create table dqa_nso.ddl_constraint_violations (
    version varchar(256),
    table_name varchar(256),
    constraint_type varchar(256),
    column_name varchar(256),
    violation_count integer,
    violation_percentage numeric
);

-- row count distribution for fields with finite expected values
create table dqa_nso.column_distributions (
    version varchar(256),
    table_name varchar(256),
    column_name varchar(256),
    column_value_concept_id integer,
    column_value_text varchar(256),
    record_count integer,
    percent_of_table numeric
);

-- row count distribution for fields with expected vocabulary
create table dqa_nso.column_vocabulary_distributions (
    version varchar(256),
    table_name varchar(256),
    column_name varchar(256),
    vocabulary_id varchar(256),
    record_count integer,
    percent_of_table numeric
);

-- top 10 values for fields with finite expected values
create table dqa_nso.top_10_concept_ids (
    version varchar(256),
    table_name varchar(256),
    column_name varchar(256),
    column_value_concept_id integer,
    column_value_text varchar(256),
    filter_column_name varchar(256),
    filter_column_value integer,
    rank integer,
    record_count integer,
    percent_of_table numeric
);

-- top 10 values for fields with finite expected values
create table dqa_nso.top_10_unmapped_concepts (
    version varchar(256),
    table_name varchar(256),
    column_name varchar(256),
    column_value_text varchar(256),
    filter_column_name varchar(256),
    rank integer,
    record_count integer,
    percent_of_table numeric
);
COMMIT;