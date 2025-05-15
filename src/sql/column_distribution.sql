BEGIN;
with numerator as (
    select 
        '{{table_name}}' as table_name,
        '{{column_name}}' as column_name,
        case 
            when cast({{column_name}} as varchar) ~ '^[0-9]+$' then {{column_name}}
            else NULL 
        end as column_value_concept_id,
        case
            when cast({{column_name}} as varchar) ~ '^[0-9]+$' then v.concept_name
            else cast({{column_name}} as varchar)
        end as column_value_text,
        count(*) as record_count,
        '{{version}}' as version
    from 
        {{schema}}.{{table_name}}
    left join
        {{vocab_schema}}.concept v 
        on case 
            when cast({{column_name}} as varchar) ~ '^[0-9]+$' then {{column_name}}::integer
            else 0
        end = concept_id
    group by
        {{column_name}},
        v.concept_name
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

insert into dqa_nso.column_distributions (
    version,
    table_name,
    column_name,
    column_value_concept_id,
    column_value_text,
    record_count,
    percent_of_table
)
select
    numerator.version,
    numerator.table_name,
    numerator.column_name,
    numerator.column_value_concept_id,
    numerator.column_value_text,
    numerator.record_count,
    trunc(cast(numerator.record_count as numeric) / cast(denominator.record_count as numeric), 4) as percent_of_table
from 
    numerator
cross join
    denominator
order by 
    numerator.record_count desc;
COMMIT;