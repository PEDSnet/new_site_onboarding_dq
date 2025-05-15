BEGIN;
with numerator as (
    select 
        '{{table_name}}' as table_name,
        '{{column_name}}' as column_name,
        {{column_name}} as column_value_text,
        '{{filter_column_name}}' as filter_column_name,
        count(*) as record_count,
        '{{version}}' as version
    from 
        {{schema}}.{{table_name}}
    where
        cast({{filter_column_name}} as varchar) in ('0','44814650','44814649','44814653')
        or {{filter_column_name}} is NULL
    group by
        {{column_name}}
    limit 10
),

denominator as (
    select 
        case when record_count > 0 then record_count else NULL::integer end as record_count
    from 
        dqa_nso.table_count
    where
        table_name = '{{table_name}}'
        and version = '{{version}}'
)

insert into dqa_nso.top_10_unmapped_concepts (
    version,
    table_name,
    column_name,
    column_value_text,
    filter_column_name,
    rank,
    record_count,
    percent_of_table
)
select
    numerator.version,
    numerator.table_name,
    numerator.column_name,
    numerator.column_value_text,
    numerator.filter_column_name,
    row_number() over (order by numerator.record_count desc) as rank,
    numerator.record_count,
    trunc(cast(numerator.record_count as numeric) / cast(denominator.record_count as numeric), 4) as percent_of_table
from 
    numerator
cross join
    denominator;
COMMIT;